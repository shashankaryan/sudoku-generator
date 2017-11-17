import numpy as np
import math
import random
import os
import multiprocessing
from colorama import init, Fore, Back, Style


class SudokuGenerator(object) :
    """ Generate unique sudoku solutions everytime for n*n grids. """

    def __init__(self, num):

        self.num = num

    def generate_grid(self):
        """ Generate a grid of n*n numbers. """

        grid = np.zeros((self.num,self.num), dtype=np.int)
        return grid

    def generate_check_lists(self):
        """ Returning a dict of n number of lists for row, column and sub-matrix.
        Each list will contain numbers from 1 to n.

        These lists will be used by sudoku_generator function for
        tracking available possibilities of number to fill a particular cell
        following the basic sudoku rules.
        """

        checker= {}
        for i in range(1,self.num+1):
            checker['row'+str(i)]=list(range(1,self.num+1))
            checker['col'+str(i)]=list(range(1,self.num+1))
            checker['box'+str(i)]=list(range(1,self.num+1))
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


    def sudoku_gen(self, state=None):
        """ Pushing number for each cell of the generated grid, following sudoku rules.
        Each number is picked randomly from the list of elements obtained by the
        intersection of checker lists for that particular row, col and submatrix
        """

        count = 0
        while True:

            if  state != None and state.value == 1:
                # print ('Solver',os.getpid(),'quitting')
                break

            else:

                m = self.generate_check_lists()
                sudoku = self.generate_grid()
                count+=1 #to get number of attempts tried to get the solution.

                try:

                    for row_n in range(1, self.num+1):
                        for col_n in range(1, self.num+1):

                            box_n = self.get_submatrix_num(row_n, col_n, int(math.sqrt(self.num)))
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

                    if sudoku[self.num-1][self.num-1]>0: # checking if solution is ready, then break out.
                        print('Total Number of attempts: ' + str(count))
                        self.display(sudoku)

                        if state != None:
                            state.value = 1 # signalling other processes to quit solving
                            # print ('Solver '+ str(os.getpid()), + ' solved the problem!')
                        break

                except IndexError: # Handling Out of Index Error
                    continue


    def cprint(self, msg, foreground = "black", background = "white"):
        """This function is used to provide color to the sudoku cells."""
        fground = foreground.upper()
        bground = background.upper()
        style = getattr(Fore, fground) + getattr(Back, bground)
        print(style + " " + msg + " " + Style.RESET_ALL, end="", flush=True)

    def display(self, solution):
        # Printing the Sudoku.
        for i in range(len(solution)):
            for j in range(len(solution)):
                self.cprint(str(solution[i][j]), "black", "green")
            print('')



class SudokuConcurrentSolver(object):

    def __init__(self, dimension):

        self.dimension = dimension

    def solve(self, nprocs):
        """ Solve for Soduko's concurrntly. """

        state = multiprocessing.Value('i', 0)

        solver = SudokuGenerator(self.dimension)
        proc = [multiprocessing.Process(target=solver.sudoku_gen, args=(state,)) for x in range(nprocs)]

        # Run processes
        for p in proc:
            p.start()

        # Exit the completed processes
        for p in proc:
            p.join()


if __name__ == "__main__":

    import sys
    import argparse

    parser = argparse.ArgumentParser(description='It takes number as optional argument.')
    parser.add_argument('-c',dest='concurrent', action="store_true", help='For implementing concurrency')
    parser.add_argument('-n', dest='gridnum', required=True, help='Grid number for generating sudoku')
    parser.add_argument('-p', dest='procs',default = multiprocessing.cpu_count(),type = int, help='No. of processes to use for concurrent solution.')

    args = parser.parse_args()

    grid_number = int(args.gridnum)
    proc = int(args.procs)
    init() #initialising the colorama

    if args.concurrent:

        instance = SudokuConcurrentSolver(grid_number)
        solution = instance.solve(proc)

    else:

        instance = SudokuGenerator(grid_number)
        solution = instance.sudoku_gen()
