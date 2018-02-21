from util import trace, coordsToStr

# ----- Go game logic -----

COLOR_BLACK = 1
COLOR_WHITE = -1

def otherColor(color):
    return color * -1

def remove_duplicates(li):
    """ Inefficient method, but used on lists of size 4 max so it doesn't matter """
    remove = []
    for i in range(len(li)):
        item = li[i]
        if item in li[i+1:]:
            remove.append(item)
    for item in remove:
        li.remove(item)

class Node:
    def __init__(self, color, data, moveNumber, markup=None):
        if color == COLOR_BLACK:
            self.type = "B"
        else:
            self.type = "W"
        self.data = data
        self.markup = markup
        self.prev = None
        self.children = []
        self.moveNumber = moveNumber
        
    def toString(self):
        if self.markup is None:
            return "%s[%s]" % (self.type, self.data)
        else:
            return "%s[%s]LB[%s]" % (self.type, self.data, self.markup)
        
    def addChild(self, child):
        self.children.append(child)
        child.prev = self
        return child
        
    def sgfToNode(self):
        """ Gives an sgf representation of the entire branch up to this node, minus the header """
        node = self
        nodes = [node.toString()]
        while node.prev is not None:
            node = node.prev
            nodes.append(node.toString())
        nodes.reverse()
        return ";" + ";".join(nodes)
        
    def sgfTree(self):
        """ Gives an sgf representation of the entire tree starting from this node """
        sgfString = ""
        toParse = [self]
        level = 0
        while len(toParse) > 0:
            cur = toParse.pop()
            sgfString.append(";" + toParse.toString)
            if len(cur.children) > 1:
                sgfString.append("(")
                level += 1
            elif len(cur.children) == 0:
                sgfString += ")"
                level -= 1
            toParse += reversed(cur.children)
        for _ in range(level):
            sgfString += ")"
        return sgfString
    
class SgfMaker:
    """ Helper class to maintain sgf representation of the game. """


    def __init__(self, size=19, initialPosition=[]):
        self.header = "(;FF[4]GM[1]SZ[%d]" % size
        # self.level = 1
        self.initPos = initialPosition
        self.root = None
        self.current = None
        self.makeSgf()
        self.nMoves = len(initialPosition)
        self.pendingVariations = []
        
    def addMove(self, pos, color):
        # Add a new node after the current active one
        posStr = coordsToStr(pos)
        newNode = Node(color, posStr, self.nMoves + 1)
        if self.current is None:
            self.current = self.root = newNode
        else:
            self.current = self.current.addChild(newNode)
        self.nMoves += 1
        
        # Update the string representation
        self.sgfString += ";" + self.current.toString()
        
        # Add any pending variation
        for pending in self.pendingVariations:
            pending[1].addChild(pending[0])
        
    def findNode(self, moveNumber):
        """ Find the node corresponding to the given move number in the current branch. """
        current = self.current
        while current.moveNumber > moveNumber:
            current = current.prev
        return current
        
    def addVariation(self, moves, fromMoveNumber):
        """ Adds a variation to the current branch at the given move number. """
        # Find the move from which the variation begins
        pending = False
        if fromMoveNumber >= self.nMoves:
            variationRoot = self.current
            pending = True
        else:
            variationRoot = self.findNode(fromMoveNumber)
        if variationRoot is None:
            # Supposedly because the board wasn't played one move at a time but was setup all at once
            variationRoot = Node(0, "dummy node", fromMoveNumber)
            variationRoot.type = "C"
            if self.root is None:
                self.root = self.current = variationRoot
            else: #FIXME what is this for ?
                variationRoot.addChild(self.root)
                self.root = variationRoot
            
        variationNode = self.addVariationFromNode(moves, variationRoot, pending)
        return variationNode
        
    def addVariationFromNode(self, moves, fromNode, pending=False):
        """ Adds a variation from the given node. """
        # Make a branch for the variation
        move = moves[0]
        coords = coordsToStr(move[0])
        variationBegin = Node(move[1], coords, fromNode.moveNumber + 1, "1")
        current = variationBegin
        markup = ["%s:%d" % (coords, 1)]
        for i in range(1, len(moves)):
            move = moves[i]
            coords =  coordsToStr(move[0])
            markup.append("%s:%d" % (coords, i+1))
            markupString = "][".join(markup)
            current = current.addChild( Node(move[1], coords, fromNode.moveNumber + 1 + i, markupString) )
            trace(markupString)
        
        if pending:
            variationBegin.prev = fromNode # Don't link it to the sgf right away because it might cause issues when updating the live game
            self.pendingVariations.append( (variationBegin, fromNode) )
        else:
            fromNode.addChild(variationBegin)
        return current
        
    def sgfForInitialPosition(self):
        sgfString = ""
        for move in self.initPos:
            pos, color = move
            if color == COLOR_BLACK:
                sgfString += ";AB[%s]" % coordsToStr(pos)
            else:
                sgfString += ";AW[%s]" % coordsToStr(pos)
        return sgfString
    
    def makeSgf(self):
        """ Creates the sgf for the complete tree """
        self.sgfString = self.header + self.sgfForInitialPosition()
        
        if self.root is not None:
            self.sgfString += self.root.sgfTree()
        
