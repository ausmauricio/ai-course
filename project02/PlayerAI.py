from random import randint
from BaseAI import BaseAI
from time import clock
from utils import Node, Queue
from random import randint
from Grid import Grid

#, apply_heuristic, order_terminal_nodes, run_minimax

class PlayerAI(BaseAI):

    """
        Implements Player AI.

        This AI uses the minimax algorithm with alpha-beta pruning,
        so it is able to return a move within 0.2 seconds (CPU time)

        In using minimax we have to determine two things:
        first, how we evaluate the terminal nodes values.
        second, how we order them to get larger tree chops,
        using alpha beta pruning.

    """

    def getMove(self, grid):

	# mixing up naming conventions

        begin = clock()
        root  = grid.clone()

        self.explored  = {}
        self.root      = Node(True, root, "root")
        self.max_depth = self.root.getDepth()
        self.terminals = []
        self.expired   = False

        frontier = Queue(self.root)

        while not(frontier.isEmpty()) and not(self.expired):

            self.curr_node = frontier.dequeue()
            self.addExplored(self.curr_node)

            for node in self.getChildren(self.curr_node.getCategory()):

                self.curr_node.setIsTerminal(False)

                if not(frontier.membershipChecking(node)) and not(self.wasExplored(node)):
                    frontier.enqueue(node)
                    if self.max_depth < node.getDepth(): self.max_depth = node.getDepth()

            if(clock() - begin > 0.14): self.expired = True

        while not(frontier.isEmpty()):

            node = frontier.dequeue()
            if node.getDepth() == self.max_depth and node.isTerminal():
                self.terminals.append(node)

        #print("explored")
        #print(self.explored)
        #print("terminals")
        #print(self.terminals)
        print("max depth")
        print(self.max_depth)
        print("CPU Time")
        print(clock() - begin)
        print("len terminals")
        print(len(self.terminals))

        if len(self.terminals):
            max_value   = 0
            action_node = None

            for terminal in self.terminals:
                #print(terminal)
                value = self.calculate_value(terminal.__repr__())
                if value > max_value:
                    action_node = terminal
                    max_value   = value

            node = action_node

            while(node.getParent().__repr__() != self.root.__repr__()):
                    node = node.getParent()

            print("CPU Time")
            print(clock() - begin)

            return node.getAction()

        else:

            moves = grid.getAvailableMoves()

            print("CPU Time")
            print(clock() - begin)

            return moves[randint(0, len(moves) - 1)] if moves else None

    def calculate_value(self, string):

        summ = 0
        max_seen_value = 0
        for s in string:

            if s == "0": summ+=8
            elif int(s) > max_seen_value:
                summ+=4*max_seen_value
            else:        summ+=(int(s))

        return summ

    def addExplored(self, node):

        self.explored[node.__repr__()] = True

    def wasExplored(self, node):

        return True if node.__repr__() in self.explored else False

    def getChildren(self, category):

         children = []
         #print(self.curr_node.getDepth())

         if category in ("player", "root"):

            moves = self.curr_node.getGrid().getAvailableMoves()
            curr_backup = self.clone(self.curr_node.getGrid())

            for move in moves:

                curr_backup.move(move)
                #print("new move")
                #print(curr_backup.map)
                children.append(Node(False, curr_backup, "computer", self.curr_node, move))
                curr_backup = self.clone(self.curr_node.getGrid())

         elif category == "computer":

             cells = self.curr_node.getGrid().getAvailableCells()
             curr_backup = self.clone(self.curr_node.getGrid())

             for cell in cells:

                 curr_backup.setCellValue(cell, 2 if randint(1,10)%2 else 4)
                 #print("new tile")
                 #print(curr_backup.map)
                 children.append(Node(False, curr_backup, "player", self.curr_node))
                 curr_backup = self.clone(self.curr_node.getGrid())

         return children

    def clone(self, grid):

        #return grid.clone()
        gridCopy = Grid()
        gridCopy.map = [sublist[:] for sublist in grid.map]
        gridCopy.size = grid.size

        return gridCopy