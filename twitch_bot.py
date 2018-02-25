import socket
import re
import os
from threading import Thread, Timer
import time
import datetime

from util import trace, letterToCol, settings
from go_game import COLOR_BLACK, COLOR_WHITE, otherColor
from greenscreen import GreenScreenGenerator

class TwitchBot(Thread):
    
    def __init__(self, game):
        super(TwitchBot, self).__init__()
        self.running = False
        self.game = game
        self.useServerCoordinates = settings["use_server_coordinates"]
        self.useSabaki = settings["use_sabaki"]
        if self.useSabaki:
            from sabaki_com import comInstance as sabakiCom
        
        self.channel = settings["twitch_channel"]
        self.refreshRate = settings["twitch_chat_refresh_delay"]
        self.socketBufferSize = settings["twitch_buffer_size"]
        self.servers = {}
        for serv in settings["servers"]:
            self.servers[serv["name"]] = {"i_col": serv["i_col"], "reversed_rows": serv["reversed_rows"]}
        self.currentServer = None
        self.lastPing = None
        
        self.greenscreenActive = settings["generate_greenscreen_image"]
        if self.greenscreenActive:
            self.greenScreenGenerator = GreenScreenGenerator()
        
        self.initSocket()
        
        
##### IRC socket management #####
    
    def initSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        
        try:
            sock.connect( (settings["twitch_host"], settings["twitch_port"]) )
        except:
            trace("Cannot connect to server %s:%s" % (settings["twitch_host"], settings["twitch_port"]), 0)
            return
        
        self.socket = sock    
        # sock.settimeout(None)
        
        self.ircSend("PASS %s\r\n" % settings["twitch_bot_oauth"])
        self.ircSend("NICK %s\r\n" % settings["twitch_bot_name"])
        self.ircSend("USER %s 8 * %s\r\n" % (settings["twitch_bot_name"], settings["twitch_bot_name"]) )
        
        data = sock.recv(1024)
        if "Login unsuccessful" in data:
            trace("Couldn't login to twitch chat, your bot's password is probably wrong.", 0)
            return
        else:
            trace("Logged in to twitch chat.", 0)
            
        self.ircSend("JOIN #%s\r\n" % self.channel)
        self.running = True
        self.lastPing = datetime.datetime.now()
        
    def checkConnection(self):
        currentTime = datetime.datetime.now()
        if (currentTime - self.lastPing).total_seconds() > 320:
            trace("No ping received in the last 5 minutes, reconnecting to twitch chat ...", 0)
            self.initSocket()
        
    def ircSend(self, message):
        self.socket.send(message)
        
    def writeMessage(self, message):
        self.ircSend("PRIVMSG #%s :%s" % (self.channel, message))
        
    def getIRCData(self):
        try:
            data = self.socket.recv(self.socketBufferSize)
            return data
        except socket.timeout:
            trace("No message from twitch", 2)
        
    def setCurrentServer(self, server):
        self.currentServer = server
        
        
##### Bot functionalities #####
    
    def getMessages(self):
        # twitch message structure ->   :<user>!<user>@<user>.tmi.twitch.tv PRIVMSG #<channel> :This is a sample message
        messages = []
        data = self.getIRCData()
        if data is None:
            return messages
        trace("Got message %s" % data, 2)
        if "PING :tmi.twitch.tv" in data:
            trace("Sending pong", 3)
            self.ircSend("PONG :tmi.twitch.tv")
        matches = re.findall(":(.+)\!(.+)\@(.+).tmi.twitch.tv PRIVMSG #%s :(.+)$" % self.channel, data, re.MULTILINE)
        for match in matches:
            user = match[0]
            content = match[3].rstrip()
            messages.append( (content.lower(), user) )
        return messages
    
    def parseCoordinates(self, coordsStr):
        col = int(letterToCol(coordsStr[0]))
        row = int(coordsStr[1:]) - 1
        iCol = None
        reversedRows = None
        if self.useServerCoordinates and self.currentServer is not None:
            iCol = self.servers[self.currentServer]["i_col"]
            reversedRows = self.servers[self.currentServer]["reversed_rows"]
        else:
            iCol = settings["coordinates_use_i_col"]
            reversedRows = settings["coordinates_reversed_rows"]
        if not iCol and col > 7:
            col -= 1
        if reversedRows:
            row = 18 - row
        return (col, row)
    
    def parseMessage(self, message):
        content, user = message
        trace("Parsing message %s from %s" % (content, user), 2)
        # Check for game sequence
        coordMatches = re.findall("[a-z][0-9]{1,2}", content)
        trace(coordMatches, 1)
        if len(coordMatches) > 0:
            trace("Found coordinates from twitch chat !", 1)
            
            # Check if there is a color for the first move
            if re.match("b [a-z][0-9]{1,2}", content):
                firstMove = COLOR_BLACK
            elif re.match("w [a-z][0-9]{1,2}", content):
                firstMove = COLOR_WHITE
            else:
                firstMove = 0
            trace("First player %d" % firstMove, 2)
            
            # Change the coordinates into (col, row) tuples
            moves = []
            color = self.game.nextPlayer() if firstMove == 0 else firstMove
            for match in coordMatches:
                coords = self.parseCoordinates(match)
                moves.append( (coords, color) )
                color = otherColor(color)
            trace("Moves %s" % str(moves), 2)
            
            # Check if the variation has a specific origin in the game tree, then send it to the game state
            variationIndex = None
            hasOrigin = re.match("(move)|(variation) ([0-9]+)", content)
            if hasOrigin:
                origin = re.match("move ([0-9]+)", content)
                if not origin:
                    variation = re.match("variation ([0-9]+)", content)
                    variationNumber = int(variation[0])
                    variationIndex = self.game.expandVariation(moves, variationNumber)
                    trace("Expanding previous variation %d" % variationNumber, 1)
                else:
                    moveNumber = int(origin[0])
                    variationIndex = self.game.addVariation(moves, moveNumber)
                    trace("Creating variation %d from move %d" % (variationIndex, moveNumber), 1)
            else:
                variationIndex = self.game.addVariation(moves)
                trace("Creating variation %d" % variationIndex, 1)
            
            # if len(moves) == 0 and not hasOrigin:   
                # return
            variationSgf, nMoves = self.game.getVariation(variationIndex)
            if self.useSabaki:
                sabakiCom.requestVariation(variationSgf, user, nMoves)
            if self.greenscreenActive:
                self.greenScreenGenerator.generateGreenScreen(moves, user)
    
##### Bot management #####
    
    def run(self):
        trace("Twitch bot start", 1)
        while self.running:
            trace("Twitch bot update", 2)
            messages = self.getMessages()
            for message in messages:
                self.parseMessage(message)
            self.checkConnection()
            time.sleep(self.refreshRate)
        trace("Twitch bot end", 1)
        
    def stop(self):
        self.running = False
    

def getTwitchBot(gameState):
    bot = TwitchBot(gameState)
    return bot
            
if __name__ == "__main__":
    bot = getTwitchBot()
    bot.start()
    bot.join()
    