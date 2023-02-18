# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame

def RenderTextToFit(width, height, fontName, text, color, maxSize = False):
    # reduces the font size until it fits within the drawbox
    Size = int(height)
    if maxSize:
        Size = maxSize
    while True:
        RenderedFont = RenderTextToSize(Size, fontName, text, color)
        ReduceFontSize = RenderedFont.get_size()[0] > width
        if ReduceFontSize == False:
            return RenderedFont, Size - 1
        Size -= 1

def RenderTextToSize(size, fontName, text, color):
    Font = pygame.font.SysFont(fontName, size, False)
    return Font.render(text, True, color)