import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import date
import time
import random

##########################
## test function

def test_f():
    return 'hello world'

#####################################
## functions for AI tic tac toe game

def full_rows(board_s, pick_XO, pc):
    # check rows which are not full yet
    full_dict = {pick_XO:1, pc:1, '':0}
    
    board_full = {'R1':[ full_dict[board_s['p1']], full_dict[board_s['p2']], full_dict[board_s['p3']] ],
                  'R2':[ full_dict[board_s['p4']], full_dict[board_s['p5']], full_dict[board_s['p6']] ],
                  'R3':[ full_dict[board_s['p7']], full_dict[board_s['p8']], full_dict[board_s['p9']] ],
                  'C1':[ full_dict[board_s['p1']], full_dict[board_s['p4']], full_dict[board_s['p7']] ],
                  'C2':[ full_dict[board_s['p2']], full_dict[board_s['p5']], full_dict[board_s['p8']] ],
                  'C3':[ full_dict[board_s['p3']], full_dict[board_s['p6']], full_dict[board_s['p9']] ],
                  'D1':[ full_dict[board_s['p1']], full_dict[board_s['p5']], full_dict[board_s['p9']] ],
                  'D2':[ full_dict[board_s['p7']], full_dict[board_s['p5']], full_dict[board_s['p3']] ]
                  }

    # for every row check if all their boxes are filled
    empty_rows = []
    for item in board_full.items():
        if sum(item[1]) != 3: # 3 means all boxes in a row are filled
            empty_rows.append(item[0])
    
    return empty_rows

def game_over(board_s, pick_XO, pc):
    # check if there is a winner
    decode_dict = {pick_XO:1, pc:-1, '':0}
    
    board_decode = {'R1':[ decode_dict[board_s['p1']], decode_dict[board_s['p2']], decode_dict[board_s['p3']] ],
                    'R2':[ decode_dict[board_s['p4']], decode_dict[board_s['p5']], decode_dict[board_s['p6']] ],
                    'R3':[ decode_dict[board_s['p7']], decode_dict[board_s['p8']], decode_dict[board_s['p9']] ],
                    'C1':[ decode_dict[board_s['p1']], decode_dict[board_s['p4']], decode_dict[board_s['p7']] ],
                    'C2':[ decode_dict[board_s['p2']], decode_dict[board_s['p5']], decode_dict[board_s['p8']] ],
                    'C3':[ decode_dict[board_s['p3']], decode_dict[board_s['p6']], decode_dict[board_s['p9']] ],
                    'D1':[ decode_dict[board_s['p1']], decode_dict[board_s['p5']], decode_dict[board_s['p9']] ],
                    'D2':[ decode_dict[board_s['p7']], decode_dict[board_s['p5']], decode_dict[board_s['p3']] ]
                    }
    
    # check if there is any row with the same values to know the winner
    for item in board_decode.items():
        if sum(item[1]) == 3:
            return 1 # player wins
        elif sum(item[1]) == -3:
            return 2 # pc wins
        else:
            pass
        
    # check if all boxes are filled and it is a draw
    position_values=[]
    for item in list(board_s.items()):
        position_values.append(item[1])
    
    if '' not in position_values:
        return 3 # draw
    else:
        return 0 # keep playing


