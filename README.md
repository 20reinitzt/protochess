# protochess
A simple chess engine (works quick up to a depth of 5 ply, slows down after that depth)
simple evaluation, negaMax with alpha-beta pruning + small opening book
not really intended to be a good engine, just a learning experience. There are lots of improvements to be made
for example, you could add quiescence search, transposition tables, negaScout, and much more

use pip install python-chess to install dependencies

Pypy3 is recommended, as it runs about 4-5x faster on pypy3 (100,000 nodes/s on pypy vs 20,000 nodes/s on python3)

# Usage
to initialize, type from chessEngine import * <br />
to play against the computer as white, type play() <br />
to watch the computers play eachother, type play_itself() <br />
to analyze a position type analyze() 
  
