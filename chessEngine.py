import chess
from time import time
from math import inf
import chess.polyglot


# Parameters will be implemented soon
bias = 10
bPawnTable = [0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]
wPawnTable = bPawnTable[::-1]
bKnightTable = [-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]
wKnightTable = bKnightTable[::-1]
bBishopTable = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20]
wBishopTable = bBishopTable[::-1]
bRookTable = [0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]
wRookTable = bRookTable[::-1]
bQueenTable = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]
wQueenTable = bQueenTable[::-1]

# Simple Evaluation Function
def evaluateBoard(board):
        evaluation = 0
        pieces = board.pieces
        # Get all pieces
        white_pawns = pieces(1, True)
        black_pawns = pieces(1, False)
        white_knights = pieces(2, True)
        black_knights = pieces(2, False)
        white_bishops = pieces(3, True)
        black_bishops = pieces(3, False)
        white_rooks = pieces(4, True)
        black_rooks = pieces(4, False)
        white_queens = pieces(5, True)
        black_queens = pieces(5, False)
        white_king = pieces(6, True)
        black_king = pieces(6, False)
        # Calculate Material Advantage (centipawns)
        evaluation += sum(map(lambda x: wPawnTable[x], white_pawns)) - sum(map(lambda x: bPawnTable[x], black_pawns))
        evaluation += sum(map(lambda x: wKnightTable[x], white_knights)) - sum(map(lambda x: bKnightTable[x], black_knights))
        evaluation += sum(map(lambda x: wBishopTable[x], white_bishops)) - sum(map(lambda x: bBishopTable[x], black_bishops))
        evaluation += sum(map(lambda x: wRookTable[x], white_rooks)) - sum(map(lambda x: bRookTable[x], black_rooks))
        evaluation += sum(map(lambda x: wQueenTable[x], white_queens)) - sum(map(lambda x: bQueenTable[x], black_queens))
        evaluation += 100*(len(white_pawns) - len(black_pawns)) + 310*(len(white_knights) - len(black_knights)) + 320*(len(white_bishops) - len(black_bishops)) + 500*(len(white_rooks) - len(black_rooks)) + 900*(len(white_queens) - len(black_queens)) + 20000*(len(black_king) - len(white_king))
        return evaluation

def negaMaxRoot(board, depth, alpha, beta, color):
    global positions
    positions += 1
    value = -inf
    moves = board.generate_legal_moves()
    bestMove = next(moves)
    for move in moves:
        board.push(move)
        boardValue = -1 * negaMax(board, depth - 1, -1 * beta, -1 * alpha, -1 * color)
        board.pop()
        if boardValue > value:
            value = boardValue
            bestMove = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return bestMove, value

def negaMax(board, depth, alpha, beta, color):
    global positions
    positions += 1
    if depth == 0:
        return color * evaluateBoard(board)
    value = -inf
    moves = board.generate_legal_moves()
    for move in moves:
        board.push(move)
        value = max(value, -1 * negaMax(board, depth - 1, -1 * beta, -1 * alpha, -1 * color))
        board.pop()
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value

def move(board, depth, color):
    global positions
    positions = 0
    try:
        reader = chess.polyglot.open_reader('book\\book.bin')
    except FileNotFoundError:
        bestMove, value = negaMaxRoot(board, depth, -inf, inf, color)
        return bestMove, value, 0
    try:
        return reader.weighted_choice(board).move, 0, 1
    except IndexError:
        bestMove, value = negaMaxRoot(board, depth, -inf, inf, color)
        return bestMove, value, 0

def play():
    global board
    fen = input('FEN?')
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    print(board)
    if input('Play?') == 'y':
        depth = int(input('Difficulty Level (Search Depth) (Don\'t go over 5 yet): '))
        while not board.is_game_over():
            user_input = input('Make Move (or type e to export the FEN of the position): ')
            if user_input.lower() == 'e':
                print(board.fen())
            try:
                board.push_uci(user_input)
            except ValueError:
                continue
            print(board)
            start = time()
            computerMove, score, book = move(board, depth, -1)
            elapsed = time() - start
            print('best move is ' + str(computerMove))
            if not book:
                print('Position advantage is calclulated as: ' + str(score) + ' (from ' + str(positions) + ' positions at '+ str(int(positions // elapsed)) +' pos/s)')
            board.push(computerMove)
            print(board)

def analyze():
    global board
    fen = input('FEN?')
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    print(board)
    if input('Analyze?') == 'y':
        depth = int(input('Search Depth (Don\'t go over 5 yet): '))
        while not board.is_game_over():
            if board.turn:
                start = time()
                computerMove, score, book = move(board, depth, 1)
                elapsed = time() - start
                print('best move is ' + str(computerMove))
                if not book:
                    print('Position advantage is calclulated as: ' + str(score) + ' (from ' + str(positions) + ' positions at '+ str(int(positions // elapsed)) +' pos/s)')
                user_input = input('Make Move (or type e to export the FEN of the position): ')
                if user_input.lower() == 'e':
                    print(board.fen())
                try:
                    board.push_uci(user_input)
                except ValueError:
                    continue
                print(board)
            else:
                start = time()
                computerMove, score, book = move(board, depth, -1)
                elapsed = time() - start
                print('best move is ' + str(computerMove))
                if not book:
                    print('Position advantage is calclulated as: ' + str(score) + ' (from ' + str(positions) + ' positions at '+ str(int(positions // elapsed)) +' pos/s)')
                user_input = input('Make Move (or type e to export the FEN of the position): ')
                if user_input.lower() == 'e':
                    print(board.fen())
                try:
                    board.push_uci(user_input)
                except ValueError:
                    continue
                print(board)

def play_itself(fen=''):
    global board
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    if input('play?') == 'y':
        depth = int(input('Search Depth (Don\'t go over 5 yet): '))
        movesToPlay = int(input('# of moves for each computer to play (type 0 for continuous play): ')) * 2
        print(board.move_stack)
        while (not board.is_game_over()) and (movesToPlay > len(board.move_stack) or movesToPlay == 0):
            start = time()
            if board.turn:
                computerMove, score, book = move(board, depth, 1)
            else:
                computerMove, score, book = move(board, depth, -1)
            elapsed = time() - start
            print('best move is ' + str(computerMove))
            if not book:
                print('Position advantage is calclulated as: ' + str(score) + ' (from ' + str(positions) + ' positions at '+ str(int(positions // elapsed)) +' pos/s)')
            board.push(computerMove)
            print(board)
