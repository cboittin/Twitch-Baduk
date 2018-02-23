from threading import Thread, Timer
from datetime import datetime
from collections import deque
import time

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import simplejson as json

from util import trace, settings

DUMMY_SGF = "(;FF[4]GM[1]SZ[19]AP[SGFC:1.13b] \
\
PB[troy]BR[12k*]\
PW[john]WR[11k*]\
KM[0.5]RE[W+12.5]\
DT[1998-06-15]\
TM[600]\
\
;B[pd];W[dp];B[pq];W[dd];B[qk];W[jd];B[fq];W[dj];B[jp];W[jj]\
;B[cn]LB[dn:A][po:B]C[dada: other ideas are 'A' (d6) or 'B' (q5)]\
;W[eo](;B[dl]C[dada: hm - looks troublesome.\
Usually B plays the 3,3 invasion - see variation];W[qo];B[qp]\
;W[sr];B[sk];W[sg];B[pa];W[gc];B[pi];W[ph];B[de];W[ed];B[kn]\
;W[dh];B[eh];W[se];B[sd];W[af];B[ie];W[id];B[hf];W[hd];B[if]\
;W[fp];B[gq];W[qj];B[sj];W[rh];B[sn];W[so];B[sm];W[ep];B[mn])\
(;W[dq]N[wrong direction];B[qo];W[qp]))"


class VariationRequestsHandler:
    def __init__(self, comInstance):
        self.comInstance = comInstance
        self.activeVariation = None
        self.variationQueue = deque([])
        self.users = {}
        self.nPostsMax = int(settings["allowed_variations_per_user"])
        self.resetTimer = int(settings["reset_variation_count_timer"])
        self.baseVariationTime = int(settings["base_variation_displaying_time"])
        self.variationTimePerStone = int(settings["variation_displaying_time_per_stone"])
        self.lastResetTime = datetime.now()
        
    def canUserPost(self, user):
        try:
            posts = self.users[user]
            return posts < 3
        except KeyError:
            return True
            
    def resetUserCount(self):
        self.users = {}
        
    def update(self):
        timelapse = (datetime.now() - self.lastResetTime).total_seconds()
        if timelapse > self.resetTimer * 60:
            self.resetUserCount()
            self.lastResetTime = datetime.now()
        
    def addVariation(self, variation, user, nMoves):
        self.update()
        if self.canUserPost(user):
            self.variationQueue.append( (variation, self.variationTime(nMoves)) )
            if user in self.users.keys():
                self.users[user] += 1
            else:
                self.users[user] = 1
    
    def variationTime(self, nMoves):
        return self.baseVariationTime + nMoves * self.variationTimePerStone
    
    def getVariation(self):
        if len(self.variationQueue) == 0:
            return None
        return self.variationQueue.popleft()

class SabakiCommunication(Thread):
    
    def __init__(self):
        super(SabakiCommunication, self).__init__()
        self.variationsHandler = VariationRequestsHandler(self)
        self.gameState = None
        self.showingVariation = False
        self.wsHandler = None
        self.paused = False
        
    def bindWsHandler(self, wsHandler):
        self.wsHandler = wsHandler
        
    def run(self):
        trace("Websocket server start", 1)
        tornado.ioloop.IOLoop.instance().start()
        trace("Websocket server end", 1)
        
    def stop(self):
        self.wsHandler.close()
        tornado.ioloop.IOLoop.instance().stop()
        
    def closeSabaki(self):
        trace("Sending close request to Sabaki", 1)
        self.wsHandler.write_message(json.dumps({"action": "close"}, separators=(",", ":") ))

    def sendGame(self, sgf):
        trace("Sending game to sabaki", 1)
        self.wsHandler.write_message(json.dumps({"action": "play", "data": sgf}, separators=(",", ":") ))

    def sendVariation(self, sgf):
        trace("Sending variation to sabaki", 1)
        self.wsHandler.write_message(json.dumps({"action": "play", "data": sgf}, separators=(",", ":") ))
        
    def updateGameState(self, sgf):
        self.gameState = sgf
        self.update()
        
    def requestVariation(self, sgf, user, nMoves):
        self.variationsHandler.addVariation(sgf, user, nMoves)
        self.update()
        
    def update(self):
        if self.showingVariation:
            return
        while self.paused:
            time.sleep(1)
        variation = self.variationsHandler.getVariation()
        if variation is not None:
            self.showingVariation = True
            sgf, displayTime = variation
            self.sendVariation(sgf)
            timer = Timer(displayTime, self._endTimer)
            timer.start()
        elif self.gameState is not None:
            self.sendGame(self.gameState)
        
    def _endTimer(self):
        self.showingVariation = False
        self.update()
        
    def pauseComms(self):
        self.paused = True
        
    def resumeComms(self):
        self.paused = False
    
comInstance = SabakiCommunication()

class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        trace("Sabaki connection open", 0)
        comInstance.bindWsHandler(self)
        self.write_message(json.dumps({"action": "hi !"}, separators=(",", ":") ))
    
    def on_message(self, message):
        trace("From Sabaki : " + message, 1)
        
    def on_close(self):
        trace("Sabaki connection closed", 0)
    
    def check_origin(self, origin):
        return True
        
def startSabakiCommunication():
    application = tornado.web.Application( [(r'/', WSHandler), ] )
        
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(4257, address="localhost")
    for sock in http_server._sockets.values():
        trace(sock.getsockname(), 2)
        trace("#####", 2)
        
    return comInstance


if __name__ == "__main__":
    inst = startSabakiCommunication()
    tornado.ioloop.IOLoop.instance().start()