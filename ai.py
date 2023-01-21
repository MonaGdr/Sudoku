import json
import sys
import numpy as np
from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp
from sudokuProblem import *




class AI:
    

    def __init__(self):
        pass

    
    def solve(self, problem):
       
        problem_data = json.loads(problem)

        # To convert the data into an array    
        data = AI.convertToArr( problem_data )

        SP = sudokuProblem(data )

        # To run the SA search on the problem
        AI.SA(SP)

        # To convert the array into Json
        result = sudokuProblem.convertToJson(SP)

        return result

    def convertToArr ( problem_data ):
        jarray = problem_data["sudoku"]
        j_1d_Array = []

        for i in range(9):
         jelement = eval(json.dumps(jarray[i]))
         j_1d_Array = j_1d_Array + jelement

        oarray = eval(str(j_1d_Array))
        data = np.array(oarray)
        return data

    def SA ( SP ):

        SP.fillTheBlanks() # initial state
        best_SP = deepcopy(SP)
        current_score = SP.score_board()
        best_score = current_score
        T = .5
        count = 0
    
        while (count < 400000):

            candidate_data = SP.make_candidate_data() # To chose a neighbor
            SP_candidate = sudokuProblem(candidate_data, SP.original_entries)
            candidate_score = SP_candidate.score_board()
            delta_V = float(current_score - candidate_score)
            
            # To make a move with the exp(delta v/T) probebility (even if the new state has a worse score)
            if (exp((delta_V/T)) - random() > 0):
                SP = SP_candidate
                current_score = candidate_score 
        
            # To make a move if the new state's score is better
            if (current_score < best_score):
                best_SP = deepcopy(SP)
                best_score = best_SP.score_board()
        
            # To stop searching if the current state is a goal state
            if candidate_score == -162:
                SP = SP_candidate
                break
    
            T = .99999*T
            count += 1 # To have a limit 
           
       


if __name__ == "__main__":


    #ENTER THE ADDRESS OF YOUR PROBLEM SET FILE
    location = input() 

    #To read the file
    with open(location) as f:
        problem = f.read()

    ai = AI()
    result = ai.solve(problem)

    print( result )

    
