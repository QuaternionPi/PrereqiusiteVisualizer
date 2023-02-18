import pygame
from Screens import Screens
from .UI.UIText import RenderTextToSize

class Selector():
    Ready = False
    SelectedFile = False
    Buttons = []
    
    def Interaction(mousePosition, isMouseDown):
        pass

    def HandleKeyPress(event):
        pass

    def Draw(surface):

        Message = "Hello World"
        RenderedMessage = RenderTextToSize(60, "ebrima", Message, (0, 0, 0))

        Screens.Screen.fill((240, 240, 240))
        Screens.Screen.blit(RenderedMessage, (40, 40))
        pygame.display.update()
