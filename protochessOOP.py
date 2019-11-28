import chess
from time import time
from math import inf
import chess.polyglot

# piece square tables (for analysis) (change these to change the engine behavior)
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
bKingTable = [0,  0,  0,  0,  0,  0,  0,  0,
 0,  0,  0,  0,  0,  0,  0,  0,
 0,  0,  0,  0,  0,  0,  0,  0,
 0,  0,  0,  0,  0,  0,  0,  0,
 0,  0,  0,  0,  0,  0,  0,  0,
 0,  0,  0,  0,  0,  0,  0,  0,
20, 20,  0,  0,  0,  0, 20, 20,
20, 30, 10,  0,  0, 10, 30, 20]
wKingTable = bKingTable[::-1]

class Engine(object):

    # initializes all required engine variables
    def __init__(self, depth, color, board, openingBookPath = 'book\\book.bin'):
        self.depth = depth
        self.color = color
        self.board = board
        try:
            self.reader = chess.polyglot.open_reader(openingBookPath)
        except FileNotFoundError:
            self.reader = False
            print('No opening book found. make sure you have the right path')

    # updates the board for the engine
    def updateBoard(self, board):
        self.board = board

    # updates the color the engine is playing as
    def updateColor(self, color):
        self.color = color

    # simple evaluation function
    def evaluateBoard(self, board):
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
        white_kings = pieces(6, True)
        black_kings = pieces(6, False)
        # Calculate Material Advantage (centipawns)
        # mapping pieces to piece-square tables
        evaluation += sum(map(lambda x: wPawnTable[x], white_pawns)) - sum(map(lambda x: bPawnTable[x], black_pawns))
        evaluation += sum(map(lambda x: wKnightTable[x], white_knights)) - sum(map(lambda x: bKnightTable[x], black_knights))
        evaluation += sum(map(lambda x: wBishopTable[x], white_bishops)) - sum(map(lambda x: bBishopTable[x], black_bishops))
        evaluation += sum(map(lambda x: wRookTable[x], white_rooks)) - sum(map(lambda x: bRookTable[x], black_rooks))
        evaluation += sum(map(lambda x: wQueenTable[x], white_queens)) - sum(map(lambda x: bQueenTable[x], black_queens))
        evaluation += sum(map(lambda x: wKingTable[x], white_kings)) - sum(map(lambda x: bKingTable[x], black_kings))
        # calculating material advantage
        evaluation += 100*(len(white_pawns) - len(black_pawns)) + 310*(len(white_knights) - len(black_knights)) + 320*(len(white_bishops) - len(black_bishops)) + 500*(len(white_rooks) - len(black_rooks)) + 900*(len(white_queens) - len(black_queens))
        return evaluation

    # qSearch function (goes up to 4 ply from end depth)
    def qSearch(self, board, alpha, beta, color, startingDepth, depth=0, maxDepth=4):
        global positions
        positions += 1
        # mate test (values shallow mates more than deeper ones)
        if board.is_checkmate():
            return color * (1 - (0.01*(startingDepth + depth))) * -99999 if board.turn else color * (1 - (0.01*(startingDepth + depth))) * 99999
        # get stand-pat for delta pruning
        value = color * self.evaluateBoard(board)
        # alpha-beta cutoffs
        if value >= beta:
            return beta
        if alpha < value:
            alpha = value
        if depth < maxDepth:
            captureMoves = (move for move in board.generate_legal_moves() if (board.is_capture(move) or board.is_check()))
            for move in captureMoves:
                board.push(move)
                score = -1 * self.qSearch(board, -beta, -alpha, -color, depth + 1, maxDepth)
                board.pop()
                # more alpha-beta cutoffs
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    # Nega Max Child Call
    def negaMax(self, board, depth, alpha, beta, color, maxDepth):
        global positions
        positions += 1
        moveEvals = []
       # draw and mate checking (values shallow mates more than deeper ones)
        if board.is_fivefold_repetition() or board.is_stalemate() or board.is_seventyfive_moves():
            return 0
        if board.is_checkmate():
            return color * (1 - (0.01*(maxDepth - depth))) * -99999 if board.turn else color * (1 - (0.01*(maxDepth - depth))) * 99999
        # testing for 'noisy' positions, and quiescence searching them for Horizon effect mitigation
        if depth == 0:
            if board.is_capture(board.peek()) or board.is_check():
                return self.qSearch(board, alpha, beta, color, maxDepth)
            return color * self.evaluateBoard(board)
        value = -inf
        for move in board.generate_legal_moves():
            board.push(move)
            value = max(value, -1 * self.negaMax(board, depth - 1, -beta, -alpha, -color, maxDepth))
            board.pop()
            # implementing alpha-beta cutoff
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    # Nega Max Root Call
    def negaMaxRoot(self, board, depth, alpha, beta, color, maxDepth):
        global positions
        positions += 1
        value = -inf
        moves = board.generate_legal_moves()
        bestMove = next(moves)
        for move in moves:
            self.board.push(move)
            boardValue = -1 * self.negaMax(board, depth - 1, -beta, -alpha, -color, maxDepth)
            self.board.pop()
            if boardValue > value:
                value = boardValue
                bestMove = move
        # implementing alpha-beta cutoff
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return bestMove, value

    # Engine move function (gets move)
    def move(self):
        global positions
        positions = 0
        # implementing the opening book + move analysis functions
        if self.reader:
            try:
                return self.reader.weighted_choice(self.board).move, 0, 1
            except IndexError:
                bestMove, value = self.negaMaxRoot(self.board, self.depth, -inf, inf, self.color, self.depth)
                return bestMove, value, 0
        bestMove, value = self.negaMaxRoot(self.board, self.depth, -inf, inf, self.color, self.depth)
        return bestMove, value, 0

    # Gets engine move, and returns some stats about engine move
    def moveWithStats(self):
        global positions
        self.initialTime = time()
        bestMove, value, book = self.move()
        self.timeTaken = time() - self.initialTime
        return bestMove, value, book, max(self.timeTaken, 0.001), positions, positions // max(self.timeTaken, 0.001)
