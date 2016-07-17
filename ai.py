import models
import constants

class AI(object):
    """
    An AI implementing the minimax algorithm.

    Attributes:
        _game: The BigBoard object representing the game.
        _gameTree: Used for the minimax tree expansion of this game.
    """
    def __init__(self, game):
        self._game = game
        self._gameTree = None

    def getNextMove(self):
        self._gameTree = GameNode(self._game, self._game.getTurn())
        self._gameTree.expandUpTo(constants.DEPTH)
        bestIndex = -1
        bestValue = -1
        gameChoices = self._gameTree.children
        for index in xrange(len(gameChoices)):
            value = gameChoices[index].minimax(False)
            if value > bestValue:
                bestValue = value
                bestIndex = index
        return self._game.getLegalMoves()[bestIndex]




class GameNode(object):
    """Like a game, but can act as a tree."""
    def __init__(self, game, side):
        self.side = side
        self.game = game
        self.children = []

    def expandUpTo(self, depth):
        if depth <= 0:
            return

        for move in self.game.getLegalMoves():
            self.game.backUp()
            self.game.makeMove(move)
            self.children.append(GameNode(self.game.makeCopy(), self.side))
            self.game.restore()

        for child in self.children:
            child.expandUpTo(depth-1)

    def minimax(self, maxPlayer): # credits to wikipedia article for minimax for the pseudocode
        if len(self.children) == 0:
            return self.evaluate()

        if maxPlayer:
            bestValue = -2
            for child in self.children:
                value = child.minimax(False)
                bestValue = max(bestValue, value)
            return bestValue

        else:
            bestValue = 2
            for child in self.children:
                value = child.minimax(True)
                bestValue = min(bestValue, value)
            return bestValue


    def evaluate(self):
        state = self.game.getState()
        if state == self.side:
            return 1
        elif state == self.side * -1:
            return -1
        else:
            advantage = 0
            disadvantage = 0
            won = 0
            lost = 0
            tie = 0
            for smallboard in self.game._board:
                if smallboard.getState() == self.side:
                    won += 1
                elif smallboard.getState() == self.side * -1:
                    lost += 1
                elif smallboard.getState() == constants.TIE:
                    tie += 1
                else:
                    friendly = 0
                    enemy = 0
                    for row in smallboard.getBoard():
                        for pos in row:
                            if pos == friendly:
                                friendly += 1
                            elif pos == enemy:
                                enemy += 1
                    if friendly > enemy:
                        advantage += 1
                    elif friendly < enemy:
                        disadvantage += 1
                    else:
                        tie += 1
            return 0.05*advantage - 0.05*disadvantage + 0.1*won - 0.1*lost