from collections import deque

class Node:

    """ A standard node class. """

    def __init__(self, is_root, grid, category, parent = None, action = None, terminal = True):

        self.root     = is_root
        self.grid     = grid
        self.categ    = category
        self.parent   = parent
        self.action   = action

        self.depth    = 0 if is_root else parent.getDepth() + 1

    def __repr__(self):

        return ''.join([str(item) for sublist in self.grid.map for item in sublist])

    def getGrid(self):

        return self.grid

    def getCategory(self):

        return self.categ

    def getParent(self):

        return self.parent

    def getAction(self):

        return self.action

    def getDepth(self):

        return self.depth





