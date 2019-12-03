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
  
# Elojavascript:void(0);
after testing with lichess it performs at a rough lichess level of 1500 on depth 4 (probably a rough elo of 1300-1350). Depth 5 performs at a +191 elo from depth 4 (tested with 50 self-play games). Extrapolation of this presents a rough elo of 1500 for depth 5
