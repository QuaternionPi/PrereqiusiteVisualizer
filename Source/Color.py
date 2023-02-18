# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

from colorsys import hsv_to_rgb

# The dict of colors for the program
Colors = {}

Colors["LightGrey"] =     (180, 180, 180)
Colors["MidGrey"] =       (128, 128, 128)
Colors["DarkGrey"] =      (80,  80,  80)

Colors["GreenBase"] =     (8,   255, 87)
Colors["GreenDimmed"] =   (5,   179, 61)
Colors["GreenDulled"] =   (70,  179, 130)
Colors["GreenDarkened"] = (5,   102, 54)

Colors["BlueBase"] =      (20,  255, 230)
Colors["BlueDimmed"] =    (14,  179, 162)
Colors["BlueDulled"] =    (81,  179, 175)
Colors["BlueDarkened"] =  (6,   102, 96)

Colors["YellowBase"] =    (240, 200, 0)
Colors["YellowDimmed"] =  (180, 160, 0)
Colors["YellowDulled"] =  (21,  21,  0)
Colors["YellowDarkened"] =(0,   0,   0)

Colors["RedBase"] =       (255, 50,  46)
Colors["RedDimmed"] =     (179, 35,  32)
Colors["RedDulled"] =     (179, 109, 98)
Colors["RedDarkened"] =   (128, 26,  13)


def ColorsFromStatus(status):
    if status == "Complete":
        return Colors["GreenBase"], Colors["GreenDimmed"], Colors["GreenDulled"], Colors["GreenDarkened"]
    elif status == "Avaliable":
        return Colors["BlueBase"], Colors["BlueDimmed"], Colors["BlueDulled"], Colors["BlueDarkened"]
    elif status == "Unavaliable":
        return Colors["RedBase"], Colors["RedDimmed"], Colors["RedDulled"], Colors["RedDarkened"]
    else:
        return (0, 0, 0), (0, 0, 0), (0, 0, 0)

# A way of racheting around a range in a modular fasion
class ModularPosition(object):
    def __init__(self, range, modulus, position = 0, step = 0):
        self.range = range
        self.modulus = modulus
        self.position = position
        if step:
            self.step = step
        else:
            self.step = modulus/1.2
    def NextPosition(self):
        self.position += self.step
        self.position %= self.modulus
        return self.position/self.modulus*(self.range[1]-self.range[0]) + self.range[0]

# Procedurally creates colors 
class ColorCreator(object):
    h = ModularPosition((-0.2, 0.6),23)
    s = ModularPosition((0.2, 1),7)
    v = ModularPosition((0.7, 1),3)

    def NewColor():
        H = ColorCreator.h.NextPosition()%1 # keeps between [0,1)
        S = ColorCreator.s.NextPosition()
        V = ColorCreator.v.NextPosition()
        R, G, B = hsv_to_rgb(H, S, V)
        return 255*R, 255*G, 255*B
