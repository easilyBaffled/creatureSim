from random import randint
import json
import urllib.request
from tkinter import *
import time
class gameBoard():
    a = [ [['X', 'X'] for _ in range(10)] for x in range(1, 11) ]
    f = 0
    s = 0
    food = []
    shelter = []
    def __init__(self):
        for x in range(0, 9):
            for y in range(1, 4):
                vert = randint(0, 9)
                if y % 2 != 0:
                    self.a[x][vert] = [['f', 1], 'X']
                    self.food.append((x, vert))
                    self.f += 1
                else:
                    self.a[x][vert] = [['s', 1], 'X']
                    self.food.append((x, vert))
                    self.s += 1
    def printBoard(self):
        '''
        for i in self.a:
            for x in i:
                print(x, end=" ")
            print(' ') 
        print()
        '''
        master = Tk()

        w = Canvas(master, width=503, height=503)
        w.pack()
        for x, row in enumerate(self.a):
            for y, cell in enumerate(row):
                if self.a[x][y][1] == 'C':
                    w.create_rectangle([3 + 50 * y, 3 + 50 * x, 53 + 50 * y, 53 + 50 * x ], fill="black")
                    w.create_text(3 + 50 * y, 3 + 50 * x, anchor=NW, fill="white", text=self.a[x][y][0][1])
                else:
                    if self.a[x][y][0][0] == 'f':
                        
                        w.create_rectangle([3 + 50 * y, 3 + 50 * x, 53 + 50 * y, 53 + 50 * x ], fill="green")
                        w.create_text(3 + 50 * y, 3 + 50 * x, anchor=NW, fill="white", text=self.a[x][y][0][1])
                    elif self.a[x][y][0][0] == 'w':
                        w.create_rectangle([3 + 50 * y, 3 + 50 * x, 53 + 50 * y, 53 + 50 * x ], fill="blue")
                        w.create_text(3 + 50 * y, 3 + 50 * x, anchor=NW, fill="white", text=self.a[x][y][0][1])
                    elif self.a[x][y][0][0] == 'X':
                        w.create_rectangle([3 + 50 * y, 3 + 50 * x, 53 + 50 * y, 53 + 50 * x ], fill="brown")
                        w.create_text(3 + 50 * y, 3 + 50 * x, anchor=NW, fill="white", text=self.a[x][y][0][1])
                    elif self.a[x][y][0][0] == 's':
                        w.create_rectangle([3 + 50 * y, 3 + 50 * x, 53 + 50 * y, 53 + 50 * x ], fill="gray")
                        w.create_text(3 + 50 * y, 3 + 50 * x, anchor=NW, fill="white", text=self.a[x][y][0][1])
        master.after(10000, lambda: master.destroy())
        master.mainloop()
 
    def grow(self):
        #http://stackoverflow.com/questions/1474489/python-weather-api
        data = urllib.request.urlopen('http://api.openweathermap.org/data/2.1/weather/city/4351977?units=imperial')
        s = data.read().decode("utf-8")
        cities = json.loads(s)
        temp = cities['main']['temp']
        for x, row in enumerate(self.a):
            for y, cell in enumerate(row):
                if self.a[x][y][0][0] == 'f':
                    self.a[x][y][0][1] += 1
                    if temp in range(60, 80):
                        self.a[x][y][0][1] += 1
                    neighbors = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1), ]
                    for i in neighbors:
                        if i[0] in range(10) and i[1] in range(10):
                            if self.a[i[0]][i[1]][0][0] == 'w':
                                self.a[x][y][0][1] += 1
                                break
                    if cities.get('rain') != None:
                        self.a[x][y][0][1] += 1
