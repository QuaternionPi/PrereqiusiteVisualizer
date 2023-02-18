# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

def CombinePaths(list1, list2):
    Output = []
    for path1 in list1:
        for path2 in list2:
            NewPath = path1[::]
            NewPathNodes = []
            for vertex in NewPath:
                NewPathNodes.append(vertex.node)
            i = 1
            while i < len(path2) and path2[i].node not in NewPathNodes:
                NewPath.append(path2[i])
                i += 1
            Output.append(NewPath)
    return [Output]

class Vertex():
    def __init__(self, node, index):
        self.node = node
        self.index = index

class OptionMap():
    def __init__(self, node, depth):
        self.listOfPaths = []
        self.CreatePaths(node, [], depth)
        self.WeavePaths() 
        self.CleanPaths()
        
    def CreatePaths(self, rootNode, path, level):
        HasDecendantPaths = False
        if level > 0:
            for option in range(len(rootNode.optionNodes)):
                ExtendedPath = path + [Vertex(rootNode, option)]
                OptionNodes = rootNode.optionNodes[option]
                for node in OptionNodes:
                    HasDecendantPaths = True
                    self.CreatePaths(node, ExtendedPath[::], level-1)
        if HasDecendantPaths == False:
            self.listOfPaths.append(path)

    def WeavePaths(self):
        PathsByOption = [[]]
        for path in self.listOfPaths:
            if len(path) > 0:
                while path[0].index >= len(PathsByOption):
                    PathsByOption.append([])
                PathsByOption[path[0].index].append(path)

        self.listOfPaths = []

        for setOfPaths in PathsByOption:
            PathsByNextNode = [[]]
            if len(setOfPaths) > 0:
                if len(setOfPaths[0]) > 1:
                    ListOfNodes = [setOfPaths[0][1].node]
                    Index = 0
                    for path in setOfPaths:
                        if len(path) > 1:
                            if path[1].node in ListOfNodes:
                                Index = ListOfNodes.index(path[1].node)
                            else:
                                ListOfNodes.append(path[1].node)
                                PathsByNextNode.append([])
                                Index = -1

                        PathsByNextNode[Index].append(path)

                elif len(setOfPaths[0]) > 0:
                    self.listOfPaths += setOfPaths

            while len(PathsByNextNode) > 1:
                PathsByNextNode[0:2] = CombinePaths(PathsByNextNode[0], PathsByNextNode[1])
                    
            self.listOfPaths += PathsByNextNode[0]

    def CleanPaths(self):
        List = []
        for path in self.listOfPaths:
            if path not in List:
                List.append(path)
        self.listOfPaths = List

    def __getitem__(self, i):
        return self.listOfPaths[i]

    def __len__(self):
        return len(self.listOfPaths)