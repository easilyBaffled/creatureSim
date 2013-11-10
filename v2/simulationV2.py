import land
import creature as Creature
from random import randint
from random import randrange
from random import shuffle
from operator import attrgetter as attribute
from time import clock
import urllib.request
import json
class Simulation():
    def __init__(self, x, lengthOfDay):
        self.timeOfDay = lengthOfDay
        self.creatures = {Creature.Creature(4, 4, 3, 4, 4, 3, 10, {}):"", Creature.Creature(4, 4, 3, 4, 4, 3, 10, {}):""}
        self.map = land.landMass
        self.waters = []
        self.foods = []
        self.shelters = []
        for row in self.map:
            for column in row: 
                if type(column) is land.Water:
                    self.waters.append(column)
                elif type(column) is land.Food:
                    self.foods.append(column)
                elif type(column) is land.Shelter:
                    self.shelters.append(column)
        for creature in self.creatures:
            shuffle(self.shelters)
            for shelter in self.shelters:
                if shelter.owner == None:
                    shelter.owner = creature
                    creature.shelter = shelter
                    creature.x = shelter.location[0]
                    creature.y = shelter.location[1]
                    self.map[creature.x][creature.y].creatures.append(creature)
                    break
        self.lifeCycles = x
        self.runStay = ["rfl", "rbf", "rbl", "rbf", ]
        self.befriend = ["bbl", "bbf"]
        self.fight = ["fbl", "fbf", "bfl", "bff", "ffl", "fff"]
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
                else: output += (str(x.__class__.__name__[0]) + " ") 
                output += ("(" + str(x.location[0]) + ", " + str(x.location[1]) + ", " + str(x.elevation) + ") " + " | ")
            output += "\n"
        output += (" life Cycle: " + str(self.lifeCycles))
        return output
    def simulate(self):
        traveling = []
        for generation in range(self.lifeCycles):
            start = clock()
            awake = list(self.creatures)
            data = urllib.request.urlopen('http://api.openweathermap.org/data/2.1/weather/city/4351977?units=imperial')
            s = data.read().decode("utf-8")
            cities = json.loads(s)
            temp = cities['main']['temp']
            rain = cities.get('rain')
            for grass in self.foods:
                grass.grow(temp, rain)
            '''
            #TO BE TESTED
            for land in self.waters:
                if rain:
                    land.waterLevel += 1
                    land.flood()
                elif land.waterLevel > self.elevation:
                    land.waterLevel -= 1
                    if land.waterLevel == self.elevation:
                        land = land.was
            '''
            for hour in range(self.timeOfDay):          
                print("Life Time " + str(generation + 1) + "/" + str(self.lifeCycles) + " Hour " + str(hour + 1) + "/" + str(self.timeOfDay))
                print(self)
                traveling = []
                for creature in list(awake):
                    goal = None
                    while goal == None:
                        priority = creature.priority()
                        if priority == "sleep" and creature.shelter.location == (creature.x, creature.y):#BECAUSE AWAKE KEEPS REFILLING
                            break
                        if priority == "improveShelter":
                            goal = creature.findBest(land.Shelter, self.map)
                        elif priority == "sleep":
                            goal = creature.findBest(land.Shelter, self.map)
                            print(awake)
                            awake.remove(creature)
                            print(awake)
                        else:
                            goal = creature.findBest(land.Food, self.map)#will return the path from here to the best goal
                        if goal == None:
                            x = creature.xyBalance(creature.x + randrange(-1, 2, 2))
                            y = creature.xyBalance(creature.y + randrange(-1, 2, 2))
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
                                    creature.performAction(self.map[creature.x][creature.y]) 
                            creature.performAction(self.map[creature.x][creature.y])
                            creature.dominance += hour   
                
            out = open("text", "a")
            out.write(str((clock() - start) * 1000) + "+")
            out.close() 
            print("time: " + str((clock() - start) * 1000))
        self.evolve()
        print(self)    
        print("END OF SIM")              
    def move(self, creature, target):
        self.map[creature.x][creature.y].creatures.remove(creature)
        creature.energy -= .5 + (abs(self.map[creature.x][creature.y].elevation - target.elevation) / creature.getSpeed())
        target.creatures.append(creature)
        print("move" + str(target.creatures))
        creature.x, creature.y = target.location    
        if len(target.creatures) > 1:
            print("-----------------action-----------------")
            action = creature.interactWith(target.creatures[0])
            otherAction = target.creatures[0].interactWith(creature)
            result = (action[0] + otherAction[0] + target.__class__.__name__[0])
            if result in self.runStay:
                self.creatures[creature] = creature.planPath(creature.x, creature.y, creature.shelter, self.map)
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
                    self.creatures[target.creatures[0]] = creature.planPath(self.creatures[target.creatures[0]].x, self.creatures[target.creatures[0]].y, self.creatures[target.creatures[0]].shelter, self.map)
                else:
                    creature.energy -= otherStrength
                    self.creatures[creature] = creature.planPath(creature.x, creature.y, creature.shelter, self.map)
            else:
                self.creatures[creature] = creature.planPath(creature.x, creature.y, creature.shelter, self.map)

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
            child = Creature.Creature(traits[0], traits[1], traits[2], traits[3], traits[4], traits[5], lastGeneration[mate].boardSize, knownPaths)
            child.shelter = lastGeneration[mate].shelter
            child.x = child.shelter.location[0]
            child.y = child.shelter.location[1]
            nextGeneration.append(child)
        self.creatures = nextGeneration

import signal
class TimeoutException(Exception): 
    pass
def alarm_handler(*args):
    raise TimeoutException()
def tryRun(func, timeout):
    oldHandler = signal.signal(signal.SIGALRM, alarm_handler) 
    try:
        signal.alarm(timeout)
        func()
    except TimeoutException:
        print("--OUT OF TIME--")
    else:
        print("--IN TIME--")
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, oldHandler)
sim = Simulation(2, 5)
tryRun(sim.simulate, 5)
#Simulation(1, 1) runs in an average of 3.273100000000001
#Simulation(1, 2) runs in an average of 6.8399000000000045
#Simulation(1, 3) runs in an average of 7.170300000000005, Sleeps
#Simulation(1, 4) runs in an average of 10.670699999999997, Sleeping for last two 'hours'
#Simulation(1, 5) runs in an average of 14.310000000000006, still sleeping
#Simulation(1, 6) runs in an average of 16.0338
#Simulation(1, 7) runs in an average of 16.412100000000006
#Simulation(1, 8) runs in an average of 18.605600000000003
#Simulation(1, 9) runs in an average of 19.8816




