import land 
import creature as Creature
from random import randint
from random import randrange
from random import shuffle
from operator import attrgetter as attribute
import urllib2  # THIS IS THE MAIN CHANGE BETWEEN LOCAL AND REMOTE VERSION
from json import loads
#import twitter#THIS IS ALSO A CHANGE FROM LOCAL TO REMOTE
from Tkinter import *


class Map():
    def __init__(self,):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=1200, height=1200)
        self.canvas.pack()
        self.colors = {
            "Land": "grey",
            "Food": "green",
            "Water": "blue",
            "Shelter": "black"
        }
        self.canvasDict = {}  # the keys are (x,y, "type"), the data is the id so it can be grabbed for item config.
        for i, row in enumerate(land.landMass):
            for j, tile in enumerate(row):
                color = self.colors[tile.__class__.__name__]
                self.canvasDict[i, j, "tile"] = self.canvas.create_rectangle(50 * i, 50 * j, 50 * (i + 1), 50 * (j + 1),
                                                                             outline=color, fill=color)
                info = tile.elevation
                if color == "green":
                    info = tile.vegitation
                elif color == "black":
                    info = tile.quality

                self.canvasDict[i, j, "text"] = self.canvas.create_text(50 * i + 3, 50 * j, anchor=NW, fill="white", text=info)
        self.canvasDict["creature"] = self.canvas.create_rectangle(0, 0, 50, 50,
                                                                   outline="red", fill="red")
        self.canvas.pack(fill=BOTH, expand=1)
        sim = Simulation([], 5, 5, self.root, self.canvas, self.canvasDict)
        self.root.after(1000, sim.simulate)
        """
        c = Creature.Creature("original")
        for i in range(100):
            print(i)
        sim.map[c.x][c.y].creatures.append(c)
        sim.move(c, sim.map[1][1])
        """
        self.root.mainloop()


