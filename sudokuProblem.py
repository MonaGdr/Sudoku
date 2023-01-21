import json
import sys
import numpy as np
from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp

class sudokuProblem(object):

    def __init__(self, data=None, original_entries=None):
       
        
        self.data = data
    
        if original_entries is None:
            self.original_entries = np.arange(81)[self.data > 0]
        else:
            self.original_entries = original_entries
            
    def fillTheBlanks(self):
        #To fill the blanks randomly. (so we have a random answer (initial state) to start our local search)
        for num in range(9):
            block_indices = self.getBlockIndex(num)
            block = self.data[block_indices]
            zero_indices = [ind for i,ind in enumerate(block_indices) if block[i] == 0]
            to_fill = [i for i in range(1,10) if i not in block]
            shuffle(to_fill)
            for ind, value in zip(zero_indices, to_fill):
                self.data[ind] = value
            
    def view_results(self):

        def notzero(s):
            if s != 0: return str(s)
            if s == 0: return "'"
            
        results = np.array([self.data[self.getRowIndex(j, type="row index")] for j in range(9)])
        out_s = ""
        for i, row in enumerate(results):
            if i%3==0: 
                out_s += "="*25+'\n'
            out_s += "| " + " | ".join([" ".join(notzero(s) for s in list(row)[3*(k-1):3*k]) for k in range(1,4)]) + " |\n"
        out_s = out_s + "="*25+'\n'
        print (out_s)
        
    def score_board(self):
        score = 0
        for row in range(9):
            score -= len(set(self.data[self.getRowIndex(row, type="row index")]))
        for col in range(9):
            score -= len(set(self.data[self.getColumnindex(col,type="column index")]))
        return score
        
    def make_candidate_data(self):

        new_data = deepcopy(self.data)
        block = randint(0,8)
        num_in_block = len(self.getBlockIndex(block, ignore_originals=True))
        if num_in_block>1:
            random_squares = sample(range(num_in_block),2)
            square1, square2 = [self.getBlockIndex(block, ignore_originals=True)[ind] for ind in random_squares]
            new_data[square1], new_data[square2] = new_data[square2], new_data[square1]
        return new_data

    def getBlockIndex(self, k, ignore_originals=False):
        
        row_offset = (k // 3) * 3
        col_offset = (k % 3)  * 3
        indices = [col_offset + (j%3) + 9*(row_offset + (j//3)) for j in range(9)]
        if ignore_originals:
            indices = list( filter(lambda x:x not in self.original_entries, indices))
        return indices
        
    def getColumnindex(self, i, type="data index"):

        if type=="data index":
            column = i % 9
        elif type=="column index":
            column = i
        indices = [column + 9 * j for j in range(9)]
        return indices
        
    def getRowIndex(self, i, type="data index"):
        
        if type=="data index":
            row = i // 9
        elif type=="row index":
            row = i
        indices = [j + 9*row for j in range(9)]
        return indices
        
    def convertToJson(self):

        def notzero(s):
            if s != 0 : return str(s)
            if s == 0 : return "0"
 
        
        results = np.array([self.data[self.getRowIndex(j, type="row index")] for j in range(9)])
        out_s = ""
        out_s += '{\n'
        out_s += "\"sudoku\":"
        for i, row in enumerate(results):
            if i==0 or i==9: 
                out_s += '  ['+'\n'
            out_s += '      ['
            if i==8:
                out_s += ", ".join([",".join(notzero(s) for s in list(row)[3*(k-1):3*k]) for k in range(1,4)]) + "]\n"
            else:
                out_s += ", ".join([",".join(notzero(s) for s in list(row)[3*(k-1):3*k]) for k in range(1,4)]) + "],\n"
        out_s += '  ]\n'
        out_s += '}'
        return out_s
            