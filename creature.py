from json import dumps
import land


class Creature:
    def __init__(self, *args): 
        if args[0] == "loaded":
            self.knownPaths = args[1]["knownPaths"]
            self.traits = args[1]["traits"]
            self.priority = args[1]["priority"]
            self.x = args[1]["x"]
            self.y = args[1]["y"]
            self.hunger = args[1]["hunger"]
            self.energy = args[1]["energy"]
            self.shelter = args[1]["shelter"]
            self.dominance = args[1]["dominance"]
            self.boardSize = args[1]["boardSize"]
        else:
            if args[0]:
                self.knownPaths = {}  # saved paths, from previous movements, shortens search time
                self.traits = [4, 4, 3, 4, 4, 3]  # ["sleep", "eat", "sensory", "improveShelter", "storeFood", "wander"]
                self.priority = ["sleep", "eat", "improveShelter", "storeFood", "wander"]  # ordered by importance
                self.x = 0  # location
                self.y = 0  # location
                self.priorityAction = None  # action determined by priority()
                self.hunger = 10  # diminishing factor pushes creature to action
                self.energy = 30  # diminishing factor pushes creature to action
                self.shelter = 0  # reference to shelter
                self.dominance = 0  #  value of hunger & energy to determine mating priority
                self.boardSize = 9  # DO NOT STEP OUTSIDE THE BOARD

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
    class NoLocation(Exception): 
        pass    
    def __str__(self):
        shelter = 0
        return("x " + str(self.x) + " y " + str(self.y) + " hunger " + str(self.hunger) + " energy " + str(self.energy) + " shelter " + str(shelter) + " dominance " + str(self.dominance) + " board size " + str(self.boardSize) + " SOCIAL " + str(self.getSocial()) + " INTELLIGENCE " + str(self.getIntelligence()) + " SENSORY " + str(self.getSensory()) + " SPEED " + str(self.getSpeed()) + " BRAVERY " + str(self.getBravery()) + " STRENGTH " + str(self.getStrength()))
    def interactWith(self, otherCreature):
        if self.getBravery() > 5:
            return "fight"
        if self.getSocial() > 5 and otherCreature.getSocial() > 4:
            return "befriend"
        else: return "run"


    def findBest(self, sim, landTileType, board):
        theWayHome = sim.planPath(board[self.shelter[0]][self.shelter[1]], self.x, self.y, self)
        if isinstance(landTileType, land.Shelter):
            return theWayHome

        sensory = self.traits[2]
        minX = 0 if self.x - sensory < 0 else self.x - sensory  # minX/Y stops you from going over the front
        minY = 0 if self.y - sensory < 0 else self.x - sensory
        subMapY = board[minY:self.y+sensory]  # slice will just stop at the end of a list and not go over
        best = (None, 0)
        for row in subMapY:
            for tile in row[minX:+sensory]:
                if isinstance(tile, landTileType) or isinstance(tile, land.Shelter):
                    path = sim.planPath(tile, self.x, self.y, self)
                    distanceToCreature = len(path)
                    distanceToShelter = len(theWayHome)
                    value = 0
                    if distanceToCreature < 15 and tile.vegitation > 0:
                        if distanceToCreature + distanceToShelter == 0:
                            value = tile.vegitation
                        else:
                           value = tile.vegitation / (distanceToCreature + distanceToShelter)
                        if value > best[1]:
                            best = path, value
                            # if value > x:
                            #   return path
        return best[0]


    def save(self):
            return dumps({"knownPaths":self.knownPaths,
                    "traits":self.traits,
                    "priority":self.priority,
                    "x":self.x,
                    "y":self.y,
                    "hunger":self.hunger,
                    "energy":self.energy,
                    "shelter":self.shelter,
                    "dominance":self.dominance,
                    "boardSize":self.boardSize, })
'''
traits = [4, 4, 3, 4, 4, 3]
priorities = ["sleep", "eat", "improveShelter", "storeFood", "wander"]
boardSize = 10
c = Creature("original", traits, priorities, boardSize, {})
c.x = 2
c.y = 3
c.shelter = Land.landMass[9][9]
print(c.getSocial())
c.save()
print(c)
with open("text") as file:
    lines = file.readlines()
    for stats in lines:
        result = loads(stats)
        b = Creature("loaded", result)
print(b)
print(b.traits)
print(b.getSocial())

'''
'''
in move, you will lose energy based on speed
your dominance will be an inverse function to the energy lost each turn,
    you lose 5 to move 1 to search 1 to eat then gain 10 for sleeping your dominance for the turn is 3
    could this end up over valuing shelters? you lose energy in a fight even if you win
'''