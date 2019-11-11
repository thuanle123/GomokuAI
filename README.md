# GomokuAI
Artificial Intelligence project on the game Gomoku

# Description
With the advancement of Artificial Intelligence (AI), creating game has been more easier. Gomoku is an ancient board game with high strategy system. The purpose of this game is to connect 5 before the opponent on a 15x15 board. The project was built using Minimax and Alpha-beta pruning to create a robust AI. The AI is deterministic and has perfect information. 

# Math
Gomoku is a two-player game. The game is deterministic and has a small tree with approxmiately 15! tree node. Minimax search chooses move to position with highest minimax value to achieve payoff against best play. Time O(b^m), Space(bm). Alpha–beta pruning is a search algorithm that seeks to decrease the number of nodes that are evaluated by the minimax algorithm in its search tree. Alpha is the best value (for Max) found so far at any choice point along the path for Max. Beta is the best value (for Min) found so far at any choice point along the best. If utility v is worse than alpha, max will avoid it. Meanwhile, if utility v is larger than beta, min will avoid it.


# Setup
Install python3 and python3-tk

# Running
```
  python3 gomoku.py
  ENJOY!!
```
