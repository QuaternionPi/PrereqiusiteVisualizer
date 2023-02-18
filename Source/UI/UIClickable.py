# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame

class UIClickable(object):
    lockOut = False
    def __init__ (self, x, y, width, height):
        self.clickedEvent = False
        self.clickedHold = False
        self.moused = False
        self.rect = pygame.Rect(x, y, width, height)

    # Tests for if the mouse is over the hitbox
    def TestMouseOver(self, mousePosition):
        self.moused = self.rect.collidepoint(mousePosition)
        return self.moused

    # Tests for if the hitbox is clicked on
    def TestClickedOn(self, isMouseDown):
        self.clickedEvent = False
        if self.moused and isMouseDown and UIClickable.lockOut == False:
            UIClickable.lockOut = True
            self.clickedEvent = True
            self.clickedHold = True
            return True

        elif isMouseDown == False:
            UIClickable.lockOut = False
            self.clickedHold = False
        return False

