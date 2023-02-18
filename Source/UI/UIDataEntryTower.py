# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

from .UIButton import UIButton

class UIDataEntryTower(object):
    def RemoveRow(self, button):
        for row in self.listOfRows:
            if row[1] == button:
                self.listOfRows.remove(row)

    def ClearRow(self, button):
        self.RemoveRow(button)
        if self.extendable == False:
            self.AddRow()

    def AddRow(self):
        DataEntryButton = self.dataEntryObject(0, 0, self.buttonWidth - self.buttonHeight, self.buttonHeight, "Enter Data")
        RemoveRowButton = UIButton(0, 0, self.buttonHeight, self.buttonHeight, "X", onClickEvent = UIDataEntryTower.ClearRow, onClickEventArgs = (self,DataEntryButton), centered = True)
        self.listOfRows.append((RemoveRowButton, DataEntryButton))

    def __init__(self, spacing, buttonWidth, buttonHeight, dataEntryObject, extendable = True):
        self.spacing = spacing
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight
        self.dataEntryObject = dataEntryObject
        self.listOfRows = []
        self.selectedData = None
        self.extendable = extendable
        if extendable:
            self.addRowButton = UIButton(0, 0, buttonWidth, buttonHeight, "Add Row", onClickEvent = self.AddRow)

    def MarkButtonAsHighlighted(self, button):
        for row in self.listOfRows:
            row[1].highlighted = False
        button.highlighted = True


    def Interaction(self, mousePosition, isMouseDown):
        yPosition = 0
        for row in self.listOfRows[::]:
            button = row[0]
            button.Interaction((mousePosition[0], mousePosition[1] - yPosition), isMouseDown)
            yPosition += button.rect.height + self.spacing
        yPosition = 0
        for row in self.listOfRows:
            button = row[1]
            button.Interaction((mousePosition[0], mousePosition[1] - yPosition), isMouseDown)
            yPosition += button.rect.height + self.spacing
            if button.clickedEvent:
                self.selectedData = button.data
                self.MarkButtonAsHighlighted(button)
        if self.extendable:
            self.addRowButton.Interaction((mousePosition[0], mousePosition[1] - yPosition), isMouseDown)
                

    def Draw(self, surface):
        if surface.get_size()[0] < self.buttonWidth:
            raise Exception("surface too small for widest button")
        yPosition = 0
        for row in self.listOfRows:
            button = row[0]
            button.Draw(surface.subsurface(0, yPosition, self.buttonHeight, self.buttonHeight))
            button = row[1]
            button.Draw(surface.subsurface(self.buttonHeight, yPosition, self.buttonWidth - self.buttonHeight, self.buttonHeight))
            yPosition += button.rect.height + self.spacing

        if self.extendable:
            self.addRowButton.Draw(surface.subsurface(0, yPosition, self.buttonWidth, self.buttonHeight))