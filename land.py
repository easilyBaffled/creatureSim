class Land():
    def __init__(self):
        self.elevation = 0
        self.neighbors = []
        self.creatures = []
        self.location = (0, 0)
        self.was = None#to keep track of when flooded     
    def __str__(self):
        return("location " + str(self.location) + 
               " elevation " + str(self.elevation) + 
               " neighbors " + str(len(self.neighbors)) + 
               " creatures " + str(x.name for x in self.creatures) + " | ")
    def redefine(self, land):
        self.elevation = land.elevation
        self.neighbors = land.neighbors
        self.creatures = land.creatures
        self.location = land.location
        self.was = land


class Water(Land):
    def __init__(self):
        Land.__init__(self)
        self.waterLevel = self.elevation
    def __str__(self):
        return("location " + str(self.location) + 
               " elevation " + str(self.elevation) + 
               " neighbors " + str(len(self.neighbors)) + 
               " creatures " + str(x.name for x in self.creatures) + 
               " water level " + str(self.waterLevel) + " | ")
    def flood(self):
        if self.waterLevel > self.elevation:
            for land in self.neighbors:
                newLand = Water()
                newLand.redefine(land)
                newLand.waterLevel = self.waterLevel - 1
                self.waterLevel = self.elevation
                newLand.flood()


class Food(Land):
    def __init__(self):
        Land.__init__(self)
        self.vegitation = 1
    def __str__(self):
        return("location " + str(self.location) + 
               " elevation " + str(self.elevation) + 
               " neighbors " + str(len(self.neighbors)) + 
               " creatures " + str(x.name for x in self.creatures) + 
               " vegetation " + str(self.vegitation) + " | ")
    def grow(self, tempurature, rain):
        self.vegitation += 1
        if 50 < tempurature < 80:
            self.vegitation += 1
        if rain != None and rain != 0:
            self.vegitation += 1
        for land in self.neighbors:
            if type(land) is Water:
                self.vegitation += 1


class Shelter(Land):
    def __init__(self):
        Land.__init__(self)
        self.quality = 1
        self.foodStorage = 0
        self.owner = None#just the name of the creature
    def __str__(self):
        return("location " + str(self.location) + 
               " elevation " + str(self.elevation) + 
               " neighbors " + str(len(self.neighbors)) + 
               " creatures " + str(x.name for x in self.creatures) + 
               " quality " + str(self.quality) + 
               " food storage " + str(self.foodStorage) + 
               " owner" + str(self.owner.__class__) + " | ")


aa = Water()
aa.elevation = 4
aa.location = (0, 0)
aa.waterLevel = 4

ab = Food()
ab.elevation = 3
ab.location = (0, 1)

ac = Land()
ac.elevation = 2
ac.location = (0, 2)

ad = Land()
ad.elevation = 3
ad.location = (0, 3)

ae = Land()
ae.elevation = 2
ae.location = (0, 4)

af = Land()
af.elevation = 3
af.location = (0, 5)

ag = Land()
ag.elevation = 3
ag.location = (0, 6)

ah = Land()
ah.elevation = 2
ah.location = (0, 7)

ai = Food()
ai.elevation = 1
ai.location = (0, 8)

aj = Land()
aj.elevation = 2
aj.location = (0, 9)

ba = Water()
ba.elevation = 3
ba.location = (1, 0)
ba.waterLevel = 3

bb = Water()
bb.elevation = 3
bb.location = (1, 1)
bb.waterLevel = 3

bc = Land()
bc.elevation = 2
bc.location = (1, 2)

bd = Land()
bd.elevation = 2
bd.location = (1, 3)

be = Food()
be.elevation = 0
be.location = (1, 4)

bf = Land()
bf.elevation = 0
bf.location = (1, 5)

bg = Shelter()
bg.elevation = 0
bg.location = (1, 6)

bh = Land()
bh.elevation = 1
bh.location = (1, 7)

bi = Land()
bi.elevation = 2
bi.location = (1, 8)

bj = Land()
bj.elevation = 3
bj.location = (1, 9)

ca = Shelter()
ca.elevation = 2
ca.location = (2, 0)

cb = Water()
cb.elevation = 2
cb.location = (2, 1)
cb.waterLevel = 2

cc = Land()
cc.elevation = 2
cc.location = (2, 2)
cc.waterLevel = 2

cd = Land()
cd.elevation = 1
cd.location = (2, 3)

