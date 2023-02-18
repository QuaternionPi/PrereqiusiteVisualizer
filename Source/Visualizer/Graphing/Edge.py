# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

from ...Commons import *

# Edges are logical connectives in a graph, they represent the relationships between nodes
class Edge(LogicalBase):
    def __init__(self, name, parent, status, sourceNode, targetNode):
        super().__init__(name, parent, status)
        self.sourceNode = sourceNode # where this edge starts
        self.targetNode = targetNode # where this edge ends
        

    def ForgetConnections(self):
        self.sourceNode = False
        self.targetNode = False
    # Distance between the target node and the soource node
    def Length(self):
        return self.targetNode.depth - self.sourceNode.depth
    