def gain_table(board_s, pick_XO, pc):
    # decode board states to numbers
    decode_dict = {pick_XO:1, pc:-1, '':0}
    
    board_decode = {'R1':[ decode_dict[board_s['p1']], decode_dict[board_s['p2']], decode_dict[board_s['p3']] ],
                    'R2':[ decode_dict[board_s['p4']], decode_dict[board_s['p5']], decode_dict[board_s['p6']] ],
                    'R3':[ decode_dict[board_s['p7']], decode_dict[board_s['p8']], decode_dict[board_s['p9']] ],
                    'C1':[ decode_dict[board_s['p1']], decode_dict[board_s['p4']], decode_dict[board_s['p7']] ],
                    'C2':[ decode_dict[board_s['p2']], decode_dict[board_s['p5']], decode_dict[board_s['p8']] ],
                    'C3':[ decode_dict[board_s['p3']], decode_dict[board_s['p6']], decode_dict[board_s['p9']] ],
                    'D1':[ decode_dict[board_s['p1']], decode_dict[board_s['p5']], decode_dict[board_s['p9']] ],
                    'D2':[ decode_dict[board_s['p7']], decode_dict[board_s['p5']], decode_dict[board_s['p3']] ]
                    }
    
    # function to fill boxes only on available rows 
    av_rows = full_rows(board_s, pick_XO, pc)
    
    # check gain status for each row - list of tuples each available row with gain
    board_gain = []
    for item in board_decode.items():
        if item[0] in av_rows:
            board_gain.append((item[0], sum(item[1])))
        
    # sorted result list ascending (-2,-1,0,1,2)
    board_gain = sorted(board_gain, key=lambda tup: tup[1])
    
    return board_gain

def row_candidates_to_fill(board_gain):
    # choose which row has to be filled
    
    # if there are no left boxes to fill - gain = []
    if len(board_gain) == 0:
        return []
    
    # pc or player to win
    if board_gain[0][1] == -2: # pc to win in this turn
        return [board_gain[0][0]]
    elif board_gain[-1][1] == 2: # player to win in next turn
        return [board_gain[-1][0]]
    else:
        pass
    
    # still more turn for some one to win - pick row candidates to fill
    if abs(board_gain[0][1]) > board_gain[-1][1]: # advantage for pc
        max_gain = board_gain[0][1]
        row_candidates = []
        for row in board_gain:
            if row[1] == max_gain:
                row_candidates.append(row[0])
        
    elif abs(board_gain[0][1]) < board_gain[-1][1]: # advantage for player
        max_gain = board_gain[-1][1]
        row_candidates = []
        for row in board_gain:
            if row[1] == max_gain:
                row_candidates.append(row[0])     
                
    else:  # draw
        max_gain = board_gain[-1][1]
        row_candidates = []
        for row in board_gain:
            if abs(row[1]) == max_gain:
                row_candidates.append(row[0]) 

    return row_candidates

def box_to_fill(board_s, row_candidates, diff):
    # decide which box to fill from row candidates
    
    # relation row index with box position
    box_positions = {'R1-0':1, 'R1-1':2, 'R1-2':3,
                     'R2-0':4, 'R2-1':5, 'R2-2':6,
                     'R3-0':7, 'R3-1':8, 'R3-2':9,
                     'C1-0':1, 'C1-1':4, 'C1-2':7,
                     'C2-0':2, 'C2-1':5, 'C2-2':8,
                     'C3-0':3, 'C3-1':6, 'C3-2':9,
                     'D1-0':1, 'D1-1':5, 'D1-2':9,
                     'D2-0':7, 'D2-1':5, 'D2-2':3,
                     }
    
    # board situation
    board_positions = {'R1':[ board_s['p1'], board_s['p2'], board_s['p3'] ],
                       'R2':[ board_s['p4'], board_s['p5'], board_s['p6'] ],
                       'R3':[ board_s['p7'], board_s['p8'], board_s['p9'] ],
                       'C1':[ board_s['p1'], board_s['p4'], board_s['p7'] ],
                       'C2':[ board_s['p2'], board_s['p5'], board_s['p8'] ],
                       'C3':[ board_s['p3'], board_s['p6'], board_s['p9'] ],
                       'D1':[ board_s['p1'], board_s['p5'], board_s['p9'] ],
                       'D2':[ board_s['p7'], board_s['p5'], board_s['p3'] ]
                       }
    
    # if there are no candidates
    if len(row_candidates) == 0:
        return 0
    
    # if the pc or the player are about to win
    if len(row_candidates) == 1:
        row = board_positions[row_candidates[0]]
        i=0
        while i < len(row):
            if row[i] == '':
                solution_key = row_candidates[0] + '-' + str(i)
                return(box_positions[solution_key])
            else:
                i = i + 1
        
    # if not about to win
    
    ## Easy mode -- pick an available box randomly
    if diff == 'Easy':
        box_list = list(board_s.keys())
        while True:
            rand_box = random.choice(box_list)
            if board_s[rand_box] == '':
                return int(rand_box[1])
    
    ## Hard mode -- try: 1- fill center box, 2- fill corners, 3- fill edges
    elif diff == 'Hard':
        # 1- fill center box
        if board_s['p5']=='' and (('R2' in row_candidates) or ('C2' in row_candidates) or ('D1' in row_candidates) or ('D2' in row_candidates)):
            return 5
        
        # # 2- fill corners
        # if board_s['p1']=='' or board_s['p3']=='' or board_s['p7']=='' or board_s['p9']=='':
        #     for cand in row_candidates:
        #         if cand not in ['R2','C2']:
        #             row = board_positions[cand]
        #             i=0
        #             while i < len(row):
        #                 if row[i] == '' and i!=1:
        #                     solution_key = cand + '-' + str(i)
        #                     return(box_positions[solution_key])
        #                 else:
        #                     i = i + 1
        
        # 3- fill corners
        for cand in row_candidates:
            row = board_positions[cand]
            i=0
            while i < len(row):
                if row[i] == '':
                    solution_key = cand + '-' + str(i)
                    return(box_positions[solution_key])
                else:
                    i = i + 1
                    
    else:
        pass

