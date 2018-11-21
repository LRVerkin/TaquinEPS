import numpy as np



class Tile:

    def __init__(self,goal,state,env):
        self.goal = goal #goal Patch of Tile, will NOT change
        self.state = state #initial position of Tile, will change



    ##### KERNEL BEHAVIOURS (DOMAIN-INDEPENDENT) #####

    # def trySatisfaction(self):

    #     if agent can be satisfied:
    #         self.doSatisfaction()
    #     else:
    #         self.satisfactionAggression()


    # def flee(self,constraint):

    #     if agent peut fuir:
    #         self.doFlee()
    #     else:
    #         self.fleeAggression(constraint)





    ##### APPLICATION BEHAVIOURS (DOMAIN-DEPENDENT) #####

    # def doSatisfaction(self):


    # def satisfactionAggression(self):


    # def doFlee(self):



    # def fleeAggression(self):



    def ManhattanDistanceGoal(self):
        self.goal.ManhattanGoal(self.state.number,self.goal.number,0)




class Patch:
    
    def __init__(self, position, taille, env,occupied = False):
        
        self.env = env #just to call getAcquaintances
        self.position = position #tuple (x,y)
        self.occupied = occupied #if a Place has a tile on it
        self.number = taille*self.position[0] + self.position[1]+1

        self.goalWaves = {self.number:0} #dict containing distances to all goals asked for
        #format: {goal:distance}
        self.blankWave = None #distance to the current blank Patch, starts at none

    def occupationChange(self):
        self.occupied = 1-self.occupied
        if self.occupied = False: #if this is now the blank Patch
            print("you still have to do the Manhattan distance from the blank Patch!")
            #need to code a function that will send a Manhattan wave to update
            # self.blankWave for all Patches
        

    def ManhattanWave(self,tile,start):
        acquaintances = env.getAcquaintances(self.number)
        for patch in acquaintances:
            if patch == tile.state:
                return 

    def ManhattanGoal(self,askingPatch,finalGoal,start):
        acquaintances = self.env.getAcquaintances(self.number) #neighbour patches
        print("at patch",self.position)
        empty_ac = []
        for direction,ac in acquaintances.items():
            if finalGoal not in ac.getGoalWaves().keys(): #if this acquaintance hasn't been reached by the wave
                print("acquaintance to update:",ac.position)
                empty_ac.append(ac)
                ac.updateGoalWaves(finalGoal,start+1)
                print("it now has distance",start+1)
        for ac in empty_ac:
            if ac.number != askingPatch:
                ac.ManhattanGoal(askingPatch,finalGoal,start+1)


    def getGoalWaves(self):
        return self.goalWaves

    def updateGoalWaves(self,goal,value):
        self.goalWaves[goal] = value







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
                
                self.grid[0, i, j] = Patch( position = (i,j), taille = taille, occupied = True,env=self)
                
                self.positions[self.grid[0, i, j].number] = (i,j) #associate a number to its position on the board
                #just so we don't have to reuse the formula all the time

        for i in range(self.grid.shape[1]):
            for j in range(self.grid.shape[2]):
                #initialize Tiles
                goal = self.positions[self.numbers[i,j]+1]
                self.grid[1, i, j] = Tile(self.grid[0,goal[0],goal[1]], self.grid[0, i, j], self)
        
        #we randomly delete an EcoAgent so others will have room to move around
        #rdtuple =  (np.random.choice(range(taille)), np.random.choice(range(taille)))
        rdtuple = (1,1)
        self.grid[1, rdtuple[0],rdtuple[1]] = None
        self.grid[0, rdtuple[0],rdtuple[1]].occupied = False
    

    def show(self):
        '''
        show the Tiles goals over the grid
        '''
        for i in range(self.taille):
            row = '|'
            for j in range(self.taille):
                if self.grid[1,i,j] != None:
                    row += ' '+str(self.grid[1,i,j].goal)+'  | '
                else :
                    row += '    | '
            print(row)
        
    
    def getAcquaintances(self, placeNumber):
        '''returns PATCHES (not Tiles)
            around the Patch with placeNumber
        '''
        x = self.positions[placeNumber][0]
        y = self.positions[placeNumber][1]
        acquaintances = {}
        directions = ["up","left","down","right"]
        for indice in [-1, 1]:
            try:
                if indice + x >= 0:
                    acquaintances[directions[indice+1]] = self.grid[0,x+indice,y]
            except IndexError: 
              print("Sortie de la grille sur y")
            try:
                if y + indice >= 0:
                    acquaintances[directions[indice+2]] = self.grid[0,x,y+indice]
            except IndexError:
              print("Sortie de la grille sur x")
        return acquaintances



e = Environnement()
e.positions
#e.getAcquintances(1)['up'].place.position
# print(e.getAcquaintances(2))
# e.show()
# e.getAcquaintances(1)['right'].tryEscape()
# print("change")
# e.show()

goal = e.grid[1,0,0].goal
print("but de l'agent en haut a gauche est",goal.position)
e.grid[1,0,0].ManhattanDistanceGoal()
print(e.grid[0,1,0].goalWaves[goal.number])