ce = Land()
ce.elevation = 0
ce.location = (2, 4)

cf = Land()
cf.elevation = 0
cf.location = (2, 5)

cg = Land()
cg.elevation = 1
cg.location = (2, 6)

ch = Land()
ch.elevation = 2
ch.location = (2, 7)

ci = Land()
ci.elevation = 3
ci.location = (2, 8)

cj = Food()
cj.elevation = 4
cj.location = (2, 9)

da = Land()
da.elevation = 1
da.location = (3, 0)

db = Food()
db.elevation = 1
db.location = (3, 1)

dc = Water()
dc.elevation = 1
dc.location = (3, 2)
dc.waterLevel = 1

dd = Water()
dd.elevation = 1
dd.location = (3, 3)
dd.waterLevel = 1

de = Land()
de.elevation = 1
de.location = (3, 4)

df = Land()
df.elevation = 1
df.location = (3, 5)

dg = Land()
dg.elevation = 1
dg.location = (3, 6)

dh = Land()
dh.elevation = 2
dh.location = (3, 7)

di = Land()
di.elevation = 3
di.location = (3, 8)

dj = Shelter()
dj.elevation = 4
dj.location = (3, 9)

ea = Land()
ea.elevation = 0
ea.location = (4, 0)

eb = Land()
eb.elevation = 0
eb.location = (4, 1)

ec = Water()
ec.elevation = 0
ec.location = (4, 2)
ec.waterLevel = 0

ed = Water()
ed.elevation = 0
ed.location = (4, 3)
ed.waterLevel = 0

ee = Water()
ee.elevation = 0
ee.location = (4, 4)
ee.waterLevel = 0

ef = Water()
ef.elevation = 0
ef.location = (4, 5)
ef.waterLevel = 0

eg = Land()
eg.elevation = 0
eg.location = (4, 6)

eh = Land()
eh.elevation = 0
eh.location = (4, 7)

ei = Food()
ei.elevation = 2
ei.location = (4, 8)

ej = Land()
ej.elevation = 3
ej.location = (4, 9)

fa = Land()
fa.elevation = 1
fa.location = (5, 0)

fb = Land()
fb.elevation = 1
fb.location = (5, 1)

fc = Food()
fc.elevation = 1
fc.location = (5, 2)

fd = Land()
fd.elevation = 1
fd.location = (5, 3)

fe = Food()
fe.elevation = 0
fe.location = (5, 4)

ff = Land()
ff.elevation = 0
ff.location = (5, 5)

fg = Food()
fg.elevation = 0
fg.location = (5, 6)

fh = Land()
fh.elevation = 1
fh.location = (5, 7)

fi = Food()
fi.elevation = 2
fi.location = (5, 8)

fj = Land()
fj.elevation = 3
fj.location = (5, 9)

ga = Land()
ga.elevation = 2
ga.location = (6, 0)

gb = Land()
gb.elevation = 1
gb.location = (6, 1)

gc = Water()
gc.elevation = 0
gc.location = (6, 2)
gc.waterLevel = 0

gd = Water()
gd.elevation = 0
gd.location = (6, 3)
gd.waterLevel = 0

ge = Water()
ge.elevation = 0
ge.location = (6, 4)
ge.waterLevel = 0

gf = Water()
gf.elevation = 0
gf.location = (6, 5)
gf.waterLevel = 0

gg = Land()
gg.elevation = 0
gg.location = (6, 6)

gh = Land()
gh.elevation = 1
gh.location = (6, 7)

gi = Land()
gi.elevation = 2
gi.location = (6, 8)

gj = Land()
gj.elevation = 3
gj.location = (6, 9)

ha = Land()
ha.elevation = 2
ha.location = (7, 0)

hb = Food()
hb.elevation = 1
hb.location = (7, 1)

hc = Water()
hc.elevation = 0
hc.location = (7, 2)
hc.waterLevel = 0

hd = Water()
hd.elevation = 0
hd.location = (7, 3)
hd.waterLevel = 0

he = Water()
he.elevation = 0
he.location = (7, 4)
he.waterLevel = 0

hf = Food()
hf.elevation = 0
hf.location = (7, 5)

hg = Food()
hg.elevation = 0
hg.location = (7, 6)

hh = Land()
hh.elevation = 1
hh.location = (7, 7)

hi = Land()
hi.elevation = 1
hi.location = (7, 8)

hj = Land()
hj.elevation = 2
hj.location = (7, 9)

