import numpy as np
import math
import random

class SudokuGenerator:
    """ Generate unique sudoku solutions everytime for n*n grids. """

    def generate_grid(self, num):
        """ Generate a grid of n*n numbers. """

        grid = np.zeros((num,num), dtype=np.int)
        return grid

    def generate_check_lists(self, num):
        """ Returning a dict of n number of lists for row, column and sub-matrix.
        Each list will contain numbers from 1 to n.

        These lists will be used by sudoku_generator function for
        tracking available possibilities of number to fill a particular cell
        following the basic sudoku rules.
        """

        checker= {}
        for i in range(1,num+1):
            checker['row'+str(i)]=list(range(1,num+1))
            checker['col'+str(i)]=list(range(1,num+1))
            checker['box'+str(i)]=list(range(1,num+1))
        return checker

    def get_submatrix_num(self, row_n, col_n, root_n):
        """ Getting the num of sub-matrix using the row and coloumn number. """

        if row_n % root_n == 0:   # root_n is square root of n
            row_t = int(row_n/root_n)
        else:
            row_t = int(row_n/root_n) + 1
        if col_n % root_n == 0:
            col_t = int(col_n/root_n)
        else:
            col_t = int(col_n/root_n) + 1
        box_n = col_t + (row_t-1)*root_n  # formula for calculating which submatrix box, a (row,column) belongs
        return box_n

    def sudoku_gen(self, num):
        """ Pushing number for each cell of the generated grid, following sudoku rules.
        Each number is picked randomly from the list of elements obtained by the
        intersection of checker lists for that particular row, col and submatrix
        """

        count = 0
        while True:

            m = self.generate_check_lists(num)
            sudoku = self.generate_grid(num)
            count+=1 #to get number of attempts tried to get the solution.

            try:

                for row_n in range(1, num+1):
                    for col_n in range(1, num+1):

                        box_n = self.get_submatrix_num(row_n, col_n, int(math.sqrt(num)))
                        row = 'row' + str(row_n)
                        col = 'col' + str(col_n)
                        box = 'box' + str(box_n)
                        # print('target row, column, box  => ' +  row, col, box)

                        common_list = list(set(m[row]).intersection(m[col],m[box])) # creating commom list.
                        # print(common_list)

                        rand_num = random.choice(common_list) # picking a number from common list.
                        sudoku[row_n-1][col_n-1] = rand_num
                        m[row].remove(rand_num)
                        m[col].remove(rand_num)
                        m[box].remove(rand_num)

                if sudoku[num-1][num-1]>0: # checking if solution is ready, then break out.
                    print('Total Number of attempts: ' + str(count))
                    break

            except IndexError: # Handling Out of Index Error
                continue

        return sudoku

if __name__ == "__main__":
    x = SudokuGenerator()
    y = x.sudoku_gen(9)
    print (y)