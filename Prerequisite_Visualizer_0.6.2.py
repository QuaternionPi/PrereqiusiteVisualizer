# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
from Source.Screens import Screens
from Source.MenuScreen import Menu
from Source.VisualizerScreen import Visualizer
from Source.SelectorScreen import Selector

def InteractionScreen():
    MousePosition = pygame.mouse.get_pos()
    IsMouseDown = pygame.mouse.get_pressed()[0]
    match Screens.ActiveScreen:
        case "menu":
            Menu.Interaction(MousePosition, IsMouseDown)
        case "visualizer":
            Visualizer.Interaction(MousePosition, IsMouseDown)
        case "selector":
            Selector.Interaction(MousePosition, IsMouseDown)

def HandleKeyPress(event):
    match Screens.ActiveScreen:
        case "menu":
            Menu.HandleKeyPress(event)
        case "visualizer":
            Visualizer.HandleKeyPress(event)
        case "selector":
            Selector.HandleKeyPress(event)

def DrawScreen():
    match Screens.ActiveScreen:
        case "menu":
            Menu.Draw(Screens.Screen)
        case "visualizer":
            Visualizer.Draw(Screens.Screen)
        case "selector":
            Selector.Draw(Screens.Screen)
        
# main loop
while True:
    UserHasInteracted = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        UserHasInteracted = True
        if event.type == pygame.QUIT:
            Screens.ExitAll()
        elif event.type == pygame.KEYDOWN:
            HandleKeyPress(event)
            
    if UserHasInteracted:
        InteractionScreen()
        DrawScreen()
        pygame.display.update()
