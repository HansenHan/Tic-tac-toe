#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import numpy as np
import time


# In[2]:


def play_a_new_game():
    print("--------------------------")  # header for the game
    print("|Welcome to Tic-tac-toe! |")
    print("--------------------------")
#     game = [" "]*9
    print_game([1,2,3,4,5,6,7,8,9])  # print the game board

    while(True):
        a = input("Do you want to play first? (yes/no/quit) ")   # let user enter
        if(a in ["yes", "no", "quit"]): break
            
    while(True):
        game = [" "]*9
        if(a == "yes"):
            start_game(game, 1)
        elif(a == "no"):
            start_game(game, -1)
        else:
            return
        
        while(True):
            b = input("Do you want to play again? (yes/no) ")  # let user play again
            if(b in ["yes", "no"]): break
        if(b == "no"):
            return
        print_game([1,2,3,4,5,6,7,8,9])


# In[3]:


def start_game(game, role):  # start the game; role=1 means user play first, role=-1 means computer play first
    pos_move = []
    
    for j in range(9):
        if game[j]!="x" and game[j]!="o":  # to find all possible moves, "o" is symbol for computer, "x" is symbol for user
            pos_move.append(j)

    role_count = role # 1 is user -1 is computer
    while(pos_move):
    
        if(role_count == -1):
            pos_set = game_logic(game, 5000)   # the simulation is 5000 times, and get the best move for computer
            pos_move.remove(pos_set)
            game[pos_set] = "o"
        
        else:
            while True:      # let user make a move
                pos_set = str(input("Choose a position [1-9]: "))
#                 print(pos_move)
#                 print(type(pos_set))
                if(pos_set in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                    pos_set = int(pos_set)
                    if((pos_set-1) in pos_move):
                        break
                    print("The position is occupied!")
            pos_move.remove(pos_set-1)
            game[pos_set-1] = "x"
        
        print_game(game)
    
        role_count = 0-role_count
        if(check_win(game) == "x"):  # check user win or not 
            print("You win!")
            return
        if(check_win(game) == "o"):  # check computer win or not
            print("Computer win!")
            return
    print("Tie")  # game is tie
    return


# In[ ]:





# In[4]:


def print_game(game):  # print the game board
    assert(len(game) == 9)
    for i in range(3):
        print((" "+"-"*5)*3)
        for j in range(3):
            print("|  "+str(game[j+i*3])+"  ", end = ""),
        print("|")
    print((" "+"-"*5)*3)


# In[5]:


def check_win(game):  # check is there a winner, return the winner symbol or return not
    for i in range(3):
        if((game[i*3]=="x" or game[i*3]=="o") and 
           game[i*3]==game[i*3+1] and game[i*3]==game[i*3+2]):
            return game[i*3];
    for i in range(3):
        if((game[i]=="x" or game[i]=="o") and 
           game[i]==game[i+3] and game[i]==game[i+6]):
            return game[i];
    if ((game[0]=="x" or game[0]=="o") and 
        game[0] == game[4] and game[0] == game[8]):
        return game[0]
    if ((game[2]=="x" or game[2]=="o") and 
        game[2] == game[4] and game[2] == game[6]):
        return game[2]
    return "not"


# In[6]:


def game_logic(game, number):  # get a best move for computer, return the move index
    score = [0]*9
    pos_move = []

#     print("check 4!!!!!")
    
    for j in range(9):  # get all possible moves
        if game[j]!="x" and game[j]!="o":
            pos_move.append(j)
    
#     print("check 5!!!!!")
    
    
    for k in pos_move:
        t_game = game.copy()
        t_game[k] = "o"
        if(check_win(t_game)=="o"):
            return k
    
    if(len(pos_move)==8): # check the corner case
        for p in range(8):
            if(game[p]=="x" or game[p]=="o"):
                if(p==0): return 8
                if(p==2): return 6
                if(p==6): return 2
                if(p==8): return 0
        
#     print("check 3!!!!!")
    
    for act in pos_move: # for each possible actions
        start = time.time()
        
        
        rand_move = pos_move.copy() # get random move for each actions
        rand_move.remove(act)
        
        copy_game = game.copy() # get a copy of the game board with the action
        copy_game[act] = "o"
        
        count = 0
        tmp_score = 0
        
        test_count = 0
        while True :  # simulation 5000 times
            
            rand_move = pos_move.copy()
            rand_move.remove(act)

            copy_game = game.copy()
            copy_game[act] = "o"
            
#             print("check 2!!!!!")
            
            role_count = 1 # -1 is computer and 1 is user
            break_flag = False
            while rand_move:  # for all possible random move, simulate
#                 print("check 1!!!!!")

                if role_count == 1: # simulate for user
                    for i in rand_move:
                        test_game = copy_game.copy()
                        test_game[i] = "x"
                        if(check_win(test_game)=="x"):
#                             print("Check detected!!!!!!")
                            tmp_score += -2
    
                            test_count+=1
                            break_flag = True
                            break
                if break_flag:
#                     print("check 6!!!!!")
                    break_flag = False
                    break
                    
                    
                tmp_move = random.choice(rand_move)  # get a random move to simulate
                rand_move.remove(tmp_move)
                
                if role_count == 1:
                    copy_game[tmp_move] = "x"
                else:
                    copy_game[tmp_move] = "o"
                
                if(check_win(copy_game) == "x"):  # get a score for simulation; +2 for win, -2 for lose, +1 for tie
                    tmp_score += -2
                elif(check_win(copy_game) == "o"):
                    tmp_score += 2
                elif(not rand_move and check_win(copy_game) == "not"):
                    tmp_score += 1
                    
                role_count = 0-role_count
            
            end = time.time()
            count+=1
#             if end - start >= 0.5:
#                 break
            if count >= number:
                break
        score[act] = tmp_score
    result = random.choice(pos_move)
    for y in pos_move:
        if(score[y]>score[result]):   # get the max score
            result = y
#    print(score)
#    print(result)
    return result  # return the best move index




if __name__ == '__main__':
  play_a_new_game()



