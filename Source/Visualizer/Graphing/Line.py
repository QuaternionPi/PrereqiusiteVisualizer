# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
from ...Commons import VisualBase
from ...Color import Colors

# Lines are the connections drawn between rectangles on the screen
class Line(VisualBase):
    def __init__(self, parent, points):
        super().__init__(parent)
        self.rootPoints = points # The list of points that are in the route of the line
        self.points = points[::]
        self.width = 2
        
        self.colorBase = parent.sourceNode.visual.dependantColor
        self.colorDulled = Colors["DarkGrey"]

    def UpdatePoints(self):
        for i in range(len(self.points)):
            self.points[i] = (self.rootPoints[i][0] + self.offsetX, self.rootPoints[i][1] + self.offsetY)

    def AddArrowhead(self):
        root = self.points[-1]
        Corner1 = (root[0] + 4, root[1] - 8)
        Corner2 = (root[0],     root[1] - 5)
        Corner3 = (root[0] - 4, root[1] - 8)
        self.points += [Corner1, Corner2, Corner3, root]
        self.rootPoints += [Corner1, Corner2, Corner3, root]
        
    def UpdateColor(self):
        if self.dulled:
            self.color = self.colorDulled
        else:
            self.color = self.colorBase

    # Draws the line to surface
    def Draw(self, surface):
        current = self.points[0]
        for next in self.points[1:]:
            pygame.draw.line(surface, self.color, current, next, self.width)
            current = next




