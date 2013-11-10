import land as Land
import twitter
from random import randint

'''
in move, you will lose energy based on speed 
your dominance will be an inverse function to the energy lost each turn,
    you lose 5 to move 1 to search 1 to eat then gain 10 for sleeping your dominance for the turn is 3
    could this end up over valuing shelters? you lose energy in a fight even if you win
'''
class Creature:
    def __init__(self, social, intelligence, sensory, speed, bravery, strenght, size, knownPaths):
        self.knownPaths = knownPaths
        self.traits = [social, intelligence, sensory, speed, bravery, strenght]
        self.x = 0
        self.y = 0
        self.priorityAction = None
        self.hunger = 10
        self.energy = 30
        self.shelter = 0
        self.dominance = 0
        self.boardSize = size - 1
        self.__SOCIAL = 0
        self.__INTELLIGENCE = 1
        self.__SENSORY = 2
        self.__SPEED = 3
        self.__BRAVERY = 4
        self.__STRENGTH = 5
        
    def getSocial(self):
        return self.traits[self.__SOCIAL]
    def getIntelligence(self):
        return self.traits[self.__INTELLIGENCE]
    def getSensory(self):
        return self.traits[self.__SENSORY]
    def getSpeed(self):
        return self.traits[self.__SPEED]
    def getBravery(self):
        return self.traits[self.__BRAVERY]
    def getStrength(self):
        return self.traits[self.__STRENGTH]
    def xyBalance(self, var):
        if var < 0:
            return 0
        if var > self.boardSize:
            return self.boardSize
        else:
            return var
    class NoLocation(Exception): 
        pass    
    def __str__(self):
        shelter = 0
        if self.shelter != 0:
            shelter = self.shelter.location
        return("x " + str(self.x) + " y " + str(self.y) + " hunger " + str(self.hunger) + " energy " + str(self.energy) + " shelter " + str(shelter) + " dominance " + str(self.dominance) + " board size " + str(self.boardSize) + " SOCIAL " + str(self.getSocial()) + " INTELLIGENCE " + str(self.getIntelligence()) + " SENSORY " + str(self.getSensory()) + " SPEED " + str(self.getSpeed()) + " BRAVERY " + str(self.getBravery()) + " STRENGTH " + str(self.getStrength()))

    def tweet(self):
        token = "1255906142-P35nCBvLM2mgZmfrTcGmL75Gx3fXVFH1koBhzzc"
        tokenS = "hD0dtGV6ix4bVMqS1YjYPehQ1jWVWnDznrP0GTM9o"
        consumerKey = "66hO0XWV1mQGUr1HzhIgGw"
        consumerS = "rsrc7h7bUlqIhf3JqsvFRjBlRUHzI6lYXyqzdFVaPw"
        auth = twitter.OAuth(token, tokenS, consumerKey, consumerS)
        t = twitter.Twitter(auth=auth)
        t.account.verify_credentials()
        t.statuses.update(status="@EasilyBaffled Hi!")
        
    def planPath(self, x, y, goal, board):
        print("Planning Path: Start " + str((x, y)) + " End: " + str(goal.location))
        visited = []
        path = []
        fringe = []
        parentMap = {}
        fringe.append(board[x][y])
        while fringe:
            self.energy -= .3
            fringe.sort(key=lambda neighbor:  abs(neighbor.location[0] - goal.location[0]) + abs(neighbor.location[1] - goal.location[1]) + abs(neighbor.elevation - goal.elevation), reverse=True)
            curr = fringe.pop()
            if self.knownPaths.get((curr, goal)):
                path.extend(self.knownPaths.get((curr, goal))[1:])
                print("path known")
                return path
            if curr == goal:
                while curr in parentMap:
                    path.insert(0, curr)
                    curr = parentMap[curr]
                for current in path:
                    self.knownPaths[(current, goal)] = path[path.index(current):]
                '''
                print("planned path. from:" + str(x) + ", " + str(y) + " to: " + str(goal.location))
                for i in path:
                    print(i)
                '''
                return path
            visited.append(curr)
            neighbors = [neighbor for neighbor in curr.neighbors if type(neighbor) is not Land.Water and neighbor not in visited]    
            for neighbor in neighbors:
                fringe.insert(0, neighbor)
                parentMap[neighbor] = curr
        
    def priority(self):
        if self.energy < 15:
            self.priorityAction = "sleep"
            return "sleep"
        if self.hunger < 14:
            self.priorityAction = "eat"
            return "eat"
        if self.shelter.quality < 50:
            self.priorityAction = "improveShelter"
            return "improveShelter"
        if self.shelter.foodStorage < 10 and self.getIntelligence() > 4:
            self.priorityAction = "storeFood"
            return "storeFood"
        self.priorityAction = "wander"
        return "wander"
    def findBest(self, landType, board):      
        minX = self.xyBalance(self.x - self.getSensory())
        maxX = self.xyBalance(self.x + self.getSensory())
        minY = self.xyBalance(self.y - self.getSensory())
        maxY = self.xyBalance(self.y + self.getSensory())  
        possibleTargets = []
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                #print(board)
                if type(board[x][y]) is landType and board[x][y] != board[self.x][self.y]:
                    possibleTargets.append(board[x][y])
                if landType is Land.Food and type(board[x][y]) is Land.Shelter and board[x][y].foodStorage > 0:
                    possibleTargets.append(board[x][y]) 
        '''
        print("possible Targets")
        for i in possibleTargets:
            print(str(i.location) + " " + str(type(i)))                 
        '''
        targetValues = {}
        targetPaths = {}
        if landType is Land.Shelter:
            return self.planPath(self.x, self.y, self.shelter, board)
        if landType is Land.Food:
            for land in possibleTargets:
                pathFromCreature = self.planPath(self.x, self.y, land, board)
                targetToCreature = len(pathFromCreature)
                targetToShelter = len(self.planPath(self.shelter.location[0], self.shelter.location[1], land, board))
                '''
                print("path to target is:")
                for i in pathFromCreature:
                    print(str(i.location))
                print()
                '''
                if targetToCreature < 15 and land.vegitation > 0:
                    if (targetToCreature + targetToShelter) - self.getSpeed() == 0:
                        targetValues[land] = land.vegitation
                    else : targetValues[land] = land.vegitation / ((targetToCreature + targetToShelter))
                    targetPaths[land] = pathFromCreature
            if targetValues:
                print("-------------------------------------")
                for all in targetPaths:
                    print(str(all) + " " + str(len(targetPaths[all])))
                print()
                print(targetValues)
                path = targetPaths[max(targetValues, key=targetValues.get)]
                print("path is ")
                for i in path:
                    print(str(i.location))
                print()
                return path
        '''
        else: 
            for land in possibleTargets:
                targetToCreature = len(self.planPath(self.x, self.y, land, board))
                if targetToCreature < 20:
                    if (targetToCreature) - self.getSpeed() == 0:
                        targetValues[land] = 1
                    else: targetValues[land] = 1 / (targetToCreature - self.getSpeed())
            if targetValues:
                return [max(targetValues, key=targetValues.get)]
        '''
        return None
       
    def performAction(self, location):
        action = self.priorityAction
        if action == "sleep":
            print("sleeping" + str(self.shelter.quality))
            self.energy += self.shelter.quality * 3
        if action == "eat":   
            if type(location) is Land.Shelter:
                print("eating at home")
                self.hunger -= location.foodStorage
                location.foodStorage = 0
            else:
                print("eating out")
                self.hunger -= location.vegitation
                location.vegitation = (-1)
        if action == "improveShelter":
            print("Improving Shelter")
            location.quality += self.getIntelligence() * 2
        if action == "storeFood":
            print("Storing Nuts for Winter")
            food = location.vegitation
            location.vegitation = (-1)
            import simulation
            simulation.Simulation.move(self, self.shelter)#PROBLEM
            self.shelter.foodStorage += food
    
    def interactWith(self, otherCreature):
        if self.getBravery() > 5:
            return "fight"
        if self.getSocial() > 5 and otherCreature.getSocial() > 4:
            return "befriend"
        else: return "run"
'''
c = Creature(4, 4, 3, 4, 4, 3, 10, {})
c.x = 2
c.y = 3
c.shelter = Land.landMass[9][9]
print(c.findBest(Land.Food, Land.landMass))

'''
