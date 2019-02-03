import numpy as np



class Tile:

    def __init__(self,goal,patch):
        self.goal = goal #goal Patch of Tile, will NOT change
        self.cur_patch = patch #initial position of Tile, will change


    def isSatisfied(self):
        if self.cur_patch == self.goal:
            return True
        else:
            return False

    ##### KERNEL BEHAVIOURS (DOMAIN-INDEPENDENT) #####

    def trySatisfaction(self,constraints_ = []):


        print("#### entered trySatisfaction with constraints:")
        print([p.number for p in constraints_])

        self.cur_patch.env.show()
        if not self.isSatisfied():
            # find patches nearest its goal

            print("Tile ",self.goal.number,"on Patch ",self.cur_patch.number," is not satisfied")
            # if self.goal.number not in self.cur_patch.getGoalWaves().keys():
            #     self.ManhattanDistanceGoal()
            destinations_goal = self.cur_patch.closestNeighbToGoal(self.goal,'all',constraints_)
            #print("destinations closest to goal for tile ",self.goal.number," are patches:")
            #print([p.number for p in destinations_goal])
              # among those, choose patch nearest to blank patch
            destinations = self.cur_patch.closestNeighbToBlank(destinations_goal)
            #print("of those, destinations closest to blank are:")
            #print([p.number for p in destinations])
            destination_patch = np.random.choice(destinations)
            while not destination_patch.isFree():
                constraints_.append(self.cur_patch)
                print("constraints for aggro of ",destination_patch.number,"by patch",self.cur_patch.number,"are:")
                print([p.number for p in constraints_])
                self.satisfactionAggression(destination_patch, constraints_,self)

            print("left while loop for tile ",self.goal.number)
            self.doSatisfaction(destination_patch)
            if destination_patch == self.goal:
                self.cur_patch.env.changePriorSatisf(self.cur_patch)
                self.cur_patch.env.findNextUnsatisf()
            else:
                self.cur_patch.env.findNextUnsatisf()
                
        else:
            self.cur_patch.env.findNextUnsatisf()

    def flee(self,constraints,initiator):


        print("Tile ",self.goal.number," #### entered flee with constraints:")
        print([p.number for p in constraints])
        self.cur_patch.env.show()
        print("Tile ",self.goal.number,"on Patch",self.cur_patch.number,"needs to flee!")
        # 1) remove from possible patches the ones given as constraints
        # if self.goal.number not in self.cur_patch.getGoalWaves().keys():
        #         self.ManhattanDistanceGoal()
        # if self.cur_patch.env.prior_satisf != None:
        #     constraints.append(self.cur_patch.env.prior_satisf)
        destinations_blank = self.cur_patch.closestNeighbToBlank('all',constraints)
        if len(destinations_blank) == 0:
            print("in flee: no destinations_blank left!")
            return
        #print("destinations closest to blank for tile ",self.goal.number," are patches:")
        #print([p.number for p in destinations_blank])
        # 2) if goal patch of current tile is in remaining patches: choose it
        if self.goal in destinations_blank:
            #print("going straight to blank!")
            destination_patch = self.goal
        # 3) among patches nearest to the blank, choose the one nearest to the goal
        else:
            destinations = self.cur_patch.closestNeighbToGoal(self.goal,destinations_blank)
            #print("of those, destinations closest to goal are:")
            #print([p.number for p in destinations])
            destination_patch = np.random.choice(destinations)
         
        while not destination_patch.isFree():
            constraints_ = [self.cur_patch]
            if self.cur_patch.env.prior_satisf != None:
                constraints_.append(self.cur_patch.env.prior_satisf)
            self.fleeAggression(destination_patch,constraints_)

        self.doFlee(destination_patch)
        if destination_patch == self.goal:
            self.cur_patch.env.changePriorSatisf(self.cur_patch)
        # constr = []
        # if self.cur_patch.env.prior_satisf != None:
        #     constr.append(self.cur_patch.env.prior_satisf)
        # initiator.trySatisfaction(constr)




    ##### APPLICATION BEHAVIOURS (DOMAIN-DEPENDENT) #####


    # SATISFATION BEHAVIOURS 

    def doSatisfaction(self,destination_patch, display=True):
        '''
        tile moves on destination patch
        update destination patch to say it now has a tile
        '''
        if display:
            print("#### entered doSatisfaction")
            print(self.goal.number," is moving to patch ",destination_patch.number)
        self.cur_patch.occupationChange(None)
        self.cur_patch = destination_patch
        self.cur_patch.occupationChange(new_tile = self)




    def satisfactionAggression(self,destination_patch,constraints,initiator):
        '''
        attack tile on destination_patch
        '''

        print("#### entered satisfactionAggression with constraints")
        print([p.number for p in constraints])
        destination_patch.attackTile(constraints,self)
        if self.goal.env.prior_satisf != None:
            initiator.trySatisfaction([self.goal.env.prior_satisf])
        else:
            initiator.trySatisfaction([])

    # FLEE BEHAVIOURS

    def doFlee(self,destination_patch):
        '''
        tile flees to destination_patch
        '''

        print("#### entered doFlee")
        print(self.goal.number," is moving to patch ",destination_patch.number)
        self.cur_patch.occupationChange(None)
        self.cur_patch = destination_patch
        self.cur_patch.occupationChange(new_tile = self)
        if self.isSatisfied():
            self.cur_patch.env.changePriorSatisf(self.cur_patch)


    def fleeAggression(self,destination_patch,constraints):
        '''attack tile on destination_patch
        '''

        print("#### entered fleeAggression with constraints:")
        print([p.number for p in constraints])
        destination_patch.attackTile(constraints,self)


    def ManhattanDistanceGoal(self):
        ''' 
        ask goal patch to send a Manhattan Wave to current patch
        '''
        self.goal.ManhattanGoal(self.cur_patch,goal.number,0)



