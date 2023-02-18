# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

from ..VisualizerScreen import Visualizer
from .Menus import Menus
from ..UI.UILabel import UILabel
from ..UI.UIButton import UIButton
from ..UI.UIFileDialogue import UIFileDialogueButton
from ..UI.UIDataEntryTower import UIDataEntryTower

class SubjectChangeMenu:
	HorizontalSpacing = 20
	VerticalSpacing = 20
	
	CourseDataLabelX = 0
	CourseDataLabelY = 0
	CourseDataLabelWidth = 320
	CourseDataLabelHeight = 40
	CourseDataLabel = UILabel(0, 0, CourseDataLabelWidth, CourseDataLabelHeight, "Course Files")
	
	CourseDataTowerX = 0
	CourseDataTowerY = VerticalSpacing + CourseDataLabelHeight + CourseDataLabelY
	CourseDataTowerButtonWidth = 320
	CourseDataTowerButtonHeight = 40
	CourseDataTower = UIDataEntryTower(VerticalSpacing, CourseDataTowerButtonWidth, CourseDataTowerButtonHeight, UIFileDialogueButton)
	
	GradesDataLabelX = HorizontalSpacing + CourseDataLabelWidth + CourseDataLabelX
	GradesDataLabelY = 0
	GradesDataLabelWidth = 240
	GradesDataLabelHeight = 40
	GradesDataLabel = UILabel(0, 0, GradesDataLabelWidth, GradesDataLabelHeight, "Grades Files")
	
	GradesDataTowerX = GradesDataLabelX
	GradesDataTowerY = CourseDataTowerY
	GradesDataTowerButtonWidth = 240
	GradesDataTowerButtonHeight = 40
	GradesDataTower = UIDataEntryTower(VerticalSpacing, GradesDataTowerButtonWidth, GradesDataTowerButtonHeight, UIFileDialogueButton)

	def UpdateGraph():
		Visualizer.Graph.CreateGraph(SubjectChangeMenu.CourseDataTower.selectedData, SubjectChangeMenu.GradesDataTower.selectedData)

	ApplyButtonX = HorizontalSpacing + GradesDataLabelWidth + GradesDataLabelX
	ApplyButtonY = 0
	ApplyButtonWidth = 160
	ApplyButtonHeight = 40
	ApplyButton = UIButton(0, 0, ApplyButtonWidth, ApplyButtonHeight, "Apply", onClickEvent = UpdateGraph)

	def Interaction(mousePosition, isMouseDown):
		MousePositionRelativeToCourseDataTower = mousePosition[0] - SubjectChangeMenu.CourseDataTowerX, mousePosition[1] - SubjectChangeMenu.CourseDataTowerY
		SubjectChangeMenu.CourseDataTower.Interaction(MousePositionRelativeToCourseDataTower, isMouseDown)
		MousePositionRelativeToGradesDataTower = mousePosition[0] - SubjectChangeMenu.GradesDataTowerX, mousePosition[1] - SubjectChangeMenu.GradesDataTowerY
		SubjectChangeMenu.GradesDataTower.Interaction(MousePositionRelativeToGradesDataTower, isMouseDown)
		
		MousePositionRelativeToApplyButton = mousePosition[0] - SubjectChangeMenu.ApplyButtonX, mousePosition[1] - SubjectChangeMenu.ApplyButtonY
		SubjectChangeMenu.ApplyButton.Interaction(MousePositionRelativeToApplyButton, isMouseDown)

	def HandleKeyPress(event):
		pass

	def Draw(surface):
		SubjectChangeMenu.CourseDataLabel.Draw(surface.subsurface(SubjectChangeMenu.CourseDataLabelX, SubjectChangeMenu.CourseDataLabelY, SubjectChangeMenu.CourseDataLabelWidth, SubjectChangeMenu.CourseDataLabelWidth))
		SubjectChangeMenu.GradesDataLabel.Draw(surface.subsurface(SubjectChangeMenu.GradesDataLabelX, SubjectChangeMenu.GradesDataLabelY, SubjectChangeMenu.GradesDataLabelWidth, SubjectChangeMenu.GradesDataLabelWidth))
		
		SubjectChangeMenu.CourseDataTower.Draw(surface.subsurface(SubjectChangeMenu.CourseDataTowerX, SubjectChangeMenu.CourseDataTowerY, SubjectChangeMenu.CourseDataTowerButtonWidth, surface.get_size()[1] - SubjectChangeMenu.CourseDataTowerY))
		SubjectChangeMenu.GradesDataTower.Draw(surface.subsurface(SubjectChangeMenu.GradesDataTowerX, SubjectChangeMenu.GradesDataTowerY, SubjectChangeMenu.GradesDataTowerButtonWidth, surface.get_size()[1] - SubjectChangeMenu.GradesDataTowerY))

		SubjectChangeMenu.ApplyButton.Draw(surface.subsurface(SubjectChangeMenu.ApplyButtonX, SubjectChangeMenu.ApplyButtonY, SubjectChangeMenu.ApplyButtonWidth, SubjectChangeMenu.ApplyButtonWidth))