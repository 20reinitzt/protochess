import chess
from time import time
from math import inf, isnan
import chess.polyglot


# Parameters will be implemented soon

# piece square tables
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

# loading opening book reader
try:
    reader = chess.polyglot.open_reader('book\\book.bin')
except FileNotFoundError:
    print('No opening book found. make sure you have it in the right folder (path should be ..\\book.bin)')

# Simple Evaluation Function
def evaluateBoard(board, depth):
    evaluation = 5 # setting bias to 5 to try and avoid draws
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
    # Calculate Material Advantage (centipawns)
    # mapping pieces to piece-square tables
    evaluation += sum(map(lambda x: wPawnTable[x], white_pawns)) - sum(map(lambda x: bPawnTable[x], black_pawns))
    evaluation += sum(map(lambda x: wKnightTable[x], white_knights)) - sum(map(lambda x: bKnightTable[x], black_knights))
    evaluation += sum(map(lambda x: wBishopTable[x], white_bishops)) - sum(map(lambda x: bBishopTable[x], black_bishops))
    evaluation += sum(map(lambda x: wRookTable[x], white_rooks)) - sum(map(lambda x: bRookTable[x], black_rooks))
    evaluation += sum(map(lambda x: wQueenTable[x], white_queens)) - sum(map(lambda x: bQueenTable[x], black_queens))
    # calculating material advantage
    evaluation += 100*(len(white_pawns) - len(black_pawns)) + 310*(len(white_knights) - len(black_knights)) + 320*(len(white_bishops) - len(black_bishops)) + 500*(len(white_rooks) - len(black_rooks)) + 900*(len(white_queens) - len(black_queens))
    return evaluation

# Nega Max Root Call
def negaMaxRoot(board, depth, alpha, beta, color, maxDepth):
    global positions
    positions += 1
    value = -inf
    moves = board.generate_legal_moves()
    bestMove = next(moves)
    for move in moves:
        board.push(move)
        boardValue = -1 * negaMax(board, depth - 1, -beta, -alpha, -color, maxDepth)
        board.pop()
        if boardValue > value:
            value = boardValue
            bestMove = move
        # implementing alpha-beta cutoff
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return bestMove, value

# Nega Max Child Call
def negaMax(board, depth, alpha, beta, color, maxDepth):
    global positions
    positions += 1
   # draw and mate checking (values shallow mates more than deeper ones)
    if board.is_fivefold_repetition() or board.is_stalemate() or board.is_seventyfive_moves():
        return 0
    if board.is_checkmate():
        return color * (1 - (0.01*(maxDepth - depth))) * -99999 if board.turn else color * (1 - (0.01*(maxDepth - depth))) * 99999
    # testing for 'noisy' positions, and quiescence searching them for Horizon effect mitigation
    if depth == 0:
        if board.is_capture(board.peek()):
            return qSearch(board, -inf, inf, color, maxDepth)
        return color * evaluateBoard(board)
    value = -inf
    moves = board.generate_legal_moves()
    for move in moves:
        board.push(move)
        value = max(value, -1 * negaMax(board, depth - 1, -beta, -alpha, -color, maxDepth))
        board.pop()
        # implementing alpha-beta cutoff
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value

# starting the quiescence search code (only searches up to 3 ply extra from captures (any more and it runs slooooowwwwww))
def qSearch(board, alpha, beta, color, startingDepth, depth=1, maxDepth=3):
    global positions
    positions += 1
    # mate test (values shallow mates more than deeper ones)
    if board.is_checkmate():
        return color * (1 - (0.01*(maxDepth + depth))) * -99999 if board.turn else color * (1 - (0.01*(maxDepth + depth))) * 99999
    # get stand-pat for delta pruning
    value = color * evaluateBoard(board, depth)
    # alpha-beta cutoffs
    if value >= beta:
        return beta
    if alpha < value:
        alpha = value
    if depth <= maxDepth:
        captureMoves = (move for move in board.generate_legal_moves() if board.is_capture(move))
        for move in captureMoves:
            board.push(move)
            score = -1 * qSearch(board, -beta, -alpha, -color, depth + 1, maxDepth)
            board.pop()
            # more alpha-beta cutoffs
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

