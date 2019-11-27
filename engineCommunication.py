import chess
from time import time
from math import inf, isnan
import chess.polyglot
from protochessOOP import Engine

# Calculates how many moves before computer sees mate
def mateInXMoves(board, score):
    # uses the move score to calculate the depth to mate
    half_moves_to_mate = (-(abs(score) - 99999) // (999.99))
    if not isnan(half_moves_to_mate):
        moves_to_mate = int((half_moves_to_mate  - 1) // 2) + 1
        if (board.turn and score > 0) or (not board.turn and score < 0):
            sideMated = 'white'
        else:
            sideMated = 'black'
        score = 'Mate in {} for {}'.format(str(moves_to_mate), sideMated)
    return score

# Allows engines of differing depths to play themselves
def playEngines(engine1Depth, engine2Depth, fen='', printBoard=True):
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    engine1 = Engine(engine1Depth, 1, board)
    engine2 = Engine(engine2Depth, -1, board)
    movesToPlay = int(input('# of moves for each computer to play (type 0 for continuous play): ')) * 2
    if printBoard:
        print(board)
    while (not board.is_game_over()) and (movesToPlay > len(board.move_stack) or movesToPlay == 0):
        if board.turn:
            computerMove, value, book, timeTaken, positions, positionsPerSecond = engine1.moveWithStats()
        else:
            computerMove, value, book, timeTaken, positions, positionsPerSecond = engine2.moveWithStats()
        if abs(value) > 50000:
            value = mateInXMoves(board, value)
            print('Best Move is: {} \nPositon advantage is calculated as {} from {} positions in {} seconds ({} pos/s)'.format(computerMove, value, positions, timeTaken, positionsPerSecond))
        else:
            if not book:
                print('Best Move is: {}\nPosition advantage is calclulated as: {} for {} from {} positions in {} seconds ({} pos/s)'.format(computerMove, value, 'white' if board.turn else 'black', positions, timeTaken, positionsPerSecond))
            else:
                print('Best Move is: {} (Book Move)'.format(computerMove))
        board.push(computerMove)
        engine1.updateBoard(board)
        engine2.updateBoard(board)
        if printBoard:
            print(board)
    if board.is_game_over():
        print('Game Over! Result: {}'.format(board.result()))
    else:
        print('Finished {} half moves. program terminated'.format(len(board.move_stack)))

def playAgainstEngine(engineDepth, fen='', printBoard=True):
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    playerColor = input('What color would you like to play as? (w)hite or (b)lack? ')
    if playerColor.lower()[0] == 'w':
        playerColor = 1
    else:
        playerColor = -1
    engine1 = Engine(engineDepth, -playerColor, board)
    while not board.is_game_over():
        if board.turn == (playerColor == 1):
            user_input = input('Make Move (or type e to export the FEN of the position): ')
            if user_input.lower() == 'e':
                print('Board FEN: {}'.format(board.fen()))
            try:
                board.push_uci(user_input)
                print('Player move: {}'.format(user_input))
                if printBoard:
                    print(board)
                engine1.updateBoard(board)
            except ValueError:
                continue
        else:
            computerMove, value, book, timeTaken, positions, positionsPerSecond = engine1.moveWithStats()
            if abs(value) > 50000:
                value = mateInXMoves(board, value)
                print('Best Move is: {} \nPositon advantage is calculated as {} from {} positions in {} seconds ({} pos/s)'.format(computerMove, value, positions, timeTaken, positionsPerSecond))
            else:
                if not book:
                    print('Best Move is: {}\nPosition advantage is calclulated as: {} for {} from {} positions in {} seconds ({} pos/s)'.format(computerMove, value, 'white' if board.turn else 'black', positions, timeTaken, positionsPerSecond))
                else:
                    print('Best Move is: {} (Book Move)'.format(computerMove))
            board.push(computerMove)
            engine1.updateBoard(board)
            if printBoard:
                print(board)
    print('Game Over! Result: {}'.format(board.result()))
            
