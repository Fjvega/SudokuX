# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:00:03 2019

@author: Francisco
"""

from simpleai.search import SearchProblem, astar
"""
from __future__ import print_function
"""
import numpy as np
import time

"""
CONDICIONES Y UTILIDADES
"""
def StringToArray(string):
    my_list =np.zeros((6,6))
    row=0
    column=0
    
    for x in string:
        if(x==','):
            pass
        else:
            if(x==";"):
                
                 row=row+1
                 column=0
            else:
                my_list[row,column]=x
                column=column+1
               
        
        
    return my_list

def ArrayToString(my_list):
    converter =""
    for x in range (0,6):
        for  y in range (0,6):
            if(y<5):
                converter=converter+str(int(my_list[x][y]))+","
            else:
                if(x<5):
                    converter=converter+str(int(my_list[x][y]))+";"
                else:
                     converter=converter+str(int(my_list[x][y]))
    return converter   

def PossibleInRow(row,table):
    
    possibility = list(range(1,7))
    _myList = []
    for x in range (0,6):
        if(table[row][x]!=0):
            _myList.append(table[row][x])
    
    return set(possibility)-set(_myList)
 
def PossibleInColumn(column,table):
    
    possibility = list(range(1,7))
    _myList = []
    for x in range (0,6):
        if(table[x][column]!=0):
            _myList.append(table[x][column])
    
    return set(possibility)-set(_myList)       
    
 
def PossibleInDiag(temp, row, col):
    diag="1,0,0,0,0,2;0,1,0,0,2,0;0,0,1,2,0,0;0,0,2,1,0,0;0,2,0,0,1,0;2,0,0,0,0,1"
    tg= StringToArray(diag)
    selec=tg[row][col]
    emptySet={}
    Poss= list(range(1,7))
    Actual=[]
    if selec != 0:
        for x in range(0,6):
            for y in range(0,6):
                if selec == tg[x][y] and temp[x][y] != 0:
                    Actual.append(temp[x][y])
                    
        return set(Poss)-set(Actual)
    else:
        return emptySet

def PossibleInGroup(temp,row,col):
    groups="1,1,1,2,2,2;1,1,1,2,2,2;3,3,3,4,4,4;3,3,3,4,4,4;5,5,5,6,6,6;5,5,5,6,6,6"
    tg= StringToArray(groups)
    selec=tg[row][col]
    
    Poss= list(range(1,7))
    Actual=[]
    
    for x in range(0,6):
        for y in range(0,6):
            if selec == tg[x][y] and temp[x][y] != 0:
                Actual.append(temp[x][y])
    return set(Poss)-set(Actual)  


            

            
            
def IsComplete(table):
    if table.all() == 0:
        return False
    return True
    '''for x in range (0,6):
        for y in range (0,6):
            if(table[x][y]==0):
                return False
    
    return True'''

def BestMatch(temp):
    """
    temp= StringToArray(state)
    """
    bestmatch = 999
    rr=0
    rc=0
    for row in range (0,6):
        for column in range (0,6):
            if(temp[row][column]==0):
                
                numRow=PossibleInRow(row,temp)
                numColumn=PossibleInColumn(column,temp)
                numGroup=PossibleInGroup(temp,row,column)
                numDiag = PossibleInDiag(temp,row,column)
                if numDiag.__len__() != 0:
                    possibility=numRow.intersection(numColumn,numGroup,numDiag)
                else:
                    possibility=numRow.intersection(numColumn,numGroup)
                
                
                if(possibility.__len__()<=bestmatch and possibility.__len__()>0):
                    bestmatch= possibility.__len__()
                    rr=row;
                    rc=column
    
    return rr,rc
    
def NextEmptyCell(table):
    
    for row in range (0,6):
        for column in range(0,6):
            if(table[row][column]==0):
                return row,column
            
            
"""
SIMPLE IA CODE
"""


class SudokuXProblem(SearchProblem):
    
    def actions(self,state):
        temp= StringToArray(state)
        
        """
        row,column = BestMatch(temp)
        """
        
        
        row,column = NextEmptyCell(temp)
        
        numRow=PossibleInRow(row,temp)
        numColumn=PossibleInColumn(column,temp)
        numGroup=PossibleInGroup(temp,row,column)
        numDiag = PossibleInDiag(temp,row,column)
        
        print("NEW STATE")
        print("Se va a expandir en la posición :")
        print(str(row)+","+str(column))
        
        
        if numDiag.__len__() != 0:
            possibility=numRow.intersection(numColumn,numGroup,numDiag)
        else:
            possibility=numRow.intersection(numColumn,numGroup)
        
        print("Estado actual")
        print(StringToArray(state))
        print("Con las siguientes posibilidades")
        print(list(possibility))
        
        return list(possibility)
        
        
    def result(self,state,action):
        temp= StringToArray(state)
        
        """
        row,column = BestMatch(temp)
        """
        row,column = NextEmptyCell(temp)
        
        temp[row][column]=action
        
        state= ArrayToString(temp)
        return state
        
        
    def cost(self,state,action,state2):
        return 1
    
    def is_goal(self, state):
        temp= StringToArray(state)
        return IsComplete(temp)

    def heuristic(self, state):
        
        h=0
        
        temp= StringToArray(state)
        for x in range (0,6):
            for y in range(0,6):
                if temp[x][y] == 0 :
                    h=h+1
        return h
                
   
     
is1="0,5,0,0,0,0;6,0,3,0,0,0;0,3,0,0,0,0;0,0,0,0,6,0;0,0,0,6,0,1;0,0,0,0,2,0"
is2="0,0,1,0,0,0;0,0,0,6,0,0;1,0,0,0,3,0;0,4,0,0,0,2;0,0,2,0,0,0;0,0,0,2,0,0"
is3="0,0,3,0,0,0;1,0,0,0,0,0;0,2,0,0,0,1;5,0,0,0,4,0;0,0,0,0,0,4;0,0,0,5,0,0"
is4="0,0,0,3,0,0;0,0,3,0,0,0;2,0,0,0,5,0;0,3,0,0,0,1;0,0,0,6,0,0;0,0,4,0,0,0"
is5="0,2,0,0,0,0;4,0,6,0,0,0;0,1,0,0,0,0;0,0,0,0,4,0;0,0,0,4,0,5;0,0,0,0,3,0"



millis = int(round(time.time() * 1000))
my_problem = SudokuXProblem(initial_state=is1)
result = astar(my_problem)

print(result)

millis2 = int(round(time.time() * 1000))

print(millis2-millis)
"""
for action, state in result.path():
    print('Insert number', action)
    print(StringToArray(state))
"""    
   