# Written by David Wiebe
# This copy is for demonstraition purposes only
# Do Not Redistribute

class SpaceAllocation1D():
    def __init__(self):
        self.allocations = []
    def Allocate(self, space):
        self.allocations.append(space)
    def __contains__(self, space):
        for allocation in self.allocations:
            Part1 = space[0] <= allocation[0] <= space[1]
            Part2 = space[0] <= allocation[1] <= space[1]
            Part3 = allocation[0] <= space[0] <= allocation[1]
            Part4 = allocation[0] <= space[1] <= allocation[1]
            if Part1 or Part2 or Part3 or Part4:
                return True
        return False
