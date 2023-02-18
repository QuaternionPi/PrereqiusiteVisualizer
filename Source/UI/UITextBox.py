# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
from ..Color import Colors
from .UIButton import UIButton
from .UIText import RenderTextToFit

def IsALetter(character):
    return character.isalpha()

def IsANumber(character):
    return character.isdigit()

def IsALetterOrNumber(character):
    return IsALetter(character) or IsANumber(character)

class UITextBox(UIButton):
    def __init__ (self, x, y, width, height, defaultText, function, requirments, maxLength = 50, forceUpperCase = False, forceLowerCase = False):
        super().__init__(x, y, width, height, '', self.MarkAsHighlighted)
        self.defaultText = defaultText
        self.function = function
        self.requirments = requirments
        self.maxLength = maxLength
        self.forceUpperCase = forceUpperCase
        self.forceLowerCase = forceLowerCase
        self.text = ''
        self.RenderText(text = self.defaultText, color = Colors["LightGrey"])

    def MarkAsHighlighted(self):
        self.highlighted = True

    def MarkAsNotHighlighted(self):
        self.highlighted = False

    def Interaction(self, screenOffsetX, screenOffsetY):
        super().Interaction(screenOffsetX, screenOffsetY)
        if pygame.mouse.get_pressed()[0] and self.moused == False:
            self.MarkAsNotHighlighted()

            
    def HandleKeyPress(self, event):
        if self.highlighted:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                letter = event.unicode
                for requirment in self.requirments:
                    if requirment(letter) == False:
                        return

                self.text += letter
                if self.forceUpperCase:
                    self.text = self.text.upper()
                elif self.forceLowerCase:
                    self.text = self.text.lower()

                if len(self.text) > self.maxLength:
                    self.text = self.text[:self.maxLength]

            if len(self.text) == 0:
                self.RenderText(text = self.defaultText, color = Colors["LightGrey"])
            else:
                self.RenderText()
            self.function(self.text)
