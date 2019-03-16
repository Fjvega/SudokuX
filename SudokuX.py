# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:00:03 2019

@author: Francisco
"""

from simpleai.search import SearchProblem, astar
import numpy as np

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
    
 
def PossibleInDiagPrin(table):
    _myList= []
    possibility = list(range(1,7))
    for x in range (0,6):
        if(table[x][x]!=0):
            _myList.append(table[x][x])
    
    return set(possibility)-set(_myList)  

def PossibleInDiagSec(table):
    _myList= []
    possibility = list(range(1,7))
    for x in range (0,6):
        for y in range (0,6):
            if(table[x][y]!=0 and (x+y+1)==6):
                _myList.append(table[x][y])
    return set(possibility)-set(_myList)  

def PossibleInGroup(table,row,column):
    _myList= []
    possibility = list(range(1,7))     
    
    if(row<=1 and column<=2):
        for y in range (0,2):
            for x in range(0,3):
                if(table[x][y]!=0):
                  _myList.append(table[x][y])
                
    if(row<=1 and column>2):
        for y in range (0,2):
            for x in range(3,6):
                if(table[x][y]!=0):
                  _myList.append(table[x][y])
    
    
    if(row>1 and row <4 and column<=2):
        for y in range (2,4):
            for x in range(0,3):
                if(table[x][y]!=0):
                  _myList.append(table[x][y])
    
    if(row>1 and row <4 and  column>2):
        for y in range (2,4):
            for x in range(3,6):
                if(table[x][y]!=0):
                  _myList.append(table[x][y])
    
    
    
    
    if(row>5 and column<=2):
        for y in range (4,6):
            for x in range(0,3):
                if(table[x][y]!=0):
                  _myList.append(table[x][y])
    
    if(row>5 and column>2):
        for y in range (4,6):
            for x in range(3,6):
                if(table[x][y]!=0):
                  _myList.append(table[x][y])
    
    
    return set(possibility)-set(_myList)  


def IsComplete(table):
    for x in range (0,6):
        for y in range (0,6):
            if(table[x][y]==0):
             return False
    
    return True

def NextEmptyCell(table):
    for x in range (0,6):
        for y in range (0,6):
            if(table[x][y]==0):
             return x,y
    

"""
SIMPLE IA CODE
"""


class SudokuXProblem(SearchProblem):
    
    def actions(self,state):
        temp= StringToArray(state)
        row,column = NextEmptyCell(temp)
        numRow=PossibleInRow(row,temp)
        numColumn=PossibleInColumn(column,temp)
        numGroup=PossibleInGroup(temp,row,column)
       
        
       
        if row == column :
            
            numDiag =  PossibleInDiagPrin(temp)
            possibility = numRow.intersection(numColumn,numGroup,numDiag)
            
            return list(possibility)
        
        elif row + column + 1 == 6:
            
            numDiag = PossibleInDiagSec(temp)
            possibility = numRow.intersection(numColumn,numGroup,numDiag)
           
            return list(possibility)
        else :
            possibility=numRow.intersection(numColumn,numGroup)
           
            return list(possibility)
        
        
    def result(self,state,action):
        
        temp= StringToArray(state)
        row,column = NextEmptyCell(temp)
  
    
        print(action)
        temp[row][column]=action
        
        state= ArrayToString(temp)
        
        print("//new Array")
        print(state)
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
                
   
     
initialState="1,0,0,0,4,0;6,0,0,2,0,0;0,0,0,0,0,4;0,0,2,0,0,0;0,3,1,0,0,0;4,0,0,0,3,2"
print(initialState)
print(ArrayToString(StringToArray(initialState)))

my_problem = SudokuXProblem(initial_state=initialState)
result = astar(my_problem)


print(result)
"""
for action, state in result.path():
    print('Insert number', action)
print(state)
"""
    