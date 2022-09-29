from ast import arg
from collections import deque
from fileinput import filename
from os import stat
import queue
from re import T
import readline
from time import process_time_ns
from tkinter import E
from turtle import shape
from xml.dom.minidom import CharacterData
import numpy as np
import sys


MAXLEN=200
board=np.full(shape=(MAXLEN,MAXLEN),fill_value=99) #empty is 99, x is 1, o is 0
filename_x='xmoves.txt '
filename_o='omoves.txt '

# xo grid
#  a b c d ... 
# 0
# 1
# 2
# 3
# 4
def readMove(msg):
    if msg[0] == 'x':
        # filex=open(filename_x,'r')
        # move=filex.readline()
        row=int(msg[1])-1# number in string
        col=int(msg[2]-'a')# letter in string
        board[row][col]=1
        
    else:
        row=int(msg[1])-1# number in string, start from 0
        col=ord(msg[2])-ord('a')# letter in string
        board[row][col]=0



def heuristic_d(state):
    global n,k
    hvalue=0
    xCnt=0
    oCnt=0
    maxXCnt=0
    maxOCnt=0
    # check rows
    for i in range(0,n):
        xCnt=0
        oCnt=0
        for j in range(0,n):
            if state[i,j] == 1:
                xCnt+=1
                oCnt=0
                maxXCnt=max(xCnt,maxXCnt)
            elif state[i,j] == 0:
                xCnt=0
                oCnt+=1
                maxOCnt=max(oCnt, maxOCnt)
            else:
                xCnt=0
                oCnt=0
        if xCnt >= k:
            hvalue= np.inf
            return hvalue
        if oCnt>=k:
            hvalue= -np.inf
            return hvalue

    xCnt=0
    oCnt=0
    maxXCnt=0
    maxOCnt=0
    # check cols
    for j in range(0,n):
        xCnt=0
        oCnt=0
        for i in range(0,n):
            if state[i,j] == 1:
                xCnt+=1
                oCnt=0
                maxXCnt=max(xCnt,maxXCnt)
            elif state[i,j] == 0:
                xCnt=0
                oCnt+=1
                maxOCnt=max(oCnt,maxOCnt)
            else:
                xCnt=0
                oCnt=0
        if xCnt >= k:
            hvalue= np.inf
            return hvalue
        if oCnt>=k:
            hvalue= -np.inf
            return hvalue
    xCnt=0
    oCnt=0
    maxXCnt=0
    maxOCnt=0
    # check diagnal leftup to right down
    for i in range(0,n):
        for j in range(0,n):
            xCnt=0
            oCnt=0
            for m in range(0,n):
                if i+m<0 or i+m>=n or j+m<0 or j+m >=n:
                    continue
                if state[i+m,j+m] == 1:
                    xCnt+=1
                    oCnt=0
                    maxXCnt=max(xCnt,maxXCnt)
                elif state[i+m,j+m] == 0:
                    xCnt=0
                    oCnt+=1
                    maxOCnt=max(oCnt,maxOCnt)
                else:
                    xCnt=0
                    oCnt=0
            if xCnt >= k:
                hvalue= np.inf
                return hvalue
            if oCnt>=k:
                hvalue= -np.inf
                return hvalue

        
    xCnt=0
    oCnt=0
    maxXCnt=0
    maxOCnt=0
    # check diagnal leftdown to rightup
    for i in reversed(range(0,n)):
        for j in range(0,n):
            xCnt=0
            oCnt=0
            for m in range(0,n):
                if i-m<0 or i-m>=n or j+m<0 or j+m >=n:
                    continue
                if state[i-m,j+m] == 1:
                    xCnt+=1
                    oCnt=0
                    maxXCnt=max(xCnt,maxXCnt)
                elif state[i-m,j+m] == 0:
                    xCnt=0
                    oCnt+=1
                    maxOCnt=max(oCnt,maxOCnt)
                else:
                    xCnt=0
                    oCnt=0
                if xCnt >= k:
                    hvalue= np.inf
                    return hvalue
                if oCnt>=k:
                    hvalue= -np.inf
                    return hvalue
    
    hvalue=pow(10,maxXCnt)-pow(10,maxOCnt)
    return hvalue

