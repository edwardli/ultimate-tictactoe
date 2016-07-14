import models
import constants

game = models.BigBoard()
print 'Welcome to Ultimate Tic-Tac-Toe! X goes first. Denote moves' \
      'with two ordered pairs; the first denotes the small square,' \
      'and the second denotes the position within that square.\n\n' \
      'Example move: (1,1),(1,1)'

while not game.getState(): # game ongoing
    print game
    move = raw_input('Enter your move: ')
    try:
        board = (int(move[1]),int(move[3]))
        position = (int(move[7]),int(move[9]))
    except:
        board = (3,3)
        position = (3,3)

    while game.makeMove(board,position) == constants.ILLEGAL_MOVE:
        move = raw_input('Illegal move. Try again: ')
        try:
            board = (int(move[1]), int(move[3]))
            position = (int(move[7]), int(move[9]))
        except:
            board = (3, 3)
            position = (3, 3)

result = game.getState()

if result == constants.X_WIN:
    print 'X wins!'
elif result == constants.O_WIN:
    print 'O wins!'
else:
    print 'Tie game!'