class Game:
    """ Internal representation of the state of a game of of Go. This is the class you are supposed to interact with. """
    
    def __init__(self, capture=None):
        self.reset(capture)
        self.variations = []
        self.nextvariationIndex = 0
        
    def reset(self, capture=None):
        if capture is None:
            self.state = SgfMaker()
            self.nextToPlay = COLOR_BLACK
            self.lastCapture = []
            for _ in range(19):
                col = []
                for _ in range(19):
                    col.append(0)
                self.lastCapture.append(col)
        else:
            # Parse the image to get the initial position
            initPos = []
            for i in range(19):
                trace("i : %d" % i, 3)
                for j in range(19):
                    trace("j : %d" % j, 3)
                    color = capture[i][j]
                    if color != 0:
                        initPos.append( ((i, j), color) )
            self.state = SgfMaker(initialPosition = initPos)
            self.nextToPlay = 0
            self.lastCapture = capture
    
    def nextPlayer(self):
        return self.nextToPlay if self.nextToPlay != 0 else COLOR_BLACK
    
    def updateGame(self, capture):
        newMoves = []
        for i in range(19):
            for j in range(19):
                color = capture[i][j]
                if color != self.lastCapture[i][j]:
                    if color == 0:
                        trace("Warning : too many moves were played before last update, resetting game", 0)
                        self.reset(capture)
                        trace("Game reset complete", 0)
                        return
                    newMoves.append( ((i, j), color) )
        if len(newMoves) == 0:
            return
        elif len(newMoves) > 2:
            trace("Warning : too many moves were played before last update, resetting game", 0)
            self.reset(capture)
            trace("Game reset complete", 0)
        elif len(newMoves) == 1:
            pos, color = newMoves[0]
            self.addMove(pos, color)
        else:
            knowWhoPlaysNext = True
            if self.nextToPlay == 0:
                knowWhoPlaysNext = False
            firstMove = newMoves[0]
            secondMove = newMoves[1]
            if self.nextToPlay == secondMove[1]:
                tmp = firstMove
                firstMove = secondMove
                secondMove = tmp
            self.addMove(firstMove[0], firstMove[1])
            self.addMove(secondMove[0], secondMove[1])
            if not knowWhoPlaysNext:
                self.nextToPlay = 0
        self.lastCapture = capture
    
    def addMove(self, move, color):
        self.state.addMove(move, color)
        self.nextToPlay = otherColor(color)
    
    def addVariation(self, moves, fromMoveNumber=9999):
        nMovesVariation = len(moves)
        self.variations.append( (self.state.addVariation(moves, fromMoveNumber), nMovesVariation) )
        self.nextvariationIndex += 1
        return self.nextvariationIndex - 1
    
    def expandVariation(self, moves, variationIndex):
        variationNode = self.getVariation(variationIndex)
        self.state.addVariationFromNode(variationNode)
        return variationIndex
        
    def getVariation(self, variationIndex):
        variation, nMoves = self.variations[variationIndex]
        return (self.state.header + self.state.sgfForInitialPosition() + variation.sgfToNode() + ")", nMoves)
    
    def getSgf(self):
        return self.state.sgfString + ")"
