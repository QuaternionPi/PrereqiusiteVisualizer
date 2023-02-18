# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame 
from ...Commons import *
from ...Color import ColorCreator
from ...Color import ColorsFromStatus
from ...Color import Colors
from ...UI.UIText import RenderTextToFit
from ...UI.UIText import RenderTextToSize
from ...UI.UIClickable import UIClickable

# Cards are the rectangular objects drawn to the screen
class Card(VisualBase, UIClickable):
    def __init__(self, parent, x, y, width, height):
        UIClickable.__init__(self, x, y, width, height)
        VisualBase.__init__(self, parent)
        self.rootX = x
        self.rootY = y
        self.bufferX = 4
        self.bufferY = 1

        self.connection = self.rect.midtop # where lines comming to and from this card attach
    
        self.colorBase, self.colorDimmed, self.colorDulled, self.textColor = ColorsFromStatus(self.parent.status)
        self.backgroundColor = self.colorBase
        self.borderColor = Colors["LightGrey"]
        self.dependantColor = ColorCreator.NewColor() # Gets a new color from the color creative
        
        self.fontName = "ebrima"
        MaxSize = 20
        self.renderedName, Size = RenderTextToFit(width - 2*self.bufferX, height - 2*self.bufferY, self.fontName, self.name, self.textColor, MaxSize)
        self.renderedGrade = RenderTextToSize(Size, self.fontName, self.parent.grade, self.textColor)

        self.showGrade = self.parent.grade != "F"

        parent.parent.Show(self, 2) # Is shown on startup


    def UpdateRect(self):
        self.rect = pygame.Rect(self.rootX + VisualBase.offsetX, self.rootY + VisualBase.offsetY, self.rect.width, self.rect.height)

    def UpdateColor(self):
        if self.dulled:
            self.borderColor = Colors["DarkGrey"]
        else:
            self.borderColor = Colors["LightGrey"]
        if self.moused:
            self.backgroundColor = self.colorDimmed
        elif self.dulled:
            self.backgroundColor = self.colorDulled
        else:
            self.backgroundColor = self.colorBase


    def Interaction(self, mousePosition, isMouseDown):
        self.TestMouseOver(mousePosition)
        self.TestClickedOn(isMouseDown)

    # Draws the line to surface
    def Draw(self, surface):
        pygame.draw.rect(surface, self.backgroundColor, self.rect)
        surface.blit(self.renderedName,      (self.rect.topleft[0] + self.bufferX, self.rect.topleft[1] + self.bufferY))
        if self.showGrade:
            surface.blit(self.renderedGrade, (self.rect.topleft[0] + self.bufferX, self.rect.topleft[1] + self.renderedName.get_size()[1] - 4))
        pygame.draw.rect(surface, self.borderColor, self.rect, 2)


