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
        
    def acquintancesPerception(self):
        self.env.getAcquintances(self.placePerception)
        
    def updateState(self):
        if self.placePerception() == self.goal:
            self.state = 'satisfied'
        return self.state
        
    def placePerception(self):
        return self.place.number
        
        
        
        
class Place:
    
    def __init__(self, number, occupied, position):
        
        self.number = number
        self.occupied = occupied
        
class Environnement:
    
    def __init__(self, taille = 3):
        
        self.grid = np.empty((2, taille, taille), dtype = object)
        
        self.numbers = np.copy(np.random.choice(taille**2+1, taille**2+1, replace = False))
        self.numbers.resize((taille, taille))
        
        self.places = np.array(range(1,taille**2+1))
        self.places.resize((taille, taille))
        
        self.positions = {}
        
        for i in range(self.grid.shape[1]):
            for j in range(self.grid.shape[2]):
                self.positions[Place(self.places[i,j])] = (i,j)
                self.grid[0, i, j] = Place(self.places[i,j])
                self.grid[1, i, j] = EcoAgent(self.numbers[i,j], self)
                
        rdtuple =  (np.random.choice(range(taille)), np.random.choice(range(taille)))
        self.grid[1, rdtuple[0],rdtuple(1)] = None
        self.grid[0, rdtuple[0],rdtuple(1)].occupied = False
        
    
    def getAcquintances(self, placeNumber):
        position = self.positions[placeNumber]
        for indice in [-1, 1]:
            

e = Environnement()
