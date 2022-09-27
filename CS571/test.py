import numpy as np
from x import heuristic

def heuristic000(state):
    winflag=False
    hvalue=0
    xCnt=0
    oCnt=0
    # check rows
    for i in range(0,n):
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
            winflag=True
            hvalue= 100
            break
        if oCnt>=k:
            winflag=True
            hvalue= -100
            break
    if winflag:
        return hvalue
    xCnt=0
    oCnt=0
    # check cols
    for j in range(0,n):
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
            winflag=True
            hvalue= 100
            break
        if oCnt>=k:
            winflag=True
            hvalue= -100
            break
    if winflag:
        return hvalue
    xCnt=0
    oCnt=0
    # check diagnal leftup to right down
    for i in range(0,n):
        for j in range(0,n):
            if winflag:
                break
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
                winflag=True
                hvalue= 100
                break
            if oCnt>=k:
                winflag=True
                hvalue= -100
                break
    if winflag:
        return hvalue
    xCnt=0
    oCnt=0
    # check diagnal leftdown to rightup
    for i in range(0,n):
        for j in range(0,n):
            if winflag:
                break
            for m in range(0,n):
                if n-i-m<0 or n-i-m>=n or j+m<0 or j+m >=n:
                    continue
                if state[n-i-m,j+m] == 1:
                    xCnt+=1
                    oCnt=0
                elif state[n-i-m,j+m] == 0:
                    xCnt=0
                    oCnt+=1
                else:
                    xCnt=0
                    oCnt=0
            if xCnt >= k:
                winflag=True
                hvalue= 100
                break
            if oCnt>=k:
                winflag=True
                hvalue= -100
                break
            
    return hvalue

def printState(state):
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

if __name__=="__main__":
    n=3
    k=3
    state=np.array( [[1,0, 1],[0, 1, 0],[0, 1, 1]])
    print(heuristic(state))
    # for i in reversed(range(0,n)):
    #     print (i)
    printState(state)