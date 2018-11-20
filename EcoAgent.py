# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:18:49 2018

@author: Océane
"""

import numpy as np

class EcoAgent:
    
    def __init__(self, goal, place, env):
        
        self.goal = goal
        self.state  = ""
        self.acquintances = []
        self.env = env
        self.place = place
        self.hasPredator = False

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
        self.occupied = occupied
        self.number = taille*self.position[0] + self.position[1]+1
        
class Environnement:
    
    def __init__(self, taille = 3):
        
        self.grid = np.empty((2, taille, taille), dtype = object)
        self.taille = taille
        self.numbers = np.copy(np.random.choice(taille**2, taille**2, replace = False))
        self.numbers.resize((taille, taille))
        
        #self.places = np.array(range(1,taille**2+1))
        #self.places.resize((taille, taille))
        
        self.positions = {}
        
        for i in range(self.grid.shape[1]):
            for j in range(self.grid.shape[2]):
                
                self.grid[0, i, j] = Place( position = (i,j), taille = taille, occupied = True)
                
                self.positions[self.grid[0, i, j].number] = (i,j)
                self.grid[1, i, j] = EcoAgent(self.numbers[i,j]+1, self.grid[0, i, j], self)
        
        #we randomly delete a tile
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
print(e.getAcquintances(8))
e.show()
