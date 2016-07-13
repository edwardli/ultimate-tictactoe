import constants
from operator import methodcaller

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
        return (self.asciifyRow(0)+'\n'+
                self.asciifyRow(1)+'\n'+
                self.asciifyRow(2))

    def asciifyRow(self, x):
        """
        :param x: The x-coordinate of this row.
        :return: An ascii representation of row x.
        """
        result = '|'
        for square in self._board[x]:
            if square == 1:
                result += 'X|'
            elif square == -1:
                result += 'O|'
            else:
                result += ' |'
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
        assert (type(coords) == tuple and len(coords) == 2 and type(coords[0]) == int and type(coords[1]) == int), 'invalid coords'
        assert (0 <= coords[0] and coords[0] <= 2 and 0 <= coords[1] and coords[1] <= 2), 'invalid coords'

        x, y = coords
        if self._board[x][y] or self._state != constants.ONGOING:
            return constants.ILLEGAL_MOVE

        self._board[x][y] = side
        self.updateState()
        return self._state


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
        cols = [ # flipped orientation
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]

        for x in range(3):
            rowsum = sum(self._board[x])
            if rowsum == 3 or rowsum == -3:
                self._state = rowsum / 3
                return
            for y in range(3):
                square = self._board[x][y]
                cols[y][x] = square
                if not square: # square == 0
                    nospace = False

        for col in cols:
            colsum = sum(col)
            if colsum == 3 or colsum == -3:
                self._state = colsum/3
                return

        # tie or ongoing, depending on whether there is space left
        if nospace:
            self._state = constants.TIE
            return
        else:
            self._state = constants.ONGOING
            return

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
        self._board = [
            [SmallBoard(), SmallBoard(), SmallBoard()],
            [SmallBoard(), SmallBoard(), SmallBoard()],
            [SmallBoard(), SmallBoard(), SmallBoard()]
        ]
        self._turn = first
        self._legalboards = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)] # every board is legal
        self._state = constants.ONGOING

    def __repr__(self):
        r = '-----------------------------\n'
        for row in self._board:
            for line in range(3):
                r += ' '+row[0].asciifyRow(line)+' $ '+row[1].asciifyRow(line)+' $ '+row[2].asciifyRow(line) +' \n'
            r += '-----------------------------\n'

        return r



    def makeMove(self, boardcoords, squarecoords):
        """
        Makes a move for the player whose turn it is.
        :param boardoords: 2-tuple of ints, coordinates of the small board targeted.
        :param squarecoords: 2-tuple of ints, coordinates of the square targeted within the small box.
        :param s: The side to play.
        :return: The game state after a move is made, or an illegal move code.
        """
        if boardcoords not in self._legalboards or self._state != constants.ONGOING:
            return constants.ILLEGAL_MOVE

        smallresult = self._board[boardcoords[0]][boardcoords[1]].makeMove(squarecoords, self._turn)
        if smallresult == constants.ILLEGAL_MOVE:
            return constants.ILLEGAL_MOVE

        self._updateState(squarecoords)
        return self._state

    def _updateState(self, squarecoords):
        """
        Updates state, legalboards and turn after a move. Should ONLY be called in conjunction with a move, hence hidden.
        :param squarecords: The small square coordinates of the move just made.
        """
        self._turn *= -1 # switch the turn to the other side
        del self._legalboards[:] # clear the legal boards in preparation for game end or new set of boards.

        # check diagonals
        diag1 = self._board[0][0].getState() + self._board[1][1].getState() + self._board[2][2].getState()
        diag2 = self._board[0][2].getState() + self._board[1][1].getState() + self._board[2][0].getState()
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
            rowsum = sum(map(methodcaller('getState'), self._board[x])) # call getState statically on all small boards
            if rowsum == 3 or rowsum == -3:
                self._state = rowsum / 3
                return
            for y in range(3):
                board = self._board[x][y].getState()
                cols[y][x] = board
                if not board:  # board == 0
                    nospace = False

        for col in cols: # these are all integers, NOT SmallBoard objects
            colsum = sum(col)
            if colsum == 3 or colsum == -3:
                self._state = colsum / 3
                return

        # tie or ongoing, depending on whether there is space left
        if nospace:
            self._state = constants.TIE
            return

        # ongoing if we got this far
        if not self._board[squarecoords[0]][squarecoords[1]].getState(): # target board is still going
            self._legalboards.append(squarecoords) # only add that one board
            return

        for x in range(3):
            for y in range(3):
                if not self._board[x][y].getState(): # the board is ongoing, so it's a legal board
                    self._legalboards.append((x,y))
        return