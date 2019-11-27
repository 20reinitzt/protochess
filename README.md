# protochess
A simple chess engine (works quick up to a depth of 5 ply, slows down after that depth) (with qSearch implemented, it is slow at 4 ply, but plays at a higher elo)
simple evaluation, negaMax with alpha-beta pruning + small opening book.
This engine is not really intended to be a good chess player, just a learning experience. There are lots of improvements to be made:
for example, you could add better quiescence search, transposition tables, negaScout, better evaluation function, and much more

use pip install python-chess to install dependencies

Pypy3 is recommended, as it runs about 4-6x faster on pypy3 (50,000-60,000 nodes/s on pypy vs 10,000-15,000 nodes/s on python3)

# Usage
to initialize, type from protochess import * <br />
to play against the computer as white, type play() <br />
to watch the computers play eachother, type play_itself() <br />
to analyze a position type analyze() 
  
# Elo
after testing with lichess stockfish, it performs on the same level as stockfish level 4-5 at depth 4, so rough ELO guess would be 1400. I've been doing puzzles with it on lichess, and its puzzle rating seems to hover around 1700-1800. At depth 5, it takes significantly longer to analyze ( > 5 minutes in complex positions), but seems to perform at the level of stockfish level 6, and sometimes takes games against level 7. From this, I think it's rating at depth 5 is around 1700
