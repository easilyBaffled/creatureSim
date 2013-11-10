from random import randint
import random
from land import gameBoard
import twitter

'''
in move, you will lose energy based on speed 
your dominance will be an inverse function to the energy lost each turn,
    you lose 5 to move 1 to search 1 to eat then gain 10 for sleeping your dominance for the turn is 3
    could this end up over valuing shelters? you lose energy in a fight even if you win
'''
class creature:
    def __init__(self):
        self.token = "1255906142-P35nCBvLM2mgZmfrTcGmL75Gx3fXVFH1koBhzzc"
        self.tokenS = "hD0dtGV6ix4bVMqS1YjYPehQ1jWVWnDznrP0GTM9o"
        self.consumerKey = "66hO0XWV1mQGUr1HzhIgGw"
        self.consumerS = "rsrc7h7bUlqIhf3JqsvFRjBlRUHzI6lYXyqzdFVaPw"
        self.x = randint(0, 9)
        self.y = randint(0, 9)
        self.hunger = 10
        self.sensory = randint(2, 4)
        self.energy = 30
        self.strength = randint(1, 10)
        self.speed = randint(1, 10)
        self.bravery = randint(1, 10)
        self.intellignce = randint(2, 10)
        self.shelter = 0
        self.food = 0
        self.dominance = 0
    
    
    def distance(self, a, b):# distance squared (don't need the square root)
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) 
    
    def closest(self, locations, creature):
        return min(locations, key=lambda p: self.distance(creature, p[0]))   
   
    def foodClosest(self, locations, creature):
        if(self.shelter != 0):
            return min(locations, key=lambda p: (self.distance(creature, p[0]) / 2) - p[1] + (self.distance(self.shelter, p[0]) / 2))
        else:
            return min(locations, key=lambda p:(self.distance(creature, p[0]) / 2) - p[1])     
                            
    def find(self, string, gameBoard):
        print("find " + string)
        locations = []
        if self.x - self.sensory < 0:  xmin = 0 
        else:  xmin = self.x - self.sensory
           
        if self.x + self.sensory > 9:  xmax = 9
        else:  xmax = self.x + self.sensory
        
        if self.y - self.sensory < 0:  ymin = 0 
        else:  ymin = self.y - self.sensory
        
        if self.y + self.sensory > 9:  ymax = 9 
        else:  ymax = self.y + self.sensory
        
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):             
                if gameBoard[i][j][0][0] == string and gameBoard[i][j][0][1] > 0:
                    locations.append(((i, j), gameBoard[i][j][0][1]))
        self.energy -= 1
        if len(locations) == 0:
            return "none"
        elif(string == "f"):
            return self.foodClosest(locations, (self.x, self.y))
        return self.closest(locations, (self.x, self.y))#RETURN LIST NOT CLOSEST LATER ON
    
    def move(self, x, y, gameBoard):
        if x > 9:  x = 9
        if x < 0:  x = 0
        if y > 9:  y = 9
        if y < 0:  y = 0
        #if (x + 1 == self.x and y == self.y) or (x - 1 == self.x and y == self.y) or (x == self.x and y + 1 == self.y) or (x == self.x and y - 1 == self.y):
        if x == self.x and y == self.y:
            if gameBoard[x][y][0] == 'w':
                self.move(self.x + randint(-1, 1), self.y + randint(-1, 1), gameBoard)
            else:
                gameBoard[self.x][self.y][1] = 'X'
                gameBoard[x][y][1] = 'C'
                self.x = x
                self.y = y
                self.energy -= 1
                board.printBoard()
        else:
            path = []
            currX = x
            currY = y
            while currX != self.x or currY != self.y:
                neighbors = [(currX + 1, currY + 1), (currX + 1, currY), (currX + 1, currY - 1), (currX, currY + 1), (currX - 1, currY + 1), (currX - 1, currY - 1)]
                for i in neighbors:
                    try:
                        if gameBoard[i[0]][i[1]][0][0] == 'w':
                            neighbors.remove(i)
                    except IndexError:
                        a = 1
                path.append(max(neighbors, key=lambda p: (self.distance((x, y), p) - self.distance((self.x, self.y), p))))
                gameBoard[self.x][self.y][1] = 'X'
                gameBoard[currX][currY][1] = 'C'
                self.x = currX
                self.y = currY
                self.energy -= 1
                 
    def play(self, board):
        gameBoard = board.a
        # if self.engery <= 0:
        #     die()
        board.grow()
        while self.energy > 15:#SLEEP
            if self.hunger > 14:#HUNGRY            
                newLocation = self.find("f", gameBoard)
                if newLocation == "none":
                    self.move(self.x + 1, self.y + 1, gameBoard)
                else:
                    self.move(newLocation[0][0], newLocation[0][1], gameBoard)
                    if(gameBoard[self.x][self.y][0] == "0"):
                        self.hunger -= gameBoard[self.x][self.y][0][1]
                    print("Nom nom nom")  
                    gameBoard[self.x][self.y][0][1] = -1
                    board.printBoard()
            else:
                if self.shelter == 0:
                    while(self.find("s", gameBoard) == "none"):
                        self.move(self.x + randint(-1, 1), self.y + randint(-1, 1), gameBoard)                                  
                    newLocation = self.find("s", gameBoard)
                    self.shelter = newLocation[0]
                self.move(self.shelter[0], self.shelter[1], gameBoard)
                gameBoard[self.x][self.y][0][1] += round(self.intellignce / 2)
                print("improving shelter")
                self.energy -= self.intellignce * 2
                board.printBoard()
                self.hunger += 1
        
        if self.shelter == 0:
            while(self.find("s", gameBoard) == "none"):
                self.move(self.x + randint(-1, 1), self.y + randint(-1, 1), gameBoard)                                  
            newLocation = self.find("s", gameBoard)
            self.shelter = newLocation[0]
        self.move(self.shelter[0], self.shelter[1], gameBoard)
        print("Shhh I'm Sleeping")
        self.energy += (gameBoard[self.x][self.y][0][1]) * 2
        self.energy -= self.hunger / 2
        self.hunger += 1
        self.dominance += self.energy
        #else:
        #    improve("Shelter", gameBoard)
    def __str__(self):
        return("x: " + str(self.x) + " y: " + str(self.y) + " hunger: " + str(self.hunger) + " energy: " + str(self.energy) + " dominance " + str(self.dominance)
              + " sensory: " + str(self.sensory) + " strength: " + str(self.strength) + " speed: " + str(self.speed) + " intelligence " + str(self.intellignce) + " bravery: " + str(self.bravery)) 

    def evolve(self, creature):
        #http://programmers.stackexchange.com/questions/189663/python-random-with-a-skew
        self.hunger = 10
        self.energy = 50
        self.sensory = self.evolveVal(creature, self.sensory, creature.sensory)
        self.strength = self.evolveVal(creature, self.strength, creature.strength)
        self.speed = self.evolveVal(creature, self.speed, creature.speed)
        self.bravery = self.evolveVal(creature, self.bravery, creature.bravery)
        self.intellignce = self.evolveVal(creature, self.intellignce, creature.intellignce)
        self.dominance = 0
        
    def evolveVal(self, creature, selfTrait, creatureTrait):
        target = random.random()
        skew = abs(self.dominance - creature.dominance) + 1
        fine_tuning_multiplier = 0.3
        skewed_target = target ** (skew * fine_tuning_multiplier)
        
        trait_delta = abs(selfTrait - creatureTrait)
        target_trait = trait_delta * (1 - skewed_target)
        
        if self.dominance > creature.dominance:
            val = creatureTrait - target_trait
        else:
            val = selfTrait + target_trait
        return round(val)
    
    def specialFind(self, string, gameBoard, x, y):
        print("find " + string)
        locations = []
        if x - self.sensory < 0:  xmin = 0 
        else:  xmin = x - self.sensory
           
        if x + self.sensory > 10:  xmax = 10 
        else:  xmax = x + self.sensory
        
        if y - self.sensory < 0:  ymin = 0 
        else:  ymin = y - self.sensory
        
        if y + self.sensory > 10:  ymax = 10 
        else:  ymax = y + self.sensory
        
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):             
                if gameBoard[i][j][0][0] == string and gameBoard[i][j][0][1] != 0:
                    locations.append((i, j))
        self.energy -= 1
        if len(locations) == 0:
            return 0
        return self.closest(locations, (x, y))#RETURN LIST NOT CLOSEST LATER ON
    def tweet(self):
        auth = twitter.OAuth(self.token, self.tokenS, self.consumerKey, self.consumerS)
        t = twitter.Twitter(auth=auth)
        t.account.verify_credentials()
        t.statuses.update(status="Hi Prof. @bederson, I just ran a life cycle simulation and will be joining you and Danny at your meeting today.")