ia = Land()
ia.elevation = 2
ia.location = (8, 0)

ib = Food()
ib.elevation = 1
ib.location = (8, 1)

ic = Land()
ic.elevation = 1
ic.location = (8, 2)

ego = Land()
ego.elevation = 1
ego.location = (8, 3)

ie = Land()
ie.elevation = 1
ie.location = (8, 4)

bob = Land()
bob.elevation = 1
bob.location = (8, 5)

ig = Land()
ig.elevation = 0
ig.location = (8, 6)

ih = Land()
ih.elevation = 1
ih.location = (8, 7)

ii = Food()
ii.elevation = 1
ii.location = (8, 8)

ij = Land()
ij.elevation = 2
ij.location = (8, 9)

ja = Shelter()
ja.elevation = 2
ja.location = (9, 0)

jb = Land()
jb.elevation = 2
jb.location = (9, 1)

jc = Land()
jc.elevation = 1
jc.location = (9, 2)

jd = Land()
jd.elevation = 0
jd.location = (9, 3)

je = Land()
je.elevation = 1
je.location = (9, 4)

jf = Shelter()
jf.elevation = 1
jf.location = (9, 5)

jg = Land()
jg.elevation = 0
jg.location = (9, 6)

jh = Land()
jh.elevation = 2
jh.location = (9, 7)

ji = Land()
ji.elevation = 2
ji.location = (9, 8)

jj = Shelter()
jj.elevation = 2
jj.location = (9, 9)

zero = [aa, ab, ac, ad, ae, af, ag, ah, ai, aj]
first = [ba, bb, bc, bd, be, bf, bg, bh, bi, bj]
second = [ca, cb, cc, cd, ce, cf, cg, ch, ci, cj]
third = [da, db, dc, dd, de, df, dg, dh, di, dj]
fourth = [ea, eb, ec, ed, ee, ef, eg, eh, ei, ej]
fifth = [fa, fb, fc, fd, fe, ff, fg, fh, fi, fj]
sixth = [ga, gb, gc, gd, ge, gf, gg, gh, gi, gj]
seventh = [ha, hb, hc, hd, he, hf, hg, hh, hi, hj]
eighth = [ia, ib, ic, ego, ie, bob, ig, ih, ii, ij]
ninth = [ja, jb, jc, jd, je, jf, jg, jh, ji, jj]
landMass = [zero, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth ]

for x, row in enumerate(landMass):
        for y, cell in enumerate(row):
            neighbors = []
            if x > 0:
                neighbors.append(landMass[x - 1][y])

            if x < 9:
                neighbors.append(landMass[x + 1][y])
            if y > 0:
                neighbors.append(landMass[x][y - 1])
            if y < 9:
                neighbors.append(landMass[x][y + 1])
            landMass[x][y].neighbors = neighbors


class DictMap():
    def __init__(self, landMass):
        self.map = []
        self.land = landMass
        for x, row in enumerate(landMass):
            innerDict = []
            for y, cell in enumerate(row):
                innerDict.append(cell.toDict())
            self.map.append(innerDict)

"""
from Tkinter import *

class Map():
    def __init__(self,):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=1200 , height=1200)
        self.canvas.pack()
        self.colors = {
            "Land": "grey",
            "Food": "green",
            "Water": "blue",
            "Shelter": "black"
        }
        self.canvasDict = {}  # the keys are (x,y, "type"), the data is the id so it can be grabbed for item config.
        for i, row in enumerate(landMass):
            for j, tile in enumerate(row):
                color = self.colors[tile.__class__.__name__]
                self.canvasDict[i,j,"tile"] = self.canvas.create_rectangle(50 * i, 50 * j, 50 * (i + 1), 50 * (j + 1),
                                                                           outline=color, fill=color)
                info = tile.elevation
                if color == "green":
                    info = tile.vegitation
                elif color == "black":
                    info = tile.quality

                self.canvasDict[i, j, "text"] = self.canvas.create_text(50 * i +3, 50 * j, anchor=NW, fill="white", text=info)
        self.canvasDict["creature"] = self.canvas.create_rectangle(0, 0, 50, 50,
                                                                   outline="red", fill="red")
        self.canvas.pack(fill=BOTH, expand=1)
        sim = simulation.Simulation([], 1, 1, self.root, self.canvas, self.canvasDict)
        self.root.after(0, sim.simulate)
        self.root.mainloop()
"""