import socket
import re
from threading import Thread
import time

from util import trace, letterToCol, settings
from go_game import COLOR_BLACK, COLOR_WHITE, otherColor
from sabaki_com import comInstance as sabakiCom

class TwitchBot(Thread):
    
    def __init__(self, game):
        super(TwitchBot, self).__init__()
        self.running = False
        self.game = game
        self.useServerCoordinates = settings["use_server_coordinates"]
        self.servers = {}
        for serv in settings["servers"]:
            self.servers[serv["name"]] = {"i_col": serv["i_col"], "reversed_rows": serv["reversed_rows"]}
        self.currentServer = None
        self.channel = settings["twitch_channel"]
        self.refreshRate = settings["twitch_chat_refresh_delay"]
        self.socketBufferSize = settings["twitch_buffer_size"]
        self.initSocket()
        
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
            trace("Logged in to twitch chat.", 1)
            
        self.ircSend("JOIN #%s\r\n" % self.channel)
        self.running = True
        
    def ircSend(self, message):
        self.socket.send(message)
        
    def writeMessage(self, message):
        self.ircSend("PRIVMSG #%s :%s" % (self.channel, message))
        
    def getIRCData(self):
        try:
            return self.socket.recv(self.socketBufferSize)
        except socket.timeout:
            pass
        
    def setCurrentServer(self, server):
        self.currentServer = server
        
    def getMessages(self):
        # twitch message structure ->   :<user>!<user>@<user>.tmi.twitch.tv PRIVMSG #<channel> :This is a sample message
        messages = []
        data = self.getIRCData()
        if data is None:
            return messages
        if "PING :tmi.twtich.tv" in data:
            self.ircSend("PONG :tmi.twitch.tv")
        matches = re.findall(":(.+)\!(.+)\@(.+).tmi.twitch.tv PRIVMSG #%s :(.+)$" % self.channel, data, re.MULTILINE)
        for match in matches:
            print match
            user = match[0]
            content = match[3].rstrip()
            trace("Got message %s from %s" % (content, user), 1)
            messages.append( (content, user) )
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
        trace("Parsing message %s" % str(message), 1)
        content, user = message
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
            trace("First player %d" % firstMove, 1)
            
            # Change the coordinates into (col, row) tuples
            moves = []
            color = self.game.nextPlayer() if firstMove == 0 else firstMove
            for match in coordMatches:
                coords = self.parseCoordinates(match)
                moves.append( (coords, color) )
                color = otherColor(color)
            trace("Moves %s" % str(moves), 1)
            
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
                    trace("Expanding previous variation %d" % variationNumber, 1)
            else:
                variationIndex = self.game.addVariation(moves)
                
            # if len(moves) == 0 and not hasOrigin:   
                # return
            variationSgf, nMoves = self.game.getVariation(variationIndex)
            sabakiCom.requestVariation(variationSgf, user, nMoves)
    
    def run(self):
        trace("Twitch bot start", 2)
        while self.running:
            trace("Twitch bot update", 2)
            messages = self.getMessages()
            for message in messages:
                self.parseMessage(message)
            time.sleep(self.refreshRate)
        trace("Twitch bot end", 2)
        
    def stop(self):
        self.running = False
        
def getTwitchBot(gameState):
    bot = TwitchBot(gameState)
    return bot
            
if __name__ == "__main__":
    bot = getTwitchBot()
    bot.start()
    bot.join()
    