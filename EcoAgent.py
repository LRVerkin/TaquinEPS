# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:18:49 2018

@author: Océane
"""

import numpy as np

class EcoAgent:
    '''
    all tiles will be EcoAgents
    note: places where tiles will be are NOT EcoAgents and have their own class!
    '''
    def __init__(self, goal, place, env):
        
        self.goal = goal
        self.state  = "" #satisfied or not
        self.acquintances = [] #tiles surrounding this one
        self.env = env
        self.place = place #its place on the board
        self.hasPredator = False #has it been attacked?

    def acquintancesPerception(self):
        self.env.getAcquintances(self.placePerception)
        

    def updateState(self):
        if self.placePerception() == self.goal:
            self.state = 'satisfied'
        return self.state
        
    def placePerception(self):
        return self.place.number
    
    def trySatisfaction(self):
        if self.has_predator:
            self.tryEscape()
        else:
            self.updateState()
        
    def isAttacked(self):
        self.hasPredator = True
        
    #def tryEscape(self):
        
        
        
class Place:
    
    def __init__(self, position, taille, occupied = False):
        
        self.position = position #tuple (x,y)
        self.occupied = occupied #if a Place has a tile on it
        self.number = taille*self.position[0] + self.position[1]+1
        


class Environnement:
    ''' 
    class defining the board
    '''
    
    def __init__(self, taille = 3):
        
        self.taille = taille
        self.grid = np.empty((2, taille, taille), dtype = object) #2 2D grids, grid[0] contains Places, grid[1] contains EcoAgents
        #self.numbers will be used to assign random goal numbers to EcoAgents
        self.numbers = np.copy(np.random.choice(taille**2, taille**2, replace = False))
        self.numbers.resize((taille, taille))
        
        #self.places = np.array(range(1,taille**2+1))
        #self.places.resize((taille, taille))
        
        self.positions = {} #so we remember which Place on 
        
        for i in range(self.grid.shape[1]):
            for j in range(self.grid.shape[2]):
                
                self.grid[0, i, j] = Place( position = (i,j), taille = taille, occupied = True)
                
                self.positions[self.grid[0, i, j].number] = (i,j) #associate a number to its position on the board
                #just so we don't have to reuse the formula all the time

                #initialize EcoAgents
                self.grid[1, i, j] = EcoAgent(self.numbers[i,j]+1, self.grid[0, i, j], self)
        
        #we randomly delete an EcoAgent so others will have room to move around
        rdtuple =  (np.random.choice(range(taille)), np.random.choice(range(taille)))
        print(rdtuple)
        self.grid[1, rdtuple[0],rdtuple[1]] = None
        self.grid[0, rdtuple[0],rdtuple[1]].occupied = False
    

    def show(self):
        '''
        show the ecoTiles goals over the grid
        '''
        for i in range(self.taille):
            row = '|'
            for j in range(self.taille):
                if self.grid[1,i,j] != None:
                    row += ' '+str(self.grid[1,i,j].goal)+'  | '
                else :
                    row += '    | '
            print(row)
        
    
    def getAcquintances(self, placeNumber):
        x = self.positions[placeNumber][0]
        y = self.positions[placeNumber][1]
        acquaintances = {}
        directions = ["up","left","down","right"]
        for indice in [-1, 1]:
            try:
                if indice + x >= 0:
                    acquaintances[directions[indice+1]] = self.grid[1,x+indice,y]
            except IndexError: 
              print("Sortie de la grille sur y")
            try:
                if y + indice >= 0:
                    acquaintances[directions[indice+2]] = self.grid[1,x,y+indice]
            except IndexError:
              print("Sortie de la grille sur x")
        return acquaintances

        

e = Environnement()
e.positions
#e.getAcquintances(1)['up'].place.position
print(e.getAcquintances(1))
e.show()
