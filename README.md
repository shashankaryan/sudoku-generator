# sudoku-generator
This program will help in generating different solutions for perfect square matrices.

Sudoku Generator Logic

Major Rules we are focusing:
1. The number should not exist already in current row.
2. The number should not exist already in current column.
3. Number should not exist in the nxn submatrix when matrix is sqr(n)*sqr(n).

Approach is completely based on the Rules:

We are taking n arrays for each, row, col and submatrix(box). So if we are working with 4*4 sudoku we will be having 4 arrays each for rows, columns and boxes. eaching having numbers upto n starting from 1

<code>
r1 => [1, 2, 3, 4]
c1 => [1, 2, 3, 4]
b1 => [1, 2, 3, 4]
r2 => [1, 2, 3, 4]
c2 => [1, 2, 3, 4]
b2 => [1, 2, 3, 4]
r3 => [1, 2, 3, 4]
c3 => [1, 2, 3, 4]
b3 => [1, 2, 3, 4]
r4 => [1, 2, 3, 4]
c4 => [1, 2, 3, 4]
b4 => [1, 2, 3, 4]
</code>
For filling every cell, we are taking a number randomly from row arrays(r1,r2,r3,r4), and putting into that particular cell,

For example,
1. If we are filling (row_n, col_n) --> (0,0)th index, we will pick 1 number randomly from r1.
2. Lets suppose, randomly 4 was selected, now 4 is removed from r(row_n+1), c(col_n+1) and using that row_n and col_n we will find box_n also from which 4 should be removed.

Hence using this approach, every cell will be randomly filled with a number which is present in all 3 arrays, r(row_n), c(col_n) and box(box_n).

And this will generate a complete diffrent solutions for every sudoku of 4*4, 9*9, .... and so on.
