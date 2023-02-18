# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

from .Commons import *
from .Screens import Screens
from .Menu.Menus import Menus
from .Menu.SettingsMenu import SettingsMenu
from .Menu.SubjectChangeMenu import SubjectChangeMenu
from .Menu.InfoMenu import InfoMenu
from .UI.UIButton import UIButton

class Menu(object):
	HorizontalSpacing = 20
	VerticalSpacing = 20

	VisualizerButtonX = HorizontalSpacing
	VisualizerButtonY = VerticalSpacing
	VisualizerButtonWidth = 200
	VisualizerButtonHeight = 40
	VisualizerButton = UIButton(0, 0, VisualizerButtonWidth, VisualizerButtonHeight, "Visualizer", onClickEvent = Screens.SetVisualizerScreen)

	MainPaneX = HorizontalSpacing + VisualizerButtonWidth + VisualizerButtonX
	MainPaneY = VerticalSpacing

	SettingsButtonX = HorizontalSpacing
	SettingsButtonY = VerticalSpacing + VisualizerButtonHeight + VisualizerButtonY
	SettingsButtonWidth = 200
	SettingsButtonHeight = 40
	SettingsButton = UIButton(0, 0, SettingsButtonWidth, SettingsButtonHeight, "Settings", onClickEvent = Menus.SetSettingsMenu)

	SubjectChangeButtonX = HorizontalSpacing
	SubjectChangeButtonY = VerticalSpacing + SettingsButtonHeight + SettingsButtonY
	SubjectChangeButtonWidth = 200
	SubjectChangeButtonHeight = 40
	SubjectChangeButton = UIButton(0, 0, SubjectChangeButtonWidth, SubjectChangeButtonHeight, "File Select", onClickEvent = Menus.SetSubjectChangeMenu)

	InfoButtonX = HorizontalSpacing
	InfoButtonY = VerticalSpacing + SubjectChangeButtonHeight + SubjectChangeButtonY
	InfoButtonWidth = 200
	InfoButtonHeight = 40
	InfoButton = UIButton(0, 0, InfoButtonWidth, InfoButtonHeight, "Information", onClickEvent = Menus.SetInfoMenu)

	ExitButtonX = HorizontalSpacing
	ExitButtonY = VerticalSpacing + InfoButtonHeight + InfoButtonY
	ExitButtonWidth = 200
	ExitButtonHeight = 40
	ExitButton = UIButton(0, 0, ExitButtonWidth, ExitButtonHeight, "Exit", onClickEvent = Screens.ExitAll)


	def Interaction(mousePosition, isMouseDown):
		MousePositionRelativeToVisualizerButton = mousePosition[0] - Menu.VisualizerButtonX, mousePosition[1] - Menu.VisualizerButtonY
		Menu.VisualizerButton.Interaction(MousePositionRelativeToVisualizerButton, isMouseDown)
		
		MousePositionRelativeToSettingsButton = mousePosition[0] - Menu.SettingsButtonX, mousePosition[1] - Menu.SettingsButtonY
		Menu.SettingsButton.Interaction(MousePositionRelativeToSettingsButton, isMouseDown)
		
		MousePositionRelativeToSubjectChangeButton = mousePosition[0] - Menu.SubjectChangeButtonX, mousePosition[1] - Menu.SubjectChangeButtonY
		Menu.SubjectChangeButton.Interaction(MousePositionRelativeToSubjectChangeButton, isMouseDown)
		
		MousePositionRelativeToInfoButton = mousePosition[0] - Menu.InfoButtonX, mousePosition[1] - Menu.InfoButtonY
		Menu.InfoButton.Interaction(MousePositionRelativeToInfoButton, isMouseDown)
		
		MousePositionRelativeToExitButton = mousePosition[0] - Menu.ExitButtonX, mousePosition[1] - Menu.ExitButtonY
		Menu.ExitButton.Interaction(MousePositionRelativeToExitButton, isMouseDown)

		MousePositionRelativeToMainPane = mousePosition[0] - Menu.MainPaneX, mousePosition[1] - Menu.MainPaneY
		if Menus.ActiveMenu == "settings":
			pass
		elif Menus.ActiveMenu == "subjectchange":
			SubjectChangeMenu.Interaction(MousePositionRelativeToMainPane, isMouseDown)
		elif Menus.ActiveMenu == "info":
			pass

	def HandleKeyPress(event):
		pass

	def Draw(screen):
		screen.fill((137, 207, 240))
		Menu.VisualizerButton.Draw(screen.subsurface(Menu.VisualizerButtonX, Menu.VisualizerButtonY, Menu.VisualizerButtonWidth, Menu.VisualizerButtonHeight))
		Menu.SettingsButton.Draw(screen.subsurface(Menu.SettingsButtonX, Menu.SettingsButtonY, Menu.SettingsButtonWidth, Menu.SettingsButtonHeight))
		Menu.SubjectChangeButton.Draw(screen.subsurface(Menu.SubjectChangeButtonX, Menu.SubjectChangeButtonY, Menu.SubjectChangeButtonWidth, Menu.SubjectChangeButtonHeight))
		Menu.InfoButton.Draw(screen.subsurface(Menu.InfoButtonX, Menu.InfoButtonY, Menu.InfoButtonWidth, Menu.InfoButtonHeight))
		Menu.ExitButton.Draw(screen.subsurface(Menu.ExitButtonX, Menu.ExitButtonY, Menu.ExitButtonWidth, Menu.ExitButtonHeight))
	
		ScreenX, ScreenY = screen.get_size()
		surface = screen.subsurface(Menu.MainPaneX, Menu.MainPaneY, ScreenX - Menu.MainPaneX - Menu.HorizontalSpacing, ScreenY - Menu.MainPaneY - Menu.VerticalSpacing)

		if Menus.ActiveMenu == "settings":
			SettingsMenu.Draw(surface)
		elif Menus.ActiveMenu == "subjectchange":
			SubjectChangeMenu.Draw(surface)
		elif Menus.ActiveMenu == "info":
			InfoMenu.Draw(surface)