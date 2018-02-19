import win32gui
import time
import os
from threading import Thread

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
                trace("Found window %s - %s " % (hwnd, title), level=2)
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

        trace("\n#####\nServers found:\n")
        trace(self.servers)
        trace("\n#####\n")
        
    def takeScreenshot(self):
        # ----- Capture the corresponding part of the screen -----
        
        hwnd = win32gui.GetForegroundWindow()
        # hwnd = servers["Crazystone"]["hwnd"] # For debugging
        
        for name, serv in self.servers.iteritems():
            if serv["hwnd"] == hwnd:
                bbox = win32gui.GetClientRect(hwnd)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                l = bbox[0] + w * serv["cropleft"] / 100.0
                r = bbox[2] - w * serv["cropright"] / 100.0
                t = bbox[1] + h * serv["croptop"] / 100.0
                b = bbox[3] - h * serv["cropbottom"] / 100.0
                trace(bbox)
                trace("Capture coordinates : %d %d %d %d" % (l,t,r,b), 1)
                if win32gui.GetForegroundWindow() == hwnd: # Check that the active window didn't change during the previous operations
                    img = ImageGrab.grab( (l, t, r, b) )
                    if self.debugCapture:
                        img.show()
                        # img.save(os.path.join("C:\\", "Users", "Me", "path, "to", "folder", str(self.counter) + ".jpg"))
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
        trace("Game capture daemon start", 2)
        self.active = True
        self.counter = 0
        while self.active:
            gameMoves = self.game.state.nMoves
            if self.counter % 10 == 0:
                trace("self moves %d - game moves %d" % (self.nMoves, gameMoves), 1)
                self.findLaunchedApps()
            self.takeScreenshot()
            self.counter += 1
            if self.counter >= 1000:
                self.counter = 0
            time.sleep(self.timeBetweenCaptures)
            if gameMoves != self.nMoves:
                sabakiCom.updateGameState(self.game.getSgf())
                self.nMoves = gameMoves
        trace("Game capture daemon end", 2)
            
    def stop(self):
        self.active = False
            
def getScreenshotDaemon(gameState, twitchBot):
    daemonThread = ScreenshotDaemon(gameState, twitchBot)
    return daemonThread