def move(board, depth, color):
    global positions
    positions = 0
    # implementing the opening book + move analysis functions
    if reader:
        try:
            return reader.weighted_choice(board).move, 0, 1
        except IndexError:
            bestMove, value = negaMaxRoot(board, depth, -inf, inf, color, depth)
            return bestMove, value, 0
    bestMove, value = negaMaxRoot(board, depth, -inf, inf, color, depth)
    return bestMove, value, 0

# calculates how many moves before computer sees mate
def mateInXMoves(score):
    # uses the score to calculate the depth of mate
    half_moves_to_mate = -(abs(score) - 99999) // (999.99)
    if not isnan(half_moves_to_mate):
        moves_to_mate = int((half_moves_to_mate  - 1) // 2) + 1
        if (board.turn and score > 0) or (not board.turn and score < 0):
            sideMated = 'white'
        else:
            sideMated = 'black'
        score = 'Mate in {} for {}'.format(str(moves_to_mate), sideMated)
    return score

# allows the computer to play as either white or black
def makeMove(colorToPlay, playerColor):
    if colorToPlay == (playerColor == 'w'):
    user_input = input('Make Move (or type e to export the FEN of the position): ')
        if user_input.lower() == 'e':
            print(board.fen())
    board.push_uci(user_input)
    else:
        start = time()
        computerMove, score, book = move(board, depth, -1)
        elapsed = time() - start
        print('best move is ' + str(computerMove))
        if score > 50000 or score < -50000:
            score = mateInXMoves(score)
        if not book:
            print('Position advantage is calclulated as: ' + str(score) + ' (from ' + str(positions) + ' positions at '+ str(int(positions // max(elapsed, 0.0001))) +' pos/s)')
        board.push(computerMove)
        

def play(fen=''):
    global board
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    print(board)
    depth = int(input('Difficulty Level (Search Depth) (Don\'t go over 5 yet): '))
    playerColor = input('play as (w)hite or (b)lack? ')[0].lower()
    while not board.is_game_over():
        try:
            makeMove(board.turn, playerColor)
        except ValueError:
            continue
        print(board)
    print('Game Over! Result: {}'.format(board.result()))

def analyze(fen=''):
    global board
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    print(board)
    depth = int(input('Search Depth (Don\'t go over 5 yet): '))
    while not board.is_game_over():
        start = time()
        if board.turn:
            computerMove, score, book = move(board, depth, 1)
        else:
            computerMove, score, book = move(board, depth, -1)
        elapsed = time() - start
        print('best move is ' + str(computerMove))
        if score > 50000 or score < -50000:
            score = mateInXMoves(score)
        if not book:
            print('Position advantage is calclulated as: ' + str(score) + ' (from ' + str(positions) + ' positions at '+ str(int(positions // max(elapsed, 0.0001))) +' pos/s)')
        user_input = input('Make Move (or type e to export the FEN of the position, or a to analyze another position): ')
        if user_input.lower() == 'e':
            print(board.fen())
        if user_input.lower() =='a':
            analyze(input('fen? '))
        try:
            board.push_uci(user_input)
        except ValueError:
            continue
        print(board)
    print('Game Over! Result: {}'.format(board.result()))

def play_itself(fen=''):
    global board
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    depth = int(input('Search Depth (Don\'t go over 5 yet): '))
    movesToPlay = int(input('# of moves for each computer to play (type 0 for continuous play): ')) * 2
    while (not board.is_game_over()) and (movesToPlay > len(board.move_stack) or movesToPlay == 0):
        start = time()
        if board.turn:
            computerMove, score, book = move(board, depth, 1)
        else:
            computerMove, score, book = move(board, depth, -1)
        elapsed = time() - start
        print('best move is ' + str(computerMove))
        if score > 50000 or score < -50000:
            score = mateInXMoves(score)
        if not book:
            print('Position advantage is calclulated as: ' + str(score) + ' (from ' + str(positions) + ' positions at '+ str(int(positions // max(elapsed, 0.0001))) +' pos/s)')
        board.push(computerMove)
        print(board)
    if board.is_game_over():
        print('Game Over! Result: {}'.format(board.result()))
    else:
        print('completed {} half-moves, program complete.'.format(len(board.move_stack)))
