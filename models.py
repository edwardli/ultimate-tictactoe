import constants
from copy import deepcopy


class SmallBoard(object):
    """
    Represents a 3x3 board.
    Note x varies vertically and y varies horizontally.
    """

    def __init__(self):
        """Initializer."""
        self._board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self._state = constants.ONGOING

    def __repr__(self):
        """Representation function."""
        return (self.asciifyRow(0) + '\n' +
                self.asciifyRow(1) + '\n' +
                self.asciifyRow(2))

    def asciifyRow(self, x):
        """
        :param x: The x-coordinate of this row.
        :return: An ascii representation of row x.
        """
        result = ' '
        for square in self._board[x]:
            if square == 1:
                result += 'X '
            elif square == -1:
                result += 'O '
            else:
                result += '  '
        return result

    def makeMove(self, coords, side):
        """
        Makes a move.
        :param side: constants.O or constants.X
        :param coords: ordered pair. The coordinates of square to move to. Upper left square is (0,0).
                        Lower left is (2,0).
        :return: a move type defined in constants. Integer.
        """
        assert (side == 1 or side == -1), 'invalid side'
        assert (type(coords) == tuple and len(coords) == 2 and type(coords[0]) == int and type(
            coords[1]) == int), 'invalid coords'
        assert (0 <= coords[0] and coords[0] <= 2 and 0 <= coords[1] and coords[1] <= 2), 'invalid coords'

        x, y = coords
        if self._board[x][y] or self._state != constants.ONGOING:
            return constants.ILLEGAL_MOVE

        self._board[x][y] = side
        self.updateState()
        return self._state

    def getLegalMoves(self, rowOffset=0, colOffset=0):
        ret = []
        if not self._state:
            for i in xrange(3):
                for j in xrange(3):
                    if not self._board[i][j]:
                        ret.append((i + rowOffset, j + colOffset))
        return ret

    def updateState(self):
        """
        :return: Win status of this board, defined in constants
        """
        # check diagonals
        diag1 = self._board[0][0] + self._board[1][1] + self._board[2][2]
        diag2 = self._board[0][2] + self._board[1][1] + self._board[2][0]
        if diag1 == 3 or diag1 == -3:
            self._state = diag1 / 3
            return
        if diag2 == 3 or diag2 == -3:
            self._state = diag2 / 3
            return

        # check horizontal and vertical, and check for empty spaces
        nospace = True
        cols = [  # flipped orientation
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for x in range(3):
            rowsum = sum(self._board[x])
            if rowsum == 3 or rowsum == -3:
                self._state = rowsum / 3
                return
            for y in range(3):
                square = self._board[x][y]
                cols[y][x] = square
                if not square:  # square == 0
                    nospace = False

        for col in cols:
            colsum = sum(col)
            if colsum == 3 or colsum == -3:
                self._state = colsum / 3
                return

        # tie or ongoing, depending on whether there is space left
        if nospace:
            self._state = constants.TIE
            return
        else:
            self._state = constants.ONGOING
            return

    def backUp(self):
        self._backUpBoard = deepcopy(self._board)
        self._backUpState = self._state

    def restore(self):
        self._board = self._backUpBoard
        self._state = self._backUpState

    def getBoard(self):
        """
        :return: The ACTUAL board. Do not modify.
        """
        return self._board

    def getState(self):
        """
        :return: The game state.
        """
        return self._state


class BigBoard(object):
    """
    Represents a 9x9 board, or a 3x3 board of 3x3 boards.
    """

    def __init__(self, first=constants.X):
        self._board = [SmallBoard() for x in xrange(0, 9)]
        self._turn = first
        self._legalboards = [x for x in xrange(0, 9)]  # every board is legal
        self._state = constants.ONGOING
        self._moveNum = 0

    def __repr__(self):
        r = '\n'
        board = self._board
        for boardInd in xrange(0, len(board), 3):
            for row in xrange(3):
                r += ' ' + board[boardInd].asciifyRow(row) + ' | ' + board[boardInd + 1].asciifyRow(row) + ' | ' + \
                     board[boardInd + 2].asciifyRow(row) + ' \n'
            r += '-----------------------------\n'

        return r[0:-30]

    def makeMove(self, coords):
        """
        Makes a move for the player whose turn it is.
        :param coords: 2-tuple of ints, coordinates of move
        :return: The game state after a move is made, or an illegal move code.
        """
        smallBoardInd = self.determineSmallBoard(coords)
        squareCoords = (coords[0] % 3, coords[1] % 3)
        if smallBoardInd not in self._legalboards or self._state != constants.ONGOING:
            return constants.ILLEGAL_MOVE

        smallresult = self._board[smallBoardInd].makeMove(squareCoords, self._turn)
        if smallresult == constants.ILLEGAL_MOVE:
            return constants.ILLEGAL_MOVE

        self._updateState(squareCoords)
        self._moveNum += 1
        return self._state

    def _updateState(self, squarecoords):
        """
        Updates state, legalboards and turn after a move. Should ONLY be called in conjunction with a move, hence hidden.
        :param squarecords: The small square coordinates of the move just made.
        """
        board = self._board
        self._turn *= -1  # switch the turn to the other side
        del self._legalboards[:]  # clear the legal boards in preparation for game end or new set of boards.

        # check diagonals
        diag1 = board[0].getState() + board[4].getState() + board[8].getState()
        diag2 = board[2].getState() + board[4].getState() + board[6].getState()
        if diag1 == 3 or diag1 == -3:
            self._state = diag1 / 3
            return
        if diag2 == 3 or diag2 == -3:
            self._state = diag2 / 3
            return

        # check horizontal and vertical, and check for empty spaces
        nospace = True
        for x in xrange(3):
            rowsum = 0
            colsum = 0
            for y in xrange(3):
                boardState = board[3 * x + y].getState()
                rowsum += boardState
                colsum += board[3 * y + x].getState()
                if not boardState:  # board == 0
                    nospace = False
            if rowsum == 3 or rowsum == -3:
                self._state = rowsum / 3
                return
            if colsum == 3 or colsum == -3:
                self._state = colsum / 3
                return

        # tie or ongoing, depending on whether there is space left
        if nospace:
            self._state = constants.TIE
            return

        # ongoing if we got this far
        if not board[3 * squarecoords[0] + squarecoords[1]].getState():  # target board is still going
            self._legalboards.append(3 * squarecoords[0] + squarecoords[1])  # only add that one board
            return

        for x in xrange(len(board)):
            if not board[x].getState():
                self._legalboards.append(x)


    def determineSmallBoard(self, coords):
        return 3 * (coords[0] / 3) + (coords[1] / 3)

    def getLegalMoves(self):
        ret = []
        if not self._state:
            board = self._board
            for boardInd in self._legalboards:
                ret.extend(board[boardInd].getLegalMoves(3 * (boardInd / 3), 3 * (boardInd % 3)))
        return ret

    def backUp(self):
        for board in self._board:
            board.backUp()
        self._backUpTurn = self._turn
        self._backUpLegalBoards = deepcopy(self._legalboards)
        self._backUpState = self._state
        self._backUpMoveNum = self._moveNum

    def restore(self):
        for board in self._board:
            board.restore()
        self._turn = self._backUpTurn
        self._legalboards = self._backUpLegalBoards
        self._state = self._backUpState
        self._moveNum = self._backUpMoveNum

    def getTurn(self):
        return self._turn

    def getMoveNum(self):
        return self._moveNum

    def getLegalBoard(self):
        return self._legalboards

    def getState(self):
        return self._state

    def makeCopy(self):
        newBB = BigBoard()
        newBB._state = self.getState()
        newBB._turn = self.getTurn()
        newBB._legalboards = self.getLegalBoard()
        newBB._moveNum = self.getMoveNum()

        for boardInd in range(len(self._board)):
            newSB = newBB._board[boardInd]
            oldSB = self._board[boardInd]
            newSB._board = deepcopy(oldSB._board)
            newSB._state = oldSB.getState()

        return newBB