class Simulation():
    def __init__(self, data, generations, lengthOfDay, root, canvas, canvasDict):
        self.root = root
        self.canvas = canvas
        self.canvasDict = canvasDict
        self.timeOfDay = lengthOfDay
        self.generations = generations
        self.creatures = {}

        if len(data) > 10:
            self.ret(2)
            result = loads(data)
            self.creatures = {Creature.Creature("loaded", result): ""}
        else:
            self.ret(1)
            print("creation")
            self.creatures = {Creature.Creature("original"): ""}
        self.data = data  
        self.map = land.landMass
        self.waters = []
        self.foods = []
        self.shelters = []
        for row in self.map:
            for column in row:
                if isinstance(column, land.Water): 
                    self.waters.append(column)
                elif isinstance(column, land.Food):
                    self.foods.append(column)
                elif isinstance(column, land.Shelter):
                    self.shelters.append(column)
        for creature in self.creatures:
            shuffle(self.shelters)
            for shelter in self.shelters:
                if shelter.owner is None:
                    shelter.owner = creature
                    creature.shelter = shelter.location
                    creature.x = shelter.location[0]
                    creature.y = shelter.location[1]
                    self.map[creature.x][creature.y].creatures.append(creature)
                    self.root.after(1000, self.canvas.move, canvasDict["creature"], creature.x*50, creature.y*50)
                    break

        self.runStay = ["rfl", "rbf", "rbl", "rbf", ]
        self.befriend = ["bbl", "bbf"]
        self.fight = ["fbl", "fbf", "bfl", "bff", "ffl", "fff"]

    def test(self):
        self.root.after(1000, self.canvas.move, self.canvasDict["creature"], 50, 50)

    def runSim(self):
        if self.generations > 0:
            self.simulate()
            self.generations -= 1
        else:
            return self.evolve()

    def ret(self, var):
        if var == 1:
            return "new"
        else:
            return "old"
        
    def __str__(self):
        output = ""
        for i in self.map:
            for x in i:
                output += x.__str__()
            output += "\n"
        for x in self.creatures:
            output += x.__str__()
            output += "\n"
        for i in self.map:
            for x in i:
                if len(x.creatures) > 0:
                    output += "C "
                else:
                    output += (str(x.__class__.__name__[0]) + " ")
                output += ("(" + str(x.location[0]) + ", " + str(x.location[1])
                           + ", " + str(x.elevation) + ") " + " | ")
            output += "\n"
        output += (" life Cycle: " + str(self.generations))
        return output

    def resim(self):
        print "RESIM STARTED", self.generations
        if self.generations > 0:
            print "working", self.generations
            self.generations -= 1
            self.root.after(1000, self.canvas.move, self.canvasDict["creature"], ((self.generations+1)-self.generations)*50, ((self.generations+1)-self.generations)*50)
            self.root.after(1000, self.resim)
        else:
            print "RESIM DONE"

    def simulate(self):
        if self.generations > 0:
            self.generations -= 1
            #THE START OF A NEW DAY
            awake = list(self.creatures)

            #<<WEATHER
            data = urllib2.urlopen('http://api.openweathermap.org/data/2.1/weather/city/4351977?units=imperial')
            s = data.read().decode("utf-8")
            cities = loads(s)
            temp = cities['main']['temp']
            rain = cities.get('rain')
            for grass in self.foods:
                grass.grow(temp, rain)
                self.root.after(1000, lambda: self.canvas.itemconfig(self.canvasDict[grass.location[0], grass.location[0], "text"], text=str(grass.vegitation)))
            #END WEATHER>>

            for hour in range(self.timeOfDay):
                print("Life Time " + str(self.generations + 1) + "/" + str(self.generations)
                      + " Hour " + str(hour + 1) + "/" + str(self.timeOfDay))
                print(self)
                traveling = []
                for creature in list(awake):  # ALL CREATURES THAT ARE STILL AWAKE
                    goal = None
                    while goal is None:  # FIND THE CURRENT CREATURES GOAL
                        priority = self.setPriority(creature)
                        if priority == "sleep" and creature.shelter == (creature.x, creature.y):
                            break
                        if priority in ["improveShelter", "sleep" ]:
                            goal = self.findBest(land.Shelter, creature)
                        else:
                            goal = self.findBest(land.Food, creature)  # will return the path from here to the best goal
                        if goal is None:
                            x = self.xyBalance(creature, creature.x + randrange(-1, 2, 2))
                            y = self.xyBalance(creature, creature.y + randrange(-1, 2, 2))
                            self.move(creature, self.map[x][y])
                        self.creatures[creature] = goal
                        #if type(goal) != land.Shelter and goal != None:
                        #    print(goal[-1].location)
                    traveling.append(creature)
                while traveling:
                    for creature in traveling:
                        if self.creatures[creature]:
                            print("traveling")
                            for all in self.creatures[creature]:
                                print(all.location)
                            print("")
                            self.move(creature, self.creatures[creature][0])
                            self.creatures[creature].pop(0)

                        else:
                            traveling.remove(creature)
                            print(self.map[creature.x][creature.y])
                            if creature.priorityAction == "sleep":
                                for i in range(1, self.timeOfDay - hour):
                                    print("sleep loop")
                                    self.performAction(creature, self.map[creature.x][creature.y])
                                awake.remove(creature)
                            self.performAction(creature, self.map[creature.x][creature.y])
                            creature.dominance += hour
            self.root.after(1000, self.simulate)
        else:
            print(self)
            print("END OF SIM")
            return self.evolve()

    def move(self, creature, target):
        newX = target.location[0] - creature.x
        newY = target.location[1] - creature.y
        self.map[creature.x][creature.y].creatures.remove(creature)
        creature.energy -= .5 + (abs(self.map[creature.x][creature.y].elevation - target.elevation) / creature.getSpeed())
        target.creatures.append(creature)
        print("------",creature.x, creature.y, self.map[creature.x][creature.y])
        self.root.after(1000, self.canvas.move, self.canvasDict["creature"], newX * 50, newY * 50)

        print("move" + str(target.creatures))
        creature.x, creature.y = target.location    

    def evolve(self):
        print("Evolving")
        lastGeneration = sorted(self.creatures.keys(), key=attribute('dominance'), reverse=True)
        nextGeneration = []
        for mate in range(0, len(lastGeneration)):
            knownPaths = lastGeneration[mate - 1].knownPaths
            traits = lastGeneration[mate - 1].traits[:2] + lastGeneration[mate].traits[2:]
            for i in range(3):
                trait = randint(0, 5)
                mutation = randint(-3, 3)
                if traits[trait] + mutation < 1:
                    traits[trait] = 1
                else:
                    traits[trait] += mutation
            knownPaths.update(lastGeneration[mate].knownPaths)
            child = Creature.Creature("original", traits, lastGeneration[mate].priority, lastGeneration[mate].boardSize, knownPaths)
            child.shelter = lastGeneration[mate].shelter
            child.x = child.shelter[0]
            child.y = child.shelter[1]
            nextGeneration.append(child)
        self.creatures = nextGeneration
        print("end of evolution")
        creatureStats = ''
        for all in self.creatures:
            creatureStats += all.save()
            creatureStats += '\n'
        return creatureStats

    def planPath(self, goal, x, y, creature):
        print("Planning Path: Start " + str((x, y)) + " End: " + str(goal.location))
        visited = []
        path = []
        fringe = []
        parentMap = {}
        fringe.append(self.map[x][y])
        while fringe:
            creature.energy -= .3
            fringe.sort(key=lambda neighbor:  abs(neighbor.location[0] - goal.location[0]) + abs(neighbor.location[1] - goal.location[1]) + abs(neighbor.elevation - goal.elevation), reverse=True)
            curr = fringe.pop()        
            if (curr, goal) in creature.knownPaths:
                path.extend(creature.knownPaths.get((curr, goal))[1:])
                print("path known")
                return path
            if curr == goal:
                while curr in parentMap:
                    path.insert(0, curr)
                    curr = parentMap[curr]
                for current in path:
                    creature.knownPaths[(current, goal)] = path[path.index(current):]
                return path
            visited.append(curr)
            neighbors = [neighbor for neighbor in curr.neighbors if not isinstance(neighbor, land.Water) and neighbor not in visited]    
            for neighbor in neighbors:
                fringe.insert(0, neighbor)
                parentMap[neighbor] = curr

    def xyBalance(self, creature, var):
        if var < 0:
            return 0
        if var > creature.boardSize:
            return creature.boardSize
        else:
            return var

    def findBest(self, landTileType, creature):
        return creature.findBest(self, landTileType, self.map)
        """
        print("finding")
        if isinstance(landTileType, land.Shelter):
            return self.planPath(self.map[creature.shelter[0]][creature.shelter[1]], creature.x, creature.y, creature)

        minX = self.xyBalance(creature, creature.x - creature.getSensory())
        maxX = self.xyBalance(creature, creature.x + creature.getSensory())
        minY = self.xyBalance(creature, creature.y - creature.getSensory())
        maxY = self.xyBalance(creature, creature.y + creature.getSensory())  
        possibleTargets = []
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                #print(self.map)
                if isinstance(self.map[x][y], landTileType) and self.map[x][y] != self.map[creature.x][creature.y]:
                    possibleTargets.append(self.map[x][y])
                if isinstance(landTileType, land.Food) and isinstance(self.map[x][y], land.Shelter) and self.map[x][y].foodStorage > 0:
                    possibleTargets.append(self.map[x][y])

        targetValues = {}
        targetPaths = {}
        stance(landTileType, land.Food):
            for landTile in possibleTargets:
                if isin     targetPaths[landTile] = self.planPath(landTile, creature.x, creature.y, creature)
                targetToCreature = len(targetPaths[landTile])
                targetToShelter = len(self.planPath(landTile, creature.shelter[0], creature.shelter[1] , creature))

                if targetToCreature < 15 and landTile.vegitation > 0:
                    if (targetToCreature + targetToShelter) == 0:
                        targetValues[landTile] = landTile.vegitation
                    else:
                        targetValues[landTile] = landTile.vegitation / ((targetToCreature + targetToShelter))
            if targetValues:
                path = targetPaths[max(targetValues, key=targetValues.get)]
                print("-----------------------------------------------")
                return path
        return None
    """

    def performAction(self, creature, location):
        action = creature.priorityAction
        if action == "sleep":
            print("sleeping" + str(self.map[creature.shelter[0]][creature.shelter[1]].quality))
            creature.energy += self.map[creature.shelter[0]][creature.shelter[1]].quality * 3
        if action == "eat":   
            if isinstance(location, land.Shelter):
                print("eating at home")
                creature.hunger -= location.foodStorage
                location.foodStorage = 0

            else:
                print("eating out")
                creature.hunger -= location.vegitation
                location.vegitation = (-1)
                self.root.after(1000, lambda: self.canvas.itemconfig(self.canvasDict[creature.x, creature.y, "text"], text="-1"))

        if action == "improveShelter":
            print("Improving Shelter")
            location.quality += creature.getIntelligence() * 2
            self.root.after(1000, lambda: self.canvas.itemconfig(self.canvasDict[creature.x, creature.y, "text"], text=str(location.quality)))

        if action == "storeFood":
            print("Storing Nuts for Winter")
            food = location.vegitation
            location.vegitation = (-1)
            self.move(creature, self.map[creature.shelter[0]][creature.shelter[1]])#PROBLEM
            self.map[creature.shelter[0]][creature.shelter[1]].foodStorage += food

    def setPriority(self, creature):
        for p in creature.priority:
            if p == "sleep" and creature.energy < 15:
                creature.priorityAction = "sleep"
                return "sleep"
            if p == "eat" and creature.hunger < 14:
                creature.priorityAction = "eat"
                return "eat"
            if p == "improveShelter" and self.map[creature.shelter[0]][creature.shelter[1]].quality < 50:
                creature.priorityAction = "improveShelter"
                return "improveShelter"
            if p == "storeFood" and self.map[creature.shelter[0]][creature.shelter[1]].foodStorage < 10 and creature.getIntelligence() > 4:
                creature.priorityAction = "storeFood"
                return "storeFood"
        creature.priorityAction = "wander"
        return "wander"

