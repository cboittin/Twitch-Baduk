import keyboard # List of keyboard keys at https://github.com/boppreh/keyboard/blob/master/keyboard/_canonical_names.py

from game_capture import getScreenshotDaemon
from sabaki_com import startSabakiCommunication
from twitch_bot import getTwitchBot
from go_game import Game
from util import trace, settings
    
class ProgramManager:
    def __init__(self):
        self.parseKeys()
        
        self.gameState = Game()
        
        self.comThread = startSabakiCommunication()
        self.twitchBot = getTwitchBot(self.gameState)
        self.daemonThread = getScreenshotDaemon(self.gameState, self.twitchBot)
        
        self.daemonThread.start()
        self.comThread.start()
        self.twitchBot.start()
        
        self.communicationActive = True
        
        keyboard.hook(self.keyCheck)
        
    def parseKeys(self):
        self.ctrl = False
        self.shift = False
        self.alt = False
        self.keyMap = {}
        for method, key in settings["keys"].iteritems():
            modMask = 4 if "ctrl" in key else 0
            modMask = modMask | 2 if "shift" in key else modMask
            modMask = modMask | 2 if "alt" in key else modMask
            if modMask != 0:
                key = key.rsplit("+", 1)[1]
            self.keyMap[key] = (getattr(self, method), modMask)
        
    def modKeyCheck(self, modMask):
        if modMask == 0:
            return True
        ctrl = False if modMask & 4 and not self.ctrl else True
        shift  = False if modMask & 2 and not self.shift else True
        alt = False if modMask & 1 and not self.alt else True
        return ctrl and shift and alt
        
    def keyCheck(self, kbEvent):
        if kbEvent.event_type == keyboard.KEY_DOWN:
            if kbEvent.name in ("ctrl", "left ctrl", "right ctrl"):
                self.ctrl = True
                trace("ctrl pressed", 3)
            elif kbEvent.name in ("shift", "left shift", "right shift"):
                self.shift = True
                trace("shift pressed", 3)
            elif kbEvent.name in ("alt", "left alt", "alt gr"):
                self.alt = True
                trace("alt pressed", 3)
            else:
                trace("Received keyboard event %s - %s" % (kbEvent.name, kbEvent.scan_code), 3)
                try:
                    method, modifiers = self.keyMap[kbEvent.name]
                    if self.modKeyCheck(modifiers):
                        method()
                except KeyError:
                    pass
        else:
            if kbEvent.name in ("ctrl", "left ctrl", "right ctrl"):
                self.ctrl = False
                trace("ctrl released", 3)
            elif kbEvent.name in ("shift", "left shift", "right shift"):
                self.shift = False
                trace("shift released", 3)
            elif kbEvent.name in ("alt", "left alt", "alt gr"):
                self.alt = False
                trace("alt released", 3)
        
    def endProgram(self):
        trace("Ending program", 0)
        self.comThread.stop()
        del self.comThread
        self.twitchBot.stop()
        del self.twitchBot
        self.daemonThread.stop()
        del self.daemonThread
        
    def toggleCommunication(self):
        if self.communicationActive:
            trace("Pausing updates to sabaki", 0)
            self.comThread.pauseComms()
            self.communicationActive = False
        else:
            trace("Resuming updates to sabaki", 0)
            self.comThread.resumeComms()
            self.communicationActive = True
            
if __name__ == "__main__":
    mgr = ProgramManager()
    mgr.comThread.join()
    keyboard.unhook_all()
    del mgr