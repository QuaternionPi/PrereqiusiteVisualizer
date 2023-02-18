# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

from .Screens import Screens
from .Visualizer.Graphing.HierarchicalGraph import HierarchicalGraph
from .Visualizer.InfoPane import InfoPane
from .UI.UIButton import UIButton
from .UI.UITextBox import UITextBox
from .UI.UITextBox import IsALetterOrNumber

class Visualizer(object):
	HorizontalSpacing = 20
	VerticalSpacing = 20

	Graph = HierarchicalGraph()
	
	MenuButtonX = HorizontalSpacing
	MenuButtonY = VerticalSpacing
	MenuButtonWidth = 200
	MenuButtonHeight = 40
	MenuButton = UIButton(0, 0, MenuButtonWidth, MenuButtonHeight, "Menu", onClickEvent = Screens.SetMenuScreen)

	ResetButtonX = HorizontalSpacing
	ResetButtonY = VerticalSpacing + MenuButtonHeight + MenuButtonY
	ResetButtonWidth = 200
	ResetButtonHeight = 40
	ResetButton = UIButton(0, 0, ResetButtonWidth, ResetButtonHeight, "Reset", onClickEvent = Graph.Reset)

	SearchBarX = HorizontalSpacing
	SearchBarY = VerticalSpacing + ResetButtonHeight + ResetButtonY
	SearchBarWidth = 200
	SearchBarHeight = 40
	SearchBar = UITextBox(0, 0, SearchBarWidth, SearchBarHeight, "Search", Graph.SearchText, [IsALetterOrNumber], 10, forceUpperCase = True)
	
	InfoPaneX = HorizontalSpacing
	InfoPaneY = VerticalSpacing + SearchBarHeight + SearchBarY
	InfoPaneWidth = 200
	InfoPaneHeight = 140
	InfoPane = InfoPane(0, 0, InfoPaneWidth, InfoPaneHeight)
	
	GraphX = 2*HorizontalSpacing + max(InfoPaneWidth, ResetButtonWidth, SearchBarWidth)
	GraphY = VerticalSpacing

	def Interaction(mousePosition, isMouseDown):
		MousePositionRelativeToMenuButton = mousePosition[0] - Visualizer.MenuButtonX, mousePosition[1] - Visualizer.MenuButtonY
		Visualizer.MenuButton.Interaction(MousePositionRelativeToMenuButton, isMouseDown)

		MousePositionRelativeToResetButton = mousePosition[0] - Visualizer.ResetButtonX, mousePosition[1] - Visualizer.ResetButtonY
		Visualizer.ResetButton.Interaction(MousePositionRelativeToResetButton, isMouseDown)

		MousePositionRelativeToSearchBar = mousePosition[0] - Visualizer.SearchBarX, mousePosition[1] - Visualizer.SearchBarY
		Visualizer.SearchBar.Interaction(MousePositionRelativeToSearchBar, isMouseDown)

		MousePositionRelativeToGraph = mousePosition[0] - Visualizer.GraphX, mousePosition[1] - Visualizer.GraphY
		Visualizer.Graph.Interaction(MousePositionRelativeToGraph, isMouseDown)
		if Visualizer.Graph.clickedEvent:
			Visualizer.InfoPane.ChangeCard(Visualizer.Graph.clickedCard)


	def HandleKeyPress(event):
		Visualizer.SearchBar.HandleKeyPress(event)

	def Draw(screen):
		screen.fill((137, 207, 240))

		ScreenX, ScreenY = screen.get_size()

		Visualizer.Graph.Draw(screen.subsurface(Visualizer.GraphX, Visualizer.GraphY, ScreenX - Visualizer.GraphX - Visualizer.HorizontalSpacing, ScreenY - Visualizer.GraphY - Visualizer.VerticalSpacing))
	
		Visualizer.ResetButton.Draw(screen.subsurface(Visualizer.ResetButtonX, Visualizer.ResetButtonY, Visualizer.ResetButtonWidth, Visualizer.ResetButtonHeight))

		Visualizer.MenuButton.Draw(screen.subsurface(Visualizer.MenuButtonX, Visualizer.MenuButtonY, Visualizer.MenuButtonWidth, Visualizer.MenuButtonHeight))

		Visualizer.SearchBar.Draw(screen.subsurface(Visualizer.SearchBarX, Visualizer.SearchBarY, Visualizer.SearchBarWidth, Visualizer.SearchBarHeight))
	
		Visualizer.InfoPane.Draw(screen.subsurface(Visualizer.InfoPaneX, Visualizer.InfoPaneY, Visualizer.InfoPaneWidth, ScreenY - Visualizer.InfoPaneY - Visualizer.VerticalSpacing))