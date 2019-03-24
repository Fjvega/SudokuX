# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:00:03 2019

@author: Francisco Vega & Alejandro Ortega
"""

from simpleai.search import SearchProblem, astar
import numpy as np
import time

"""
CONDICIONES Y UTILIDADES
"""
#Conversion String a Matriz
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

#Conversion Matriz a String
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
 
#Condicional Filas
def PossibleInRow(row,table):
    possibility = list(range(1,7))
    _myList = []
    for x in range (0,6):
        if(table[row][x]!=0):
            _myList.append(table[row][x])
    
    return set(possibility)-set(_myList)
 
#Condicional Columna
def PossibleInColumn(column,table):
    possibility = list(range(1,7))
    _myList = []
    for x in range (0,6):
        if(table[x][column]!=0):
            _myList.append(table[x][column])
    
    return set(possibility)-set(_myList)       
    
#Condicional Diagonales
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

#Condicional Grupos
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

#Verificacion de Estado Objetivo
def IsComplete(table):
    if table.all() == 0:
        return False
    return True

#Buscador de primera casilla vacia (Heuristica 1)
def NextEmptyCell(table):
    
    for row in range (0,6):
        for column in range(0,6):
            if(table[row][column]==0):
                return row,column
            

#Buscador de casilla con menos posibilidades (Heuristica 2)
def BestMatch(temp):

    bestmatch = 999
    rr=0
    rc=0
    rpossibility = {}
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
                    rpossibility =possibility
    
    return rr,rc,rpossibility
     
    
"""
SIMPLE IA CODE
"""
#SIMPLE IA Code para Heuristica 1
class SudokuXProblem(SearchProblem):
    
    def actions(self,state):
        temp= StringToArray(state)
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
    
#SIMPLE IA Code para Heuristica 2
class SudokuXProblem2(SearchProblem):
    
    def actions(self,state):
        temp= StringToArray(state)
        
        
        row,column,possibility = BestMatch(temp)
        

      
        print("NEW STATE")
        print("Se va a expandir en la posición :")
        print(str(row)+","+str(column))
        print("Estado actual")
        print(StringToArray(state))
        print("Con las siguientes posibilidades")
        print(list(possibility))
        
        return list(possibility)
        
        
    def result(self,state,action):
        temp= StringToArray(state)
        
        
        row,column,possibility = BestMatch(temp)
        
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
                
   
     
        
    
#Casos de Prueba Sudoku X
is1="0,5,0,0,0,0;6,0,3,0,0,0;0,3,0,0,0,0;0,0,0,0,6,0;0,0,0,6,0,1;0,0,0,0,2,0"
is2="0,0,1,0,0,0;0,0,0,6,0,0;1,0,0,0,3,0;0,4,0,0,0,2;0,0,2,0,0,0;0,0,0,2,0,0"
is3="0,0,3,0,0,0;1,0,0,0,0,0;0,2,0,0,0,1;5,0,0,0,4,0;0,0,0,0,0,4;0,0,0,5,0,0"
is4="0,0,0,3,0,0;0,0,3,0,0,0;2,0,0,0,5,0;0,3,0,0,0,1;0,0,0,6,0,0;0,0,4,0,0,0"
is5="0,2,0,0,0,0;4,0,6,0,0,0;0,1,0,0,0,0;0,0,0,0,4,0;0,0,0,4,0,5;0,0,0,0,3,0"








#HEURISTICA DE LA PRIMERA CASILLA VACIA 
millis_h1 = int(round(time.time() * 1000))
my_problem2 = SudokuXProblem(initial_state=is2)
result1 = astar(my_problem2)
millis_h12 = int(round(time.time() * 1000))
Tiempo_Primera_Vacia =millis_h12-millis_h1


#HEURISTICA CASILLA CON MENOS POSIBILIDADES
millis_h2 = int(round(time.time() * 1000))
my_problem = SudokuXProblem2(initial_state=is2)
result2 = astar(my_problem)
millis_h22 = int(round(time.time() * 1000))
Tiempo_Menos_Posibilidades =millis_h22-millis_h2



#Muestreo de resultados obtenidos
print('Tiempo de la 1 heuristica ',Tiempo_Primera_Vacia)
print(result1)
print('Tiempo de la 2 heuristica ',Tiempo_Menos_Posibilidades)
print(result2)


#En caso de ver cual fue el camino para la solución con la heuristica 1 descomente el siguiente bloque
'''
for action, state in result1.path():
    print('Insert number', action)
    print(StringToArray(state))
 
'''

#En caso de ver cual fue el camino para la solución con la heuristica 2 descomente el siguiente bloque
'''
for action, state in result2.path():
    print('Insert number', action)
    print(StringToArray(state))
'''