"""
    def tweet(self):
        token = "1255906142-P35nCBvLM2mgZmfrTcGmL75Gx3fXVFH1koBhzzc"
        tokenS = "hD0dtGV6ix4bVMqS1YjYPehQ1jWVWnDznrP0GTM9o"
        consumerKey = "66hO0XWV1mQGUr1HzhIgGw"
        consumerS = "rsrc7h7bUlqIhf3JqsvFRjBlRUHzI6lYXyqzdFVaPw"
        auth = twitter.OAuth(token, tokenS, consumerKey, consumerS)
        t = twitter.Twitter(auth=auth)
        t.account.verify_credentials()
        t.statuses.update(status="@EasilyBaffled Hi!")
        """
"""
import signal
class TimeoutException(Exception): 
    pass
def alarm_handler(*args):
    raise TimeoutException()
def tryRun(func, timeout):
    oldHandler = signal.signal(signal.SIGALRM, alarm_handler) 
    try:
        signal.alarm(timeout)
        print(func())
    except TimeoutException:
        print("--OUT OF TIME--")
    else:
        print("--IN TIME--")
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, oldHandler)
sim = Simulation('', 1, 1)
#tryRun(sim.simulate, 5)





#Simulation(1, 1) runs in an average of 3.273100000000001
#Simulation(1, 2) runs in an average of 6.8399000000000045
#Simulation(1, 3) runs in an average of 7.170300000000005, Sleeps
#Simulation(1, 4) runs in an average of 10.670699999999997, Sleeping for last two 'hours'
#Simulation(1, 5) runs in an average of 14.310000000000006, still sleeping
#Simulation(1, 6) runs in an average of 16.0338
#Simulation(1, 7) runs in an average of 16.412100000000006
#Simulation(1, 8) runs in an average of 18.605600000000003
#Simulation(1, 9) runs in an average of 19.8816
"""
"""
#took this from simulation init
        with open(data) as file:
            if file.read(4):
                #random creations
                with open(data) as file:
                    lines = file.readlines()
                    for stats in lines:
"""
"""
       #FLOODING TO BE TESTED
       for landTile in self.waters:
           if rain:
               land.waterLevel += 1
               land.flood()
           elif land.waterLevel > self.elevation:
               land.waterLevel -= 1
               if land.waterLevel == self.elevation:
                   landTile = land.was
       """