#######################################################################
#######################################################################


class Patch:
    
    def __init__(self, position, taille, env, tile):
        
        self.env = env #just to call getAcquaintances
        self.position = position #tuple (x,y)
        self.tile = tile #if a Place has a tile on it
        self.taille = taille
        self.number = taille*self.position[0] + self.position[1]+1

        self.goalWaves = {self.number:0} #dict containing distances to all goals asked for
        #format: {goal:distance}
        self.blankWave = None #distance to the current blank Patch, starts at 
        #self.distanceKnown = False


    def occupationChange(self,new_tile = None):
        self.tile = new_tile
        if new_tile == None:
            self.env.blankPatch = self
            self.MBToNone()


    def isFree(self):
        if self.tile == None:
            return True
        else:
            return False


    def attackTile(self,constraints,initiator):
        '''
        tells current tile to flee,
        gives it constraints aka patches to avoid
        '''
        self.tile.flee(constraints,initiator)


    def closestNeighbToGoal(self,goal,chooseFrom,constraints = []):
        '''
        returns list of patches that are closest to goal Patch
        '''
        closest = []
        minDist = (self.taille-1)*2
        if chooseFrom == 'all':
            acquaintances = list(self.env.getAcquaintances(self.number).values())
        else:
            acquaintances = chooseFrom

        for c in constraints:
            if c in acquaintances:
                acquaintances.remove(c)

        for ac in acquaintances:
            #print("acquaintance is ",ac.number)
            #this ac doesn't know its distance to goal patch: get it
            if self.tile.goal.number not in ac.getGoalWaves().keys():
                #print("Patch ",ac.number," doesn't know its distance to",self.tile.goal.number,"...")
                ac.ManhattanGoal(ac,self.tile.goal.number,0)
            if ac.getGoalWaves()[self.tile.goal.number] <= minDist:
                minDist = ac.getGoalWaves()[self.tile.goal.number]

        for ac in acquaintances:
            #print("for Patch ",ac.number," distance to goal is ",ac.getGoalWaves()[self.tile.goal.number])
            if ac.getGoalWaves()[self.tile.goal.number] == minDist:
                closest.append(ac)

        return closest

    def closestNeighbToBlank(self,chooseFrom,constraints = []):
        '''
        returns list of patches that are closest to Blank Patch
        '''
        closest = []
        minDist = (self.taille-1)*2
        if chooseFrom == 'all':
            acquaintances = list(self.env.getAcquaintances(self.number).values())
        else:
            acquaintances = chooseFrom


        for c in constraints:
            if c in acquaintances:
                acquaintances.remove(c)


        for ac in acquaintances:
            ac.ManhattanBlank()
            #print("for ",ac.number,", dist to blank is ",ac.blankWave)
            if ac.blankWave == None:
                minDist = 0
                break
            elif ac.blankWave < minDist:
                minDist = ac.blankWave

        for ac in acquaintances:
            if ac.blankWave == minDist:
                closest.append(ac)
            if ac.blankWave == None:
                closest = [ac]

        return closest


    ####### MANHATTAN METHODS #######
    def ManhattanBlank(self,distance = 0):
        ''' 
        update self.blankWave so it will contain
        distance from this Patch to current blank Patch
        '''

        #if blank Patch has changed, turn self.BlankNode back to None
        # if self.tile == None and distance == 0:
        #     print("### in MANHATTANBLANK, blank patch is",self.number)
        #     self.MBToNone()
        #     self.blankWave = 0


        if distance == 0:
            self.env.blankPatch.blankWave = 0
            acquaintances = self.env.getAcquaintances(self.env.blankPatch.number)
        else:
            acquaintances = self.env.getAcquaintances(self.number)

        for ac in acquaintances.values():
            if ac.blankWave == None or ac.blankWave > distance+1:
                ac.blankWave = distance+1
                ac.ManhattanBlank(distance+1)


    def MBToNone(self):
        self.blankWave = None
        acquaintances = self.env.getAcquaintances(self.number)
        for direction,ac in acquaintances.items():
            if ac.blankWave != None:
                ac.MBToNone()
        

    # def ManhattanGoal(self,askingPatch,finalGoal,start):
    #     '''
    #     update self.goalWaves so this Patch contains 
    #     Manhattan distance from finalGoal
    #     '''
    #     print("## ANALYZING MANHATTANDISTANCE to goal ",finalGoal," for patch ",askingPatch.number)
    #     if finalGoal in askingPatch.getGoalWaves().keys():
    #             return ""
    #     if start==0:
    #         acquaintances = self.env.getAcquaintances(finalGoal) #neighbour patches
    #     else:
    #         acquaintances = self.env.getAcquaintances(self.number)
    #     empty_ac = []
    #     for direction,ac in acquaintances.items():
    #         print("    PATCH ",ac.number)
    #         if finalGoal not in ac.getGoalWaves().keys(): #if this acquaintance hasn't been reached by the wave
    #             print("doesn't have its distance to ",finalGoal)
    #             empty_ac.append(ac)
    #             ac.updateGoalWaves(finalGoal,start+1)
    #             print("now patch",ac.number,"'s distance to patch",finalGoal," is ",str(start+1))
    #             if ac.number == askingPatch.number:
    #                 break
    #             #print("it now has distance",start+1)
    #         elif finalGoal not in askingPatch.getGoalWaves().keys():
    #             print("going after",ac.number)
    #             empty_ac.append(ac)

    #     for ac in empty_ac:
    #         if ac.number != askingPatch.number:
    #             print("now going to get distance to",finalGoal,"for acquains of patch",ac.number)
    #             ac.ManhattanGoal(askingPatch,finalGoal,start+1)
    #         else:
    #             break

    #     print("## END OF MANHATTANDISTANCE")


    def ManhattanGoal(self,askingPatch,finalGoal,start):
        '''
        update self.goalWaves so this Patch contains 
        Manhattan distance from finalGoal
        '''

        #print("## ANALYZING MANHATTANDISTANCE to goal ",finalGoal," for patch ",askingPatch.number)

        if start == 0:
            self.env.blankPatch.blankWave = 0
            acquaintances = self.env.getAcquaintances(finalGoal)
        else:
            acquaintances = self.env.getAcquaintances(self.number)

        for ac in acquaintances.values():
            if finalGoal not in ac.getGoalWaves().keys() or (finalGoal in ac.getGoalWaves().keys() and ac.getGoalWaves()[finalGoal] > start+1):
                ac.updateGoalWaves(finalGoal,start+1)
                #print("now patch",ac.number,"'s distance to patch",finalGoal," is ",str(start+1))
                ac.ManhattanGoal(askingPatch,finalGoal,start+1)


        #print("## END OF MANHATTANDISTANCE")

    def getBlankWave(self):
        return self.blankWave

    def getGoalWaves(self):
        return self.goalWaves

    def updateGoalWaves(self,goal,value):
        self.goalWaves[goal] = value

    def updateBlankWave(self,value):
        self.blankWave = value

    ####### END OF MANHATTAN METHODS #######