def pc_turn_f(board_s, pick_XO, pc, diff):
    # the pc chooses a box to fill
    gain_list = gain_table(board_s, pick_XO, pc)
    row_candidates = row_candidates_to_fill(gain_list)
    pc_choice = box_to_fill(board_s, row_candidates, diff)
    return pc_choice

## AI testing area
# board_test = {'p1':'X', 'p2':'X', 'p3':'O',
#               'p4':'O' , 'p5':'O', 'p6':'X',
#               'p7':'X', 'p8':'X' , 'p9':'O' }
# pick_XO = 'X'
# pc = 'O'
# game_statuts = game_over(board_test, pick_XO, pc)
# print(game_statuts)
# pc_turn = pc_turn(board_test, pick_XO, pc)
# print(pc_turn)
    

# test area
# board_test = {'p1':'X', 'p2':'O', 'p3':'',
#               'p4':'X' , 'p5':'', 'p6':'',
#               'p7':'O', 'p8':'X' , 'p9':'' }
# pick_XO = 'X'
# pc = 'O'
# diff = 'Easy'
# game_statuts = game_over(board_test, pick_XO, pc)
# pc_turn = pc_turn(board_test, pick_XO, pc, diff)

# print(game_statuts)
# print(pc_turn)
    

##########################
## Roulette functions

def option_from_bet_type(bet_type):
    if bet_type == 'Single number':
        return list(range(0,37))
    elif bet_type == 'Double numbers':
        l = []
        l.append([0,1])
        l.append([0,2])
        l.append([0,3])
        for e in list(range(1,34)):
            l.append([e,e+3])
        return l
    elif bet_type == 'Three numbers':
        l = []
        l.append([0,1,2])
        l.append([0,2,3])
        l_nums = np.arange(1, 35, 3, dtype=int)
        for e in l_nums:
            l.append([e,e+1,e+2])
        return l
    elif bet_type == 'Four numbers':
        l = []
        l.append([0,1,2,3])
        l_nums_1 = list(np.arange(1, 32, 3, dtype=int))
        l_nums_2 = list(np.arange(2, 33, 3, dtype=int))
        l_nums = sorted(l_nums_1 + l_nums_2)
        for e in l_nums:
            l.append([e,e+1,e+3,e+4])
        return l
    elif bet_type == 'Six numbers':
        l = []
        l_nums = list(np.arange(1, 32, 3, dtype=int))
        for e in l_nums:
            l.append([e,e+1,e+2,e+3,e+4,e+5])
        return l
    elif bet_type == 'Dozen':
        return ['First Dozen', 'Second Dozen', 'Third Dozen']
    elif bet_type == 'Column':
        return ['First Column', 'Second Column', 'Third Column']
    elif bet_type == '18 numbers':
        return ['From 1 to 18', 'From 19 to 36']
    elif bet_type == 'Red/Black':
        return ['Red', 'Black']
    elif bet_type == 'Odd/Even':
        return ['Odd', 'Even']
    else:
        pass  

