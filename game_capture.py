from ctypes import windll
import time
import os
from threading import Thread

import win32gui
import win32ui
import pyscreenshot as ImageGrab
import PIL

from go_game import Game, COLOR_WHITE, COLOR_BLACK
from sabaki_com import comInstance as sabakiCom
from util import trace, settings

def replacePixel(img, xy):
    (r, g, b) = img.getpixel(xy)
    if b < 70:
        img.putpixel(xy, (0, 0, 0) )
        return COLOR_BLACK
    elif b > 145:
        img.putpixel(xy, (255, 255, 255) )
        return COLOR_WHITE
    else:
        img.putpixel(xy, (128, 128, 128) )
        return 0

class ScreenshotDaemon(Thread):

    def __init__(self, game, twitchBot):
        super(ScreenshotDaemon, self).__init__()
        self.active = False
        self.game = game
        self.twitchBot = twitchBot
        self.nMoves = 0
        self.servers = {}
        self.debugCapture = settings["setup_capture"]
        self.timeBetweenCaptures = settings["time_between_captures"]
        
    def findLaunchedApps(self):
    
        # ----- Get the go apps handles -----
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            title = win32gui.GetWindowText(hwnd)
            if title != "":
                trace("Found window %s - %s " % (hwnd, title), 3)
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)

        self.servers = {}

        for serv in settings["servers"]:
            pattern = serv["pattern"]
            try:
                server = [(hwnd, title) for hwnd, title in winlist if pattern in title.lower()] [0] # Grab the first matching window handle
                self.servers[serv["name"]] = {"hwnd": server[0], "windowname": server[1], "cropleft": serv["crop_left"], "cropright": serv["crop_right"], "croptop": serv["crop_top"], "cropbottom": serv["crop_bottom"], }
            except Exception:
                trace("Couldn't find a window handle for server " + serv["name"], 2)

        trace("\n#####\nServers found:\n%s\n#####\n" % str(self.servers.keys()), 1)
        
    def takeScreenshot(self):
        # ----- Capture the corresponding part of the screen -----
        
        hwnd = win32gui.GetForegroundWindow()
        # hwnd = servers["Crazystone"]["hwnd"] # For debugging
        
        for name, serv in self.servers.iteritems():
            if serv["hwnd"] == hwnd:
                left, top, right, bot = win32gui.GetClientRect(hwnd)
                w = right - left
                h = bot - top
                
                hwndDC = win32gui.GetWindowDC(hwnd)
                mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
                saveDC = mfcDC.CreateCompatibleDC()
                
                saveBitMap = win32ui.CreateBitmap()
                saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

                saveDC.SelectObject(saveBitMap)
                
                result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
                
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)
                
                # FIXME find a way to make this work since it should be faster ?
                # bmpstr2 = ""
                # capBegin = (int(t)-top) * bmpinfo["bmWidth"]
                # capW = int(r) - int(l)
                # capH = int(b) - int(t)
                # begin = capBegin
                # for i in range(capH):
                    # begin += bmpinfo["bmWidth"]
                    # end = begin + capW
                    # bmpstr2 += bmpstr[begin:end]
                # print "%d - %d" % (capW * capH, len(bmpstr2))
                # img = PIL.Image.frombytes("RGB", (capW, capH), bmpstr2, "raw", "BGRX", 0, 1)
                # ioStr = StringIO.StringIO(bmpstr2)
                # img = PIL.Image.open(ioStr)
                w = bmpinfo["bmWidth"]
                h = bmpinfo["bmHeight"]
                img = PIL.Image.frombytes("RGB", (w, h), bmpstr, "raw", "BGRX", 0, 1)
                
                l = w * serv["cropleft"] / 100.0
                r = w * (1 - serv["cropright"] / 100.0)
                t = h * serv["croptop"] / 100.0
                b = h * (1 - serv["cropbottom"] / 100.0)
                trace("Capture coordinates : %d %d %d %d" % (l,t,r,b), 2)
                
                img = img.crop( (l, t, r, b) )
                
                if self.debugCapture:
                    img.show()
                
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                
                img = img.resize((19, 19), PIL.Image.BOX)
                
                board = []
                
                for i in range(19):
                    col = []
                    for j in range(19):
                        color = replacePixel(img, (i, j))
                        col.append(color)
                    board.append(col)
                    
                if self.debugCapture:
                    img.show()
                    
                self.twitchBot.setCurrentServer(name)
                self.game.updateGame(board)
                return
                
    def run(self):
        trace("Game capture daemon start", 1)
        self.active = True
        self.counter = 0
        while self.active:
            gameMoves = self.game.state.nMoves
            if self.counter % 100 == 0:
                trace("self moves %d - game moves %d" % (self.nMoves, gameMoves), 2)
                self.findLaunchedApps()
            self.takeScreenshot()
            self.counter += 1
            if self.counter >= 1000:
                self.counter = 0
            time.sleep(self.timeBetweenCaptures)
            if gameMoves != self.nMoves:
                sabakiCom.updateGameState(self.game.getSgf())
                self.nMoves = gameMoves
        trace("Game capture daemon end", 1)
            
    def stop(self):
        self.active = False
    
def getScreenshotDaemon(gameState, twitchBot):
    daemonThread = ScreenshotDaemon(gameState, twitchBot)
    return daemonThread