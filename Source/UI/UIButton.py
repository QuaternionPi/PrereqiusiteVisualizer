# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
from .UIClickable import UIClickable
from .UILabel import UILabel

def lerp(start, end, t):
    return start*(1-t) + end*t

def DoNothing():
    pass

class UIButton (UILabel, UIClickable):
    def __init__ (self, x, y, width, height, text, 
                  onClickEvent    = DoNothing, onClickEventArgs   = (), 
                  onClickHold     = DoNothing, onClickHoldArgs    = (), 
                  onMouseOver     = DoNothing, onMouseOverArgs    = (), 
                  onMouseNotOver  = DoNothing, onMouseNotOverArgs = (),
                  textColor = (0, 0, 0), fontName = "ebrima", centered = False,
                  baseBackgroundColor = (255, 255, 255), mousedColor = (127, 127, 127)):
        UIClickable.__init__(self, x, y, width, height)
        UILabel.__init__(self, x, y, width, height, text, fontName, textColor, baseBackgroundColor, centered = centered)
        self.text = text

        self.onClickEvent       = onClickEvent
        self.onClickEventArgs   = onClickEventArgs
        self.onClickHold        = onClickHold
        self.onClickHoldArgs    = onClickHoldArgs
        self.onMouseOver        = onMouseOver
        self.onMouseOverArgs    = onMouseOverArgs
        self.onMouseNotOver     = onMouseNotOver
        self.onMouseNotOverArgs = onMouseNotOverArgs
        
        self.fontName = fontName

        self.backgroundColor = baseBackgroundColor
        self.textColor = textColor
        self.baseBackgroundColor = baseBackgroundColor
        self.mousedBackgroundColor = mousedColor
        self.transitionAmmount = 0

        self.highlighted = False

        self.RenderText()

    def MouseOverEffect(self):
        if self.moused:
            self.transitionAmmount = max(self.transitionAmmount - 0.04, 0)
        else:
            self.transitionAmmount = min(self.transitionAmmount + 0.04, 1)
        if 1 > self.transitionAmmount > 0:
            R = lerp(self.mousedBackgroundColor[0], self.baseBackgroundColor[0], self.transitionAmmount)
            G = lerp(self.mousedBackgroundColor[1], self.baseBackgroundColor[1], self.transitionAmmount)
            B = lerp(self.mousedBackgroundColor[2], self.baseBackgroundColor[2], self.transitionAmmount)
            self.backgroundColor = (R, G, B)

    def Interaction(self, mousePosition, isMouseDown):
        self.TestMouseOver(mousePosition)
        self.TestClickedOn(isMouseDown)

        if self.clickedEvent:
            self.onClickEvent(*self.onClickEventArgs)
        if self.clickedHold:
            self.onClickHold(*self.onClickHoldArgs)
        if self.moused:
            self.onMouseOver(*self.onMouseOverArgs)
        else:
            self.onMouseNotOver(*self.onMouseNotOverArgs)

        self.MouseOverEffect()