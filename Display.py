# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:47:57 2019

@author: Océane
"""
ICONS = [' ',1,2,3,4,5,6,7,8,9] + list(range(10,100))

def displayBoard(grid):
    CELL_SIZE=9

    CELL_HEIGHT = int(CELL_SIZE/3)

    GRID_WIDTH = len(grid[0])
    GRID_HEIGHT= len(grid)

    out_str = ''

    def displayHor_line():
        out_str=''
        for j in range(GRID_WIDTH):
            out_str += '|'
            for k in range(CELL_SIZE):
                out_str += '-'
        out_str += '|'
        return out_str

    for i in range(GRID_HEIGHT):
        out_str += displayHor_line()

        for l in range(CELL_HEIGHT):
            out_str += '\n'
            for j in range(GRID_WIDTH):

                out_str += '|'
                cellColsIter = iter(range(CELL_SIZE))
                for k in cellColsIter:
                    if (k) == int(CELL_SIZE/2)-(1 if grid[i][j]>9 else 0) and l == int(CELL_HEIGHT/2):
                        out_str += str(ICONS[grid[i][j]])

                        if grid[i][j]>9:
                            next(cellColsIter)
                    else:
                        out_str += ' '
            out_str += '|'
        out_str += '\n'

    out_str += displayHor_line()
    out_str += '\n'
    print(out_str)