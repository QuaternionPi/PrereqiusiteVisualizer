# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute


# Translates course requirment stings into useful data
def HandleRequirment(text):
    Requirment = text.upper()
    FirstTerm = Requirment.split("<")[0]
    tags = []
    for tag in Requirment.split("<"):
        tags.append(tag[:-1])
    if FirstTerm == "SPECIAL":
        return "Special", tags
    elif FirstTerm[0].isdigit():
        return "NumberOfCredits", [FirstTerm] + tags
    else:
        return "Course", [FirstTerm] + tags[1:]
    
JoinNameCharater = ":"
# Edges and Lines use joined names in the form Source:Target
# Joins two names together
def JoinName(source, target):
    return source + JoinNameCharater + target
# Determines if a name is a joined name
def IsJoinName(name):
    return JoinNameCharater in name
# Returns the source name of the joined name
def JoinNameSource(name):
    return name.split(JoinNameCharater)[0]
# Returns the target name of the joined name
def JoinNameTarget(name):
    return name.split(JoinNameCharater)[1]
    
# The base for nodes and edges
class LogicalBase(object):
    def __init__(self, name, parent, status):
        self.name = name
        self.parent = parent # The parent hierarchical graph
        self.nodes = parent.nodes # Dictionary of all nodes in the graph
        self.edges = parent.edges # Dictionary of all edges in the graph
        self.depth = 0 # The depth of the node in the graph, is calculated later
        self.status = status # The status of the node, determines the color scheme
        self.visual = False # The decendent visual object, either a card or a line

# The base for cards and lines
class VisualBase(object):
    offsetX = 0
    offsetY = 0
    def __init__(self, parent):
        self.name = parent.name # The name of the parent logical object
        self.parent = parent # The parent logical object
        self.color = (0, 0, 0)
        self.dulled = False