######################################################################
######################################################################



class Environnement:
    ''' 
    class defining the board
    '''
    
    def __init__(self, taille = 3):
        
        self.taille = taille
        self.grid = np.empty((taille, taille), dtype = object) #2 2D grids, grid[0] contains Places, grid[1] contains EcoAgents
        #self.numbers will be used to assign random goal numbers to EcoAgents
        #self.numbers = np.copy(np.random.choice(taille**2, taille**2, replace = False))
        #self.numbers.resize((taille, taille))

        self.places = np.array(range(1,taille**2+1))
        self.places.resize((taille, taille))
        
        #prior satisfied tile (for constraints)
        self.prior_satisf = None

        self.positions = {} #so we remember which Place on
                #fill Patches
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                self.grid[i, j] = Patch(position = (i,j), taille = taille, tile = None,env=self)
                self.positions[self.grid[i, j].number] = (i,j) #associate a number to its position on the board
                #just so we don't have to reuse the formula all the time

        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.places[i,j] != taille**2:
                    goal = self.positions[self.places[i,j]]
                    self.grid[i, j].occupationChange(Tile(self.grid[goal[0],goal[1]], self.grid[i, j]))
                else:
                    self.blankPatch = self.grid[i,j]
        self.shuffle()
    
    def shuffle(self, T=1000):
        '''
        shuffles the tiles on the grid to have a random solvable configuration
        '''
        print("shuffling the grid...")
        for t in range(T):
            target = np.random.choice(list(self.getAcquaintances(self.blankPatch.number).values()), 1)[0]
            target.tile.doSatisfaction(self.blankPatch, display=False)

    def show_grid(self):
        '''
        show the Patches over the grid
        '''
        print("Reminder of original grid:")
        for i in range(self.taille):
            row = '|'
            for j in range(self.taille):
                row += ' '+str(self.grid[i,j].number)+'  | '
            print(row)

        print()

    def show(self):
        '''
        show the Tiles (identified by their goals) over the grid
        '''
        for i in range(self.taille):
            row = '|'
            for j in range(self.taille):
                if not self.grid[i,j].isFree():
                    row += ' '+str(self.grid[i,j].tile.goal.number)+'  | '
                else :
                    row += '    | '
            print(row)

        print()


    def changePriorSatisf(self,patch):
        print("################ new prior_satisf is",patch.number,"#####################")
        self.prior_satisf = patch

    def findNextUnsatisf(self):
        nextToSat = self.furtherFromBlank().tile
        print("gonna call trySatisfaction on tile ",nextToSat.goal.number)
        if self.prior_satisf != None:
            nextToSat.trySatisfaction([self.prior_satisf])
        else:
            nextToSat.trySatisfaction([])
        
    

    def furtherFromBlank(self):
        ''' 
        returns patch that is further from blank patch
        '''
        max_dist = 0
        for i in range(self.taille):
            for j in range(self.taille):
                if self.grid[i,j].getBlankWave() == None:
                    self.grid[i,j].ManhattanBlank()
                dist = self.grid[i,j].getBlankWave()
                if dist > max_dist and not self.grid[i,j].tile.isSatisfied():
                    max_dist = dist
                    furth = self.grid[i,j]
        return furth

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
                    acquaintances[directions[indice+1]] = self.grid[x+indice,y]
            except IndexError: 
              True
            try:
                if y + indice >= 0:
                    acquaintances[directions[indice+2]] = self.grid[x,y+indice]
            except IndexError:
              True

        return acquaintances




##########################################################
##########################################################

e = Environnement()
#e.positions
#e.getAcquintances(1)['up'].place.position
# print(e.getAcquaintances(2))
# e.show()
# e.getAcquaintances(1)['right'].tryEscape()
# print("change

e.show_grid()
e.show()
'''e.grid[0,0].tile.trySatisfaction()
print()
e.show()
'''

# #testing ManhattanGoal
# print("test of ManhattanGoal")
# goal = e.grid[0,0].tile.goal
# print("but de l'agent en haut a gauche est",goal.position)
# e.grid[0,0].tile.ManhattanDistanceGoal()
# print(e.grid[0,0].goalWaves)

# #testing MBToNone
# print("test of MBToNone")
# patch = e.grid[0,0]
# patch.MBToNone()
# print(e.grid[2,1].blankWave)

# #testing ManhattanBlank
# print("Test of ManhattanBlank")
# blank = e.grid[0,0] #patch de la ligne 1, colonne 2
# blank.ManhattanBlank()
# e.show()
# print(e.grid[1,1].blankWave)
