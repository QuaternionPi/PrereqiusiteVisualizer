# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

from ...Commons import*
from .OptionMap import OptionMap
from .SFUGrades import*

# Nodes are the main logical element in a graph, the conain information
class Node(LogicalBase):
    recursionLimit = 2
    def __init__(self, name, title, parent, grade, prerequisites = [[]], concurrencies = []):
        Value = GradeToValue[grade]
        if Value > 0:
            status = "Complete"
        else:
            status = "Unavaliable"
        self.grade = grade
        super().__init__(name, parent, status)
        self.title = title
        self.listOfRequisiteNodes = [] # All nodes that can be required for this node
        self.listOfRequisiteEdges = [] # All edges that target this node

        self.listOfDependantNodes = [] # All nodes depend on this node
        self.listOfDependantEdges = [] # All edges that source at this node

        self.concurrentCourses = concurrencies
        self.corequisiteBlock = [self]

        # An 'option' is a set of requirments to take a course, some courses have multiple options
        self.optionNodes = [] # Requisite nodes, sorted by option
        self.optionEdges = [] # Requisite edges, sorted by option
        self.optionGrades = [] # The grade required for every requisite node, sorted by option
        self.optionNames = prerequisites # The names of requisite courses, sorted by option
        self.option = 0 # The currently displayed option

        self.optionMap = [] # A map of every posible prerequisite path, to the recursion limit
        self.optionMapPosition = 0 # Index in that map

        self.prerequisites = [] # The names of all prerequisites

        for i in prerequisites: # lays out neccesary lists within lists
            self.prerequisites += i
            self.optionNodes.append([])
            self.optionGrades.append([])
            self.optionEdges.append([])

        self.prerequisites = list(dict.fromkeys(self.prerequisites)) # Removes duplocates from self.prerequisites

    # Removes references to all other objects
    def ForgetConnections(self):
        self.listOfRequisiteEdges = []

        self.listOfDependantNodes = []
        self.listOfDependantEdges = []
        
        self.corequisiteBlock = [self]
        
        self.optionNodes = [[]] 
        self.optionGrades = [[]]
        self.optionEdges = [[]]
        self.option = 0

        self.optionMap = []
        self.optionMapPosition = 0 

        if self.visual:
            self.visual = False


    # Turns list of concurrencies into either prerequisites or corequisites
    def HandleConcurrencies(self):
        for name in self.concurrentCourses:
            Concurrency = name.upper()
            if self.name in self.nodes[Concurrency].concurrentCourses: # If the concurrency is mutual
                # Combine both nodes corequisiteBlock into one, shared list
                self.corequisiteBlock += self.nodes[Concurrency].corequisiteBlock
                self.corequisiteBlock = list(dict.fromkeys(self.corequisiteBlock))
                self.nodes[Concurrency].corequisiteBlock = self.corequisiteBlock
            else:
                # Add the concurrency as a prerequisite
                for option in self.optionNames:
                    option.append(Concurrency + "<D>")
                self.prerequisites.append(Concurrency + "<D>")

    # Finds this nodes requisite nodes and set up their relationship
    def AdjacentNodes(self):
        for name in self.prerequisites:
            Prerequisite = name.upper()
            Type, Tags = HandleRequirment(Prerequisite)
            if Type == "Course":
                Name = Tags[0].upper()
                node = self.nodes[Name]
                self.listOfRequisiteNodes.append(node)
                node.listOfDependantNodes.append(self)
                
    # Computes the depth of this node in the graph
    def CalculateMinDepth(self):
        #print(self.name)
        MaxDepth = 0
        for node in self.corequisiteBlock:
            if node.depth == 0:
                for requisite in node.listOfRequisiteNodes:
                    node.depth = max(node.depth, requisite.CalculateMinDepth() + 1)
            MaxDepth = max(node.depth, MaxDepth)
        for node in self.corequisiteBlock:
            node.depth = MaxDepth
        return self.depth

    def CalculateMaxDepth(self):
        if len(self.listOfDependantNodes) > 0:
            MinDepth = 1000000
            for node in self.corequisiteBlock:
                for dependant in node.listOfDependantNodes:
                    MinDepth = min(dependant.CalculateMaxDepth() - 1, MinDepth)
            for node in self.corequisiteBlock:
                node.depth = MinDepth
        return self.depth



    # Finds every edge coming into or from this node
    def AdjacentEdges(self):
        for node in self.listOfRequisiteNodes:
            EdgeName = JoinName(node.name, self.name)
            edge = self.edges[EdgeName]
            self.listOfRequisiteEdges.append(edge)

        for node in self.listOfDependantNodes:
            EdgeName = JoinName(self.name, node.name)
            edge = self.edges[EdgeName]
            self.listOfDependantEdges.append(edge)

    # Finds adjecent nodes and edges by option
    def AdjacentOptions(self):
        for node in self.listOfRequisiteNodes:
            for nodes, names, grades in zip(self.optionNodes, self.optionNames, self.optionGrades):
                for requirment in names:
                    Type, Tags = HandleRequirment(requirment)
                    if Type == "Course":
                        Name = Tags[0]
                        Grade = Tags[1]
                        if Name == node.name:
                            nodes.append(node)
                            grades.append(Grade)
                    elif Type == "NumberOfCredits":
                        pass
                    elif Type == "Special":
                        pass

        for edge in self.listOfRequisiteEdges:
            for edges, names in zip(self.optionEdges, self.optionNames):
                for requirment in names:
                    Type, Tags = HandleRequirment(requirment)
                    if Type == "Course":
                        Name = Tags[0]
                        if edge.sourceNode.name == Name:
                            edges.append(edge)
                            edges = list(dict.fromkeys(edges))
                    elif Type == "NumberOfCredits":
                        pass
                    elif Type == "Special":
                        pass

    def DependantMaxLength(self):
        length = 0
        for edge in self.listOfDependantEdges:
            length = max(edge.Length(), length)
        return length

    def HasConnections(self):
        return len(self.listOfRequisiteNodes) > 0 or len(self.listOfDependantNodes) > 0 or len(self.corequisiteBlock) > 1

    # Creates a map of every posible prerequisite path within recursive limits
    def MapOptions(self):
        self.optionMap = OptionMap(self, self.recursionLimit)

    # Determines if this node should be marked as avaliable
    def UpdateStatus(self):
        if self.status == "Unavaliable":
            for nodes, grades in zip(self.optionNodes, self.optionGrades):
                Valid = True
                for node, grade in zip(nodes, grades):
                    if GradeToValue[node.grade] < GradeToValue[grade]:
                        Valid = False
                        break
                if Valid:
                    self.status = "Avaliable"
                    break

    def ShowCorequisites(self):
        for node in self.corequisiteBlock:
            self.parent.Show(node.visual, 2)

    # Marks all requisite nodes as greyed out within recursive limits
    def ShowRequisites(self, level):
        if level > 0:
            for edge in self.listOfRequisiteEdges:
                edge.sourceNode.ShowRequisites(level-1)
                edge.visual.dulled = True
                self.parent.Show(edge.visual, 1)
        self.visual.dulled = True
        self.parent.Show(self.visual, 2)
    
    # Marks all requisites in one option as fully shown within recursive limits
    def ShowOption(self, level):
        if level > 0:
            for edge in self.optionEdges[self.option]:
                edge.sourceNode.ShowOption(level-1)
                edge.visual.dulled = False
                self.parent.Show(edge.visual, 1)
        self.visual.dulled = False
        self.parent.Show(self.visual, 2)

    # Marks all dependant nodes as fully shown within recursive limits
    def ShowDependants(self, level):
        if level > 0:
            for edge in self.listOfDependantEdges:
                edge.targetNode.ShowDependants(level-1)
                edge.visual.dulled = False
                self.parent.Show(edge.visual, 1)
        self.visual.dulled = False
        self.parent.Show(self.visual, 2)

    #***
    # Sets the option of nodes to construct a valid prerequisite path
    def SetRequisiteOptions(self):
        if len(self.optionMap) > 0:
            for vertex in self.optionMap[self.optionMapPosition]:
                vertex.node.option = vertex.index
        self.optionMapPosition += 1
        if self.optionMapPosition == len(self.optionMap):
            self.optionMapPosition = 0


    # What to do if clicked on
    def Clicked(self):        
        self.SetRequisiteOptions()
        self.ShowCorequisites()
        self.ShowDependants(self.recursionLimit)
        self.ShowRequisites(self.recursionLimit)
        self.ShowOption(self.recursionLimit)