"""
#INTERACTION
if len(target.creatures) > 1:
    print("-----------------action-----------------")
    action = creature.interactWith(target.creatures[0])
    otherAction = target.creatures[0].interactWith(creature)
    result = (action[0] + otherAction[0] + target.__class__.__name__[0])
    if result in self.runStay:
        self.creatures[creature] = self.planPath(self.map[creature.shelter[0]][creature.shelter[1]]
            , creature.x, creature.y, creature)
    elif result in self.befriend:
        if result[2] == "f":
            food = target.vegitation
            target.vegitation = -1
            creature.hunger += food / 2
            target.creatures[0].hunger += food / 2
            self.traveling.remove(creature)
            self.traveling.remove(target.creatures[0])
    elif result in self.fight:
        strength = creature.getStrength()
        otherStrength = target.creatures[0]
        if strength > otherStrength:
            target.creatures[0].energy -= strength
            self.creatures[target.creatures[0]] = self.planPath(self.creatures[self.creatures[target.creatures[0]]].shelter, self.creatures[self.creatures[target.creatures[0]]].x, self.creatures[self.creatures[target.creatures[0]]].y, self.creatures[self.creatures[target.creatures[0]]])
        else:
            creature.energy -= otherStrength
            self.creatures[creature] = self.planPath(self.map[creature.shelter[0]][creature.shelter[1]], creature.x, creature.y , creature)
    else:
        self.creatures[creature] = self.planPath(self.map[creature.shelter[0]][creature.shelter[1]], creature.x, creature.y, creature)
"""
#land will call simulation then every move, weather update, and action will call update map in landTile

m = Map()