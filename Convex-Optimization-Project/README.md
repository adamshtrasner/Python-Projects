# Convex-Optimization-Project
This project is about solving a convex optimization problem.
* Programming Language: Python

## Definitions
* Band Matrix: a matrix A is called "k-band" if:
  <img src="https://render.githubusercontent.com/render/math?math=|i-j|>k\Rightarrow A_{ij}=0">
* Bandwidth: the k value of a k-band matrix is called the bandwidth of the matrix.

## The Problem to Solve
The convex problem:
<img src="https://render.githubusercontent.com/render/math?math=\underset{K\succeq0:K\ is\ k-band}{min}Tr(SK)-log(|K|)">
Where S is a matrix parameter.

* The algorithm which I chose to use: Newton-Raphson.