def player_win(roulette_result, num_bets, ses_state, dict_bets, dict_odds):
    player_wins = 0
    for e in range(1,num_bets+1):
        bet_type = ses_state[('bet_{}_type').format(e)]
        bet_select = ses_state[('bet_{}_select').format(e)]
        bet_amount = ses_state[('bet_{}_amount').format(e)]
        if type(bet_select) == int:
            print('a')
            bet_select = [bet_select]
            if roulette_result in bet_select:
                bet_odds = dict_odds[bet_type]
                player_wins = player_wins + bet_odds * bet_amount
            else:
                player_wins = player_wins - bet_amount
        elif type(bet_select) == list:
            print('b')
            if roulette_result in bet_select:
                bet_odds = dict_odds[bet_type]
                player_wins = player_wins + bet_odds * bet_amount
            else:
                player_wins = player_wins - bet_amount
        else:
            numbers = dict_bets[bet_select]
            print('c')
            if roulette_result in numbers:
                bet_odds = dict_odds[bet_type]
                player_wins = player_wins + bet_odds * bet_amount
            else:
                player_wins = player_wins - bet_amount
        
    return player_wins
    
# numbers in bet types
red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
black_numbers = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
first_dozen = list(range(0,13))
second_dozen = list(range(13,25))
third_dozen = list(range(25,37))
first_column = list(np.arange(1, 35, 3, dtype=int))
second_column = list(np.arange(2, 36, 3, dtype=int))
third_column = list(np.arange(3, 37, 3, dtype=int))
first_18 = list(range(0,19))
second_18 =  list(range(19,37))
odd_numbers = list(np.arange(1, 37, 2, dtype=int))
even_numbers = list(np.arange(2, 38, 2, dtype=int))

# bets dictionary
dict_bets = {'First Dozen':first_dozen, 'Second Dozen':second_dozen, 'Third Dozen':third_dozen,
             'First Column':first_column, 'Second Column':second_column, 'Third Column':third_column,
             'From 1 to 18':first_18, 'From 19 to 36':second_18,
             'Red':red_numbers, 'Black':black_numbers,
             'Odd':odd_numbers, 'Even':even_numbers}

# bet ods
dict_odds = {'Single number':35, 'Double numbers':17, 'Three numbers':11, 'Four numbers':8, 'Six numbers':5, 
             'Dozen':2, 'Column':2, '18 numbers':1, 'Red/Black':1, 'Odd/Even':1}

# roulette result
roulette_result = 1

# num bets
num_bets = 1

# session state
# ses_state = {"bet_1_type":"Red/Black", "bet_1_amount":1, "bet_1_select":"Red",
#               "bet_2_type":"Single number", "bet_2_amount":1, "bet_2_select":0,
#               "bet_3_type":"Double numbers", "bet_3_amount":1, "bet_3_select":[1,2],
#               }
ses_state = {"bet_1_type":"Red/Black", "bet_1_amount":1, "bet_1_select":"Red"}
# ses_state = {"bet_1_type":"Single number", "bet_1_amount":1, "bet_1_select":0}
# ses_state = {"bet_1_type":"Double numbers", "bet_1_amount":1, "bet_1_select":[1,2]}


# print(player_win(roulette_result, num_bets, ses_state, dict_bets, dict_odds))







