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
        self.term     = terminal if not(is_root) else False

        self.children = []

    def __repr__(self):

        return ''.join([str(item) for sublist in self.grid.map for item in sublist])

    def addChild(self, child):

        self.children.append(child)

    def setIsTerminal(self, terminal):

        self.term = terminal

    def isTerminal(self):

        return self.term

    def getGrid(self):

        return self.grid

    def getCategory(self):

        return self.categ

    def getParent(self):

        return self.parent

    def getChildren(self):

        return self.children

    def getAction(self):

        return self.action

    def getDepth(self):

        return self.depth

class Queue:

    """ Implements a FIFO Data Structure. """

    def __init__(self, first = None):
        
        self.frontier       = deque()
        self.frontier_dict  = dict()
        self.size           = 0

        if first: self.enqueue(first)

    def enqueue(self, node):

        self.frontier.append(node)
        self.frontier_dict[node.__repr__()] = True
        self.size += 1

    def dequeue(self):

        node = self.frontier.popleft()
        del self.frontier_dict[node.__repr__()]       
        self.size -= 1 
  
        return node

    def isEmpty(self):

        return True if self.size == 0 else False

    def membershipChecking(self, node):

        """ Checks if node is in the frontier. """

        return True if node.__repr__() in self.frontier_dict else False





