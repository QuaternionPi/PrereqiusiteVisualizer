# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
import sys
import time
from .UI.UIText import RenderTextToSize
pygame.init()

class Screens(object):
    Screen = pygame.display.set_mode((1400, 700))

    ActiveScreen = "menu"
    def DrawStartMessage():
        pygame.display.set_caption('Prequisite Visualizer 0.6.2')

        Message = "Prerequisite Visualizer by David Wiebe"
        RenderedMessage = RenderTextToSize(60, "ebrima", Message, (0, 0, 0))

        Screens.Screen.fill((240, 240, 240))
        Screens.Screen.blit(RenderedMessage, (40, 40))
        pygame.display.update()

    def ExitAll():
        pygame.quit()
        sys.exit()

    def SetSelectorScreen():
        Screens.ActiveScreen = "selector"

    def SetMenuScreen():
        Screens.ActiveScreen = "menu"

    def SetVisualizerScreen():
        Screens.ActiveScreen = "visualizer"
Screens.DrawStartMessage()
print("Prequisite Visualizer 0.6.2")
print("This copy is for demonstraition purposes only")
print("Do Not Redistribute")
time.sleep(3)