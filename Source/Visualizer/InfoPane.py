# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
from ..Commons import *
from ..Color import Colors
from ..UI.UIText import RenderTextToFit
from ..UI.UIText import RenderTextToSize
from ..UI.UILabel import UIMultiLineLabel

class InfoPane(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.size = 18
        self.label = False
        self.drawCardEmulation = False
        self.surfaceSize = (0, 0)

    def ChangeCard(self, card):
        self.Update()
        self.drawCardEmulation = True

        self.backgroundColor = card.colorBase
        self.textColor = card.textColor
        self.fontName = card.fontName

        self.renderedStatus, size = RenderTextToFit(self.rect.width/2, self.rect.height, self.fontName, card.parent.status, self.textColor, 25)
        
        self.renderedName, size = RenderTextToFit(self.rect.width - 10, self.rect.height, self.fontName, card.parent.name, self.textColor, 40)
        
        self.renderedTitle, size = RenderTextToFit(self.rect.width - 10, self.rect.height, self.fontName, card.parent.title, self.textColor, 18)

        if card.parent.grade != "F":
            self.renderedGrade = RenderTextToSize(size, self.fontName, card.parent.grade, self.textColor)

    def Update(self):
        LabelX = 0
        LabelY = self.rect.height + 20
        self.drawCardEmulation = True
        self.label = UIMultiLineLabel(LabelX, LabelY, self.surfaceSize[0], self.surfaceSize[1] - LabelY, self.text, size = self.size)


    def Draw(self, surface):
        if self.drawCardEmulation:
            pygame.draw.rect(surface, self.backgroundColor, self.rect)
            surface.blit(self.renderedName, (self.rect.topleft[0] + 7, self.rect.topleft[1]))
            surface.blit(self.renderedStatus, (self.rect.x + 7, self.rect.y + 50))
            surface.blit(self.renderedTitle, (self.rect.x + 7, self.rect.y + 85))
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
            
        self.surfaceSize = surface.get_size()
        if self.label == False:
            self.text = "Green indicates a course has been taken, blue that it can be taken, red that it cannot be taken. The coloured arrows indicate relivant prerequisites. Touching courses are corequisites."
            self.label = UIMultiLineLabel(0, 0, self.surfaceSize[0], self.surfaceSize[1] - self.rect.height - 20, self.text, size = self.size)
        self.label.Draw(surface)



