# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

import pygame
import json
from time import time
from ...Commons import *
from .SpaceAllocation import SpaceAllocation1D
from .Node import Node
from .Edge import Edge
from .Card import Card
from .Line import Line

class HierarchicalGraph(object):
    def __init__ (self):
        self.layers = [] # An array containing every node, sorted by depth
        self.nodes = {} # Every node in the graph
        self.edges = {} # Every edge in the graph
        self.showables = [[],[],[]] # Controls the Z-order of drawn objects
        self.interactables = [] # Every interactable card currently shown

        self.clickedEvent = False
        self.clickedCard = False

        self.cellWidth = 90 # The width of every cell
        self.cellHeight = 50 # The height of every cell
        self.intraLayerGap = 20 # The gap between cells of the same layer
        self.extraLayerGap = 90 # The gap between different layers of cells
        
        self.surfaceSize = (0, 0) # The size of the drawable surface
        self.internalBorder = 15 # How far the user can scroll beyond the nearest edge of the furthest card
        VisualBase.offsetX = self.internalBorder
        VisualBase.offsetY = self.internalBorder

        self.width = 0
        self.height = 0
        self.lastTime = time() # Used in DeltaTime calculations

    # Removes references to every other object
    def ForgetConnections(self):
        self.layers = [[]]
        self.showables = [[],[],[]]
        self.interactables = []
        for node in self.nodes.values():
            node.ForgetConnections()
            del node
        self.nodes = {}
        for edge in self.edges.values():
            edge.ForgetConnections()
            del edge
        self.edges = {}

    # Makes it so no objects are shown
    def ClearShowables(self):
        self.showables = [[],[],[]]
        self.interactables = []

    # Shows one visual object, if it is a card then it becomes interactable
    def Show(self, visual, layer = 0):
        self.showables[layer].append(visual)
        if type(visual) == Card:
            self.interactables.append(visual)

    # Shows every card
    def ShowAllCards(self):
        for node in self.nodes.values():
            self.Show(node.visual, 2)

    # Hides all visuals and resets their color
    def HideAll(self):
        self.ClearShowables()
        for node in self.nodes.values():
            node.visual.dulled = False
            node.visual.UpdateColor()

    # Resets the graph to it's default presentation
    def Reset(self):
        self.HideAll()
        self.ShowAllCards()

    # Only shows cards who's name contains specific text
    def SearchText(self, text):
        self.HideAll()
        for node in self.nodes.values():
            if text in node.name or text.lower() in node.title.lower():
                self.Show(node.visual,2)

    # Creates a graph from json files
    def CreateGraph(self, CoursesPath, GradesPath):
        # Catches invalid inputs
        if CoursesPath == '' or type(CoursesPath) is None or GradesPath == '' or type(GradesPath) is None:
            return False

        # If this graph previously contained data, it is removed
        self.ForgetConnections()

        # Imports json data. This should have some exeption handling attached
        Courses = open(CoursesPath,"r")
        JsonOfCourses = json.loads(Courses.read())
        Courses.close()

        Grades = open(GradesPath,"r")
        JsonOfGrades = json.loads(Grades.read())
        Grades.close()

        # Extracts data from json files and adds it to the graph
        for course in JsonOfCourses:
            if(course == ".data"): # Skip reading .data
                continue
            Grade = "F"
            if course in JsonOfGrades:
                Grade = JsonOfGrades[course]["grade"]
            Name = course.upper()
            Title = JsonOfCourses[course]["title"]
            Prerequisites = JsonOfCourses[course]["prerequisites"]
            Corequisites = JsonOfCourses[course]["corequisites"]
            self.nodes[Name] = Node(Name, Title, self, Grade, Prerequisites, Corequisites)

        self.CreateLogical()
        self.CreateCards()
        self.CreateLines()
        return True

    # Creates edges between nodes
    def CreateEdges(self):
        for node in list(self.nodes.values()):
            for dependant in node.listOfDependantNodes:
                Name = JoinName(node.name, dependant.name)
                self.edges[Name] = Edge(Name, self, node.status, node, dependant)
                
    # Assigns nodes to a layer based on their depth
    # Position in the layer depends on the prerequisite block
    def Assignlayers(self):
        MaxDepth = 0
        for node in self.nodes.values():
            MaxDepth = max(MaxDepth, node.depth)

        for i in range(MaxDepth):
            self.layers.append([])

        for node in self.nodes.values():
            self.layers[node.depth].append(node)

        # Assigns the nodes in the largest corequisiteBlocks to be the first ones drawn
        for layer in self.layers:
            i = 1
            while i < len(layer):
                j = i
                while j > 0 and len(layer[j - 1].corequisiteBlock) < len(layer[j].corequisiteBlock):
                    layer[j-1],layer[j] = layer[j],layer[j-1]
                    j -= 1
                i += 1

    # Creates the logical elements of the graph; nodes and edges
    def CreateLogical(self):
        # Determines if courses are mutualy concurrent
        for node in self.nodes.values():
            node.HandleConcurrencies()
        # Finds each nodes relative nodes, e.i. requisites and dependants
        for node in self.nodes.values():
            node.AdjacentNodes()
        # If a node has no depenants or requisites it is removed
        for name in list(self.nodes.keys()):
            if self.nodes[name].HasConnections() == False:
                del self.nodes[name]

        # Calculates the closest each node can be to depth 0
        for node in self.nodes.values():
            node.CalculateMinDepth()
        # Calculates the furthest each node can be from depth 0 unless it has no dependants
        for node in self.nodes.values():
            node.CalculateMaxDepth()

        self.CreateEdges()

        # Finds each edge going into or out of a node
        for node in self.nodes.values():
            node.AdjacentEdges()
        # Finds the edges and nodes going into a node by option
        for node in self.nodes.values():
            node.AdjacentOptions()
            
        self.Assignlayers()
        
        # Creates the sets of courses that will be displayed when clicked
        for node in self.nodes.values():
            node.MapOptions()
        # Updates the status of courses; i.e. checking to see if a course should be avaliable
        for node in self.nodes.values():
            node.UpdateStatus()
           
    # Creates cards and places them, while leaving space for lines to be draw between them.
    def CreateCards(self):
        NumberOfPathsEnteringEachLayer = [] # Counts the number of paths that enter each layer

        AllocatedSpaces = [] # SpaceAllocations mark occupied spaces and prevent object placement
        for layer in self.layers:
            AllocatedSpaces.append(SpaceAllocation1D())
            NumberOfPathsEnteringEachLayer.append(0)

        xPosition = 0
        yPosition = 0
        CurrentLevel = 0
        # Creats cards
        for layer in self.layers:
            # Finds every corequisite block. Note some corequisite blocks are shared between nodes
            CorequisiteBlocks = []
            for node in layer:
                if node.corequisiteBlock not in CorequisiteBlocks:
                    CorequisiteBlocks.append(node.corequisiteBlock)

            for block in CorequisiteBlocks:
                AllocatedSpace = AllocatedSpaces[CurrentLevel]

                HitAllocatedSpace = True
                while HitAllocatedSpace:
                    Left = xPosition + self.intraLayerGap/2 
                    Right = xPosition - 1 + self.cellWidth*len(block) 
                    SpaceToBeAssigned = (Left, Right)# The space needed to display the corequisite block
                    HitAllocatedSpace = SpaceToBeAssigned in AllocatedSpace
                    if HitAllocatedSpace:
                        # Move the x position over by half the distance between cells, center on center
                        xPosition += (self.cellWidth + self.intraLayerGap)/2
                    else:
                        AllocatedSpace.Allocate(SpaceToBeAssigned)

                for node in block:
                    # Creates a card (the visual object representing the node)
                    node.visual = Card(node, xPosition, yPosition, self.cellWidth, self.cellHeight)
                    
                    xPosition += self.cellWidth
                    # Updates the width of the graph
                    self.width = max(self.width, xPosition) 

                    # Allocates space for lines that source from node
                    for level in range(CurrentLevel + 1, CurrentLevel + node.DependantMaxLength()):
                        Left = node.visual.rect.midtop[0] - self.intraLayerGap/2
                        Right = node.visual.rect.midtop[0] + self.intraLayerGap/2
                        AllocatedSpaces[level].Allocate((Left, Right))
                xPosition = 0
                
            yPosition += self.cellHeight
            # Updates the height of the graph
            self.height = max(self.height, yPosition)
            yPosition += self.extraLayerGap
            CurrentLevel += 1
            
        for node in self.nodes.values():
            node.visual.UpdateRect()
            
    # Creates lines between cards in the graph
    def CreateLines(self):
        for layer in self.layers:
            RequisiteCards = []# All cards that have lines targeting node in this layer
            for node in layer:
                for requisite in node.listOfRequisiteNodes:
                    card = requisite.visual
                    if card not in RequisiteCards:
                        RequisiteCards.append(card)
            
            # Sorts cards by their x position
            i = 1
            while i < len(RequisiteCards):
                j = i
                while j > 0 and RequisiteCards[j-1].rect.x > RequisiteCards[j].rect.x:
                    RequisiteCards[j-1], RequisiteCards[j] = RequisiteCards[j], RequisiteCards[j-1]
                    j -= 1
                i += 1

            # 
            for node in layer:
                for edge in node.listOfRequisiteEdges:
                    Source = edge.sourceNode.visual.connection # Source location of the line
                    Target = edge.targetNode.visual.connection # Target location of the line
                
                    VerticalIndex = 0
                    for card in RequisiteCards:
                        if card == edge.sourceNode.visual:
                            break
                        VerticalIndex += 1
                
                    NumberOfEdgesEntering = len(RequisiteCards)
                    RelativeVertialPosition = ((VerticalIndex + 1) / (NumberOfEdgesEntering + 2) - 1)
                    VerticalPosition = Target[1] + self.extraLayerGap*RelativeVertialPosition

                    RequisiteEdges = edge.targetNode.listOfRequisiteEdges
                    if len(RequisiteEdges) != 1:
                        HorizontalIndex = 0
                        for card in RequisiteCards:
                            if card == edge.sourceNode.visual:
                                break
                            if card.parent in node.listOfRequisiteNodes:
                                HorizontalIndex += 1
                        RelativeHorizontalPosition = HorizontalIndex / (len(RequisiteEdges) - 1)
                        EnteranceRange = edge.targetNode.visual.rect.width/2.5
                        Target = Target[0] + (RelativeHorizontalPosition - 0.5) * EnteranceRange, Target[1]

                    mid2 = (Target[0], VerticalPosition)
                    mid1 = (Source[0], VerticalPosition)

                    edge.visual = Line(edge, [Source, mid1, mid2, Target])
                    edge.visual.AddArrowhead()

        for edge in self.edges.values():
            edge.visual.UpdatePoints()

    # Moves the location of the visual objects of the graph
    def Move(self, deltaX, deltaY):
        MadeChange = False
        if deltaX > 0:
            VisualBase.offsetX = min(VisualBase.offsetX + deltaX, self.internalBorder)
            MadeChange = True
        elif deltaX < 0:
            VisualBase.offsetX = max(VisualBase.offsetX + deltaX, min(0, self.surfaceSize[0] - self.width - self.internalBorder))
            MadeChange = True

        if deltaY > 0:
            VisualBase.offsetY = min(VisualBase.offsetY + deltaY, self.internalBorder)
            MadeChange = True
        elif deltaY < 0:
            VisualBase.offsetY = max(VisualBase.offsetY + deltaY, min(0, self.surfaceSize[1] - self.height - self.internalBorder))
            MadeChange = True

        return MadeChange
            
    
    def Interaction(self, mousePosition, isMouseDown):
        Now = time()
        DeltaTime = float(Now - self.lastTime)
        self.lastTime = Now

        ScaleFactor = 500
        DeltaAmmount = ScaleFactor * DeltaTime
        DeltaX = 0
        DeltaY = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            DeltaX = DeltaAmmount
        if keys[pygame.K_RIGHT]:
            DeltaX = -DeltaAmmount
        if keys[pygame.K_UP]:
            DeltaY = DeltaAmmount
        if keys[pygame.K_DOWN]:
            DeltaY = -DeltaAmmount

        for node in self.nodes.values():
            node.visual.UpdateColor()
        for edge in self.edges.values():
            edge.visual.UpdateColor()

        UpdatePositions = self.Move(DeltaX, DeltaY)
        if UpdatePositions:
            for node in self.nodes.values():
                node.visual.UpdateRect()
        if UpdatePositions:
            for edge in self.edges.values():
                edge.visual.UpdatePoints()

        self.clickedEvent = False
        for card in self.interactables:
            card.Interaction(mousePosition, isMouseDown)
            if card.clickedEvent:
                self.clickedEvent = True
                self.clickedCard = card
                self.ClearShowables()
                card.parent.Clicked()
                
            
    def Draw(self, surface):
        surface.fill((40,40,50))
        ShowEverything = False # This is a debug option, should always be false unless debuging
        if ShowEverything:
            for edge in self.edges.values():
                edge.visual.Draw(surface)
            for node in self.nodes.values():
                node.visual.Draw(surface)

        else:
            for level in self.showables:
                for visual in level:
                    visual.Draw(surface)
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, *surface.get_size()), 3)
            self.surfaceSize = surface.get_size()

        
