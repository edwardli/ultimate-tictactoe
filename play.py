import constants
from models import BigBoard
from sys import argv
from ai import AI

def main(args):
    gameType = args[1] if len(args) > 1 else constants.NO_AI
    game = BigBoard()
    ai = AI(game)
    print 'Welcome to Ultimate Tic-Tac-Toe! X goes first. Denote moves ' \
          'with an ordered pair (row, col) where the top left is (0,0)\n\n' \
          'Example move: 4,4'
    
    if gameType == constants.TWO_AI:
        pass
    else:
        print game
        while not game.getState(): # game ongoing
            move = raw_input('Enter your move: ')
            try:
                coords = (int(move[0]),int(move[2]))
            except:
                coords = (9,9)
            if game.makeMove(coords) == constants.ILLEGAL_MOVE:
                print 'Illegal move. Try again: '
            else:
                print game
                if gameType == constants.ONE_AI and not game.getState():
                    game.makeMove(ai.getNextMove())
                    print game
        
        result = game.getState()
        if result == constants.X_WIN:
            print 'X wins!'
        elif result == constants.O_WIN:
            print 'O wins!'
        else:
            print 'Tie game!'
            
main(argv)