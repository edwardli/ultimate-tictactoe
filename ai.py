import models
import constants
import time
from math import sqrt, log

class AI(object):
    
    def __init__(self, board, side = constants.O, timeLimit = 10000, searchDepth = -1):
        self.board = board
        self.side = side
        self.timeLimit = timeLimit
        self.searchDepth = searchDepth
        
    def getNextMove(self):
        self.weights = {}
        curr = int(time.time() * 1000)
        stop = curr + self.timeLimit
        simNum = 0
        while curr < stop:
            self.board.backUp()
            moveList, outcome = self.simulateOnce(simNum)
            self.updateWeights(moveList, outcome)
            self.board.restore()
            curr = int(time.time() * 1000)
            simNum += 1
        
        bestVal = 0
        for move in self.board.getLegalMoves():
            moveKey = (move[0], move[1], self.board.getMoveNum() + 1)
            if moveKey in self.weights:
                moveVal = float(self.weights[moveKey][0])/ self.weights[moveKey][1]
                if moveVal > bestVal:
                    bestMove = move
                    bestVal = moveVal
        print "AI Move:(" + str(bestMove[0]) + "," + str(bestMove[1]) + ")\nAI Estimated Win Chance: " + str(bestVal)
        print self.board.evaluateBoard()
        return bestMove
    
    def simulateOnce(self, simulationNum):
        depth = self.searchDepth
        board = self.board
        moveList = []
        t = simulationNum + 1 #number of simulations run on parent node
        c = 2 #constant multiplier for expansion term
        
        while depth and (not board.getState()):
            moveOptions = board.getLegalMoves()
            moveNum = board.getMoveNum() + 1
            
            bestValue = float('-inf')
            for move in moveOptions:
                moveKey = (move[0], move[1], moveNum)
                if moveKey in self.weights:
                    exploitation = float(self.weights[moveKey][0])/self.weights[moveKey][1]
                    if board.getTurn() != self.side:
                        exploitation = 1 - exploitation
                    expansion = sqrt(c * log(t) / self.weights[moveKey][1])
                else:
                    exploitation = 0.5
                    expansion = sqrt(c * log(t))
                
                moveValue = exploitation + expansion
                if moveValue > bestValue:
                    bestValue = moveValue
                    bestMove = move
            board.makeMove(bestMove)
            bestMoveKey = (bestMove[0], bestMove[1], board.getMoveNum())
            moveList.append(bestMoveKey)
            depth -= 1
            if bestMoveKey in self.weights:
                t = self.weights[bestMoveKey][1] + 1
            else:
                t = 1
        
        if not board.getState():
            outcome = board.evaluateBoard()
        elif board.getState() == constants.TIE:
            outcome = .5
        elif board.getState() == constants.X_WIN:
            outcome = 0
        elif board.getState() == constants.O_WIN:
            outcome = 1
            
        return (moveList, outcome if self.side == constants.O else 1 - outcome)
    
    def updateWeights(self, moveList, outcome):
        for move in moveList:
            if move in self.weights:
                oldWeight = self.weights[move]
                self.weights[move] = (oldWeight[0] + outcome, oldWeight[1] + 1)
            else:
                self.weights[move] = (outcome, 1)