# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
from .Menus import Menus
from ..UI.UILabel import UIMultiLineLabel

class InfoMenu:
	text =  '''The Prerequisites Visualizer is a program to view and visualy understand course requirments. 

To begin, click "File Select". 
Then Click "Add Row" under both "Course Files" and "Grades Files"
Select one of the supplied files for each.
Then click "Apply", then click "Visualizer".

Once at the visualizer repeatedly click on a course to see all posible prerequisites.

Written by David Wiebe.
Version 0.6.2.
Last edit: 2023/01/23.
For demonstraition purposes only.
Do Not Redistribute.
'''
	Label = UIMultiLineLabel(0, 0, 100, 100, text)

	def Interaction(screenOffsetX, ScreenOffsetY):
		pass

	def HandleKeyPress(event):
		pass

	def Draw(surface):
		InfoMenu.Label.width, InfoMenu.Label.height = surface.get_size()
		InfoMenu.Label.rect = pygame.Rect(0, 0, *surface.get_size())
		InfoMenu.Label.UpdateText()
		InfoMenu.Label.Draw(surface)