# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
from .UIText import RenderTextToFit
from .UIClickable import *

class UILabel (object):
    def __init__ (self, x, y, width, height, text, fontName = "ebrima",
                  textColor = (0, 0, 0), backgroundColor = (255, 255, 255), centered = False):
        self.rect = pygame.Rect(x, y, width, height)
        self.bufferX = 5
        self.bufferY = 3
        self.text = text
        self.fontName = fontName
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.centered = centered
        self.highlighted = False
        self.RenderText()

    def RenderText(self, width = False, height = False, fontName = False, text = False, color = False):
        Width = self.rect.width - 2*self.bufferX
        if width:
            Width = width
        Height = self.rect.height - 2*self.bufferY
        if height:
            Height = height
        FontName = self.fontName
        if fontName:
            FontName = fontName
        Text = self.text
        if text:
            Text = text
        Color = self.textColor
        if color:
            Color = color

        self.renderedFont, Size = RenderTextToFit(Width, Height, FontName, Text, Color)

    def Draw(self, surface):
        pygame.draw.rect(surface, self.backgroundColor, self.rect)
        if self.highlighted:
            pygame.draw.rect(surface, (255, 210, 0), self.rect, 3)
        else:
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        TextX = self.rect.topleft[0] + self.bufferX
        TextY = self.rect.topleft[1] - 5
        if self.centered:
            TextX = self.rect.topleft[0] + (surface.get_size()[0] - self.renderedFont.get_size()[0])/2
        surface.blit(self.renderedFont, (TextX, TextY))


class UIMultiLineLabel(object):
    def __init__ (self, x, y, width, height, text, fontName = "ebrima", size = 25,
                  textColor = (0, 0, 0), backgroundColor = (255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.bufferX = int(width/15)
        self.bufferY = int(height/15)
        self.text = text
        self.fontName = fontName
        self.size = size
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.highlighted = False
        self.RenderText(size)
        self.RenderImage()

    def RenderText(self, fontSize, fontName = False, text = False, color = False):
        FontName = self.fontName
        if fontName:
            FontName = fontName
        Text = self.text
        if text:
            Text = text
        Color = self.textColor
        if color:
            Color = color

        Font = pygame.font.SysFont(FontName, fontSize, False)

        self.rederedText = [[]]
        for line in Text.splitlines():
            for word in line.split(" "):
                self.rederedText[-1].append(Font.render(word + " ", True, Color))
            self.rederedText.append([])

    def RenderImage(self):
        yPosition = 0
        xPosition = 7
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0,0,0), pygame.Rect(0, 0, *self.image.get_size()), 2)
        for layer in self.rederedText:
            for renderedWord in layer:
                Width, Height = renderedWord.get_size()
                if xPosition + Width > self.image.get_size()[0]:
                    xPosition = 7
                    yPosition += Height
                self.image.blit(renderedWord, (xPosition, yPosition))
                xPosition += Width
            xPosition = 7
            yPosition += Height

    def UpdateText(self):
        self.RenderText(self.size)
        self.RenderImage()

    def Draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))