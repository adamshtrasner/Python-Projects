# Nonogram
A Python implementation of the Nonogram game, using backtracking.

# Description
Nonogram is a picture logic puzzle in which cells in a grid must be colored or left blank according to numbers at the side of the grid to reveal a hidden picture.
In this implementation, the game is represented as follows:
* An n x m board is represented by an n x m matrix (an array of n arrays of size m) of integers.
  a blank spot is represented by 0, a marked spot is represented by 1, and an undecided spot is represented by -1.
* The constraints (the numbers from the left of the board and above it) are represented by an array of 2 arrays: the first array represents the rows constarints, 
  and the second array represents the columns constraints. In each of those arrays, each cell is an array representing the numbers (constraints) of that row/column.
  
A vivid example of how the board and the constraints are shown can be executed by the helper.py program.