board = gameBoard()

board.a = [[[['f', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X']],
[[['s', 1], 'X'], [['X', 0], 'X'], [['w', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X']],
[[['X', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['s', 1], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X']],
[[['X', 0], 'X'], [['w', 0], 'X'], [['w', 0], 'X'], [['w', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['s', 1], 'X']],
[[['X', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['w', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['s', 1], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X']],
[[['X', 0], 'X'], [['s', 1], 'X'], [['X', 0], 'X'], [['w', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X']],
[[['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['w', 0], 'X'], [['f', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['s', 1], 'X'], [['X', 0], 'X'], [['X', 0], 'X']],
[[['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['w', 0], 'X'], [['s', 1], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X']],
[[['f', 0], 'X'], [['X', 0], 'X'], [['w', 0], 'X'], [['w', 0], 'X'], [['X', 0], 'X'], [['f', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['s', 1], 'X'], [['X', 0], 'X']],
[[['X', 0], 'X'], [['X', 0], 'X'], [['w', 0], 'X'], [['w', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X'], [['X', 0], 'X']]]

animal = creature()
'''
animal.strength = 5
animal.speed = 5
animal.bravery = 5
animal.x = 0
animal.y = 0
animal.sensory = 4
'''
with  open("text", "rt")as inFile:
#ABSOLUTLY MAKE SURE THAT THERE ARE NO EXTRA \n IN TEXT
    for line in inFile:
        data = line.split()
        if data[0] == "x":
            animal.x = int(data[2])
        elif data[0] == "y":
            animal.y = int(data[2])
        elif data[0] == "hunger":
            animal.hunger = int(data[2])
        elif data[0] == "sensory":
            animal.sensory = int(data[2])
        elif data[0] == "energy":
            animal.energy = int(data[2])
        elif data[0] == "strength":
            animal.strength = int(data[2])
        elif data[0] == "speed":
            animal.speed = int(data[2])
        elif data[0] == "bravery":
            animal.bravery = int(data[2])
        elif data[0] == "intellignce":
            animal.intellignce = int(data[2])
        elif data[0] == "shelter":
            if data[2] == "0":
                animal.shelter = 0
            else: 
                animal.shelter = eval(data[2] + data[3])
        elif data[0] == "food":
            animal.food = int(data[2])
        elif data[0] == "dominance":
            animal.dominance = int(data[2])
#inFile.close() THE WITH OPEN...AS WILL AUTOCLOSE FILE AND CATCH ALL EXCEPTIONS
board.a[animal.x][animal.y][1] = 'C'
print(animal)
board.printBoard()
for i in range(5): 
    animal.play(board)
    print(animal)
    board.printBoard()
mate = creature()
mate.strength = 10
mate.speed = 10
mate.bravery = 7
mate.sensory = 5
animal.intelligence = 5
mate.dominance = 100
animal.evolve(mate)
print(animal)
#animal.tweet()TWEET
out = open("text", "wt")
out.write("strength" + " = " + str(animal.strength) + "\n")
out.write("speed" + " = " + str(animal.speed) + "\n")
out.write("bravery" + " = " + str(animal.bravery) + "\n")
out.write("x" + " = " + str(animal.x) + "\n")
out.write("y" + " = " + str(animal.y) + "\n")
out.write("sensory" + " = " + str(animal.sensory) + "\n")
out.write("hunger" + " = " + str(animal.hunger) + "\n")
out.write("energy" + " = " + str(animal.energy) + "\n")
out.write("dominance" + " = " + str(animal.dominance) + "\n")
out.write("shelter" + " = " + str(animal.shelter) + "\n")
out.close()