#check winning state, count rows,cols,diag1,diag2
#improve: can be added to readmove()
def heuristic(state):
    global n,k
    hvalue=0
    xCnt=0
    oCnt=0
    # check rows
    for i in range(0,n):
        xCnt=0
        oCnt=0
        for j in range(0,n):
            if state[i,j] == 1:
                xCnt+=1
                oCnt=0
            elif state[i,j] == 0:
                xCnt=0
                oCnt+=1
            else:
                xCnt=0
                oCnt=0
        if xCnt >= k:
            hvalue= 100
            return hvalue
        if oCnt>=k:
            hvalue= -100
            return hvalue

    xCnt=0
    oCnt=0
    # check cols
    for j in range(0,n):
        xCnt=0
        oCnt=0
        for i in range(0,n):
            if state[i,j] == 1:
                xCnt+=1
                oCnt=0
            elif state[i,j] == 0:
                xCnt=0
                oCnt+=1
            else:
                xCnt=0
                oCnt=0
        if xCnt >= k:
            hvalue= 100
            return hvalue
        if oCnt>=k:
            hvalue= -100
            return hvalue
    xCnt=0
    oCnt=0
    # check diagnal leftup to right down
    for i in range(0,n):
        for j in range(0,n):
            xCnt=0
            oCnt=0
            for m in range(0,n):
                if i+m<0 or i+m>=n or j+m<0 or j+m >=n:
                    continue
                if state[i+m,j+m] == 1:
                    xCnt+=1
                    oCnt=0
                elif state[i+m,j+m] == 0:
                    xCnt=0
                    oCnt+=1
                else:
                    xCnt=0
                    oCnt=0
            if xCnt >= k:
                hvalue= 100
                return hvalue
            if oCnt>=k:
                hvalue= -100
                return hvalue

        
    xCnt=0
    oCnt=0
    # check diagnal leftdown to rightup
    for i in reversed(range(0,n)):
        for j in range(0,n):
            xCnt=0
            oCnt=0
            for m in range(0,n):
                if i-m<0 or i-m>=n or j+m<0 or j+m >=n:
                    continue
                if state[i-m,j+m] == 1:
                    xCnt+=1
                    oCnt=0
                elif state[i-m,j+m] == 0:
                    xCnt=0
                    oCnt+=1
                else:
                    xCnt=0
                    oCnt=0
                if xCnt >= k:
                    hvalue= 100
                    return hvalue
                if oCnt>=k:
                    hvalue= -100
                    return hvalue
            
    return hvalue

def minimax(state, isMaxmazing, alpha, beta):
    global n,k
    hvalue=heuristic(state)
    if hvalue!=0:#someone won
        return hvalue,state

    empty_space=0
    for i in range(0,n):
        for j in range(0,n):
            if state[i,j]>1:
                empty_space+=1
                break
    if empty_space==0:#draw
        hvalue=0
        return hvalue,state

    returnState= state.copy()
    if isMaxmazing is True:
        maxEval=-np.inf
        for i in range(0,n):
            for j in range(0,n):
                if state[i,j]>1:# is empty
                    nextstate=state.copy()
                    nextstate[i,j]=1
                    Eval,Nstate=minimax(nextstate, not isMaxmazing, alpha, beta)

                    if Eval>maxEval:
                        maxEval=Eval
                        returnState=nextstate.copy()
                    alpha = max(alpha, Eval)
                    if alpha >= beta:
                        break

        return maxEval, returnState

    else:
        minEval=np.inf
        for i in range(0,n):
            for j in range(0,n):
                if state[i,j]>1:# is empty
                    nextstate=state.copy()
                    nextstate[i,j]=0

                    Eval, Nstate =minimax(nextstate, not isMaxmazing, alpha, beta)

                    if Eval < minEval:
                        minEval=Eval
                        returnState=nextstate.copy()
                    beta = min(beta, Eval)
                    if alpha >= beta:
                          break
        return minEval, returnState
    

def printState(state):
    global n,k
    for i in range(0,n):
        for j in range(0,n):
            if state[i,j]<=1:
                if state[i,j]==0:
                    print('o ',end='')
                else:
                    print('x ',end='')
            else:
                print('- ',end='')
        print('\n')


def main():
    global n,k,board,player_first
    # n=3
    # k=3
    # player_first='x'
    
    linepos=0
    if player_first == 'o':
        #read first
        while True:
            fileo=open(filename_o,'r')
            msg=fileo.readline()
            fileo.close()
            if len(msg)>=3:
                print("=======")
                print("x.py read : ",msg)
                readMove(msg)
                linepos+=1
                break

    
    while True:
        
        hvalue, state= minimax(board,True, -np.inf, np.inf)

        row=0
        col=0
        for i in range(0,n):
            for j in range(0,n):
                if state[i,j]<2 and board[i,j]>2:
                    row=i
                    col=j

        board[row,col]=1
        #write in file
        colname=chr(ord('a')+col)
        filex=open(filename_x,'a')
        filex.write('x'+str(row+1)+colname+'\n')
        filex.close()
        print('x'+str(row+1)+colname+'\n')
        printState(board)
        h=hvalue
        if h <0:
            print("o wins")
            return
        elif h>0:
            print("x wins")
            return
        else:
            empty_space=0
            for i in range(0,n):
                for j in range(0,n):
                    if state[i,j]>1:
                        empty_space+=1
                        break
            if empty_space==0:#draw
                print("draw")
                return

        #read file x to build board
        while True:
            fileo=open(filename_o,'r')
            content=fileo.readlines()
            fileo.close()
            length=len(content)
            if length >0:
                if len(content[length-1])<3:
                    continue
            if linepos >= length :
                continue
    
            msg=content[linepos]
            linepos+=1
            print("=======")
            print("x.py read : ",msg)
            readMove(msg)
            # filex.close()
            break
        #==================

        
        

def test():
    global n,k
    n=3
    k=3
    state=np.array( [[1,99, 1],[0, 0, 1],[99, 1, 0]])
    print(heuristic(state))
    printState(state)


import time
if __name__ == "__main__":
   
    start = time.time()
    
    n=int(sys.argv[1])
    k=int(sys.argv[2])
    player_first=sys.argv[3]

    #debug
    # n=2
    # k=2
    # player_first='o'
    main()

    
    end = time.time()
    print(end - start)
    # test()
