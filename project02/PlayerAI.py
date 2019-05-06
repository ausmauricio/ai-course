from random import randint
from BaseAI import BaseAI
from time import clock
from utils import Node
from random import randint
from Grid import Grid
from sys import maxint

#, apply_heuristic, order_terminal_nodes, run_minimax

MAX_DEPTH = 4
MIN_INT = -(maxint - 1)
MAX_INIT = maxint

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

        begin = clock()
        alpha, beta = MIN_INT, MAX_INIT

        root  = grid.clone()
        self.root = Node(True, root, "root")

        node, _ = self.max(self.root, alpha, beta)

        print("CPU Time: ", clock() - begin)

        if node is not None:
            return node.getAction()
        else:
            print("lol")
            moves = grid.getAvailableMoves()
            return moves[randint(0, len(moves) - 1)] if moves else None
        
    def min(self, node, alpha, beta):

        if node.getDepth() >= MAX_DEPTH:
            return node, self.calculate_value(node.grid)

        min_child, min_utility = None, MAX_INIT

        for child in self.get_children(node):
            self.num_nodes+=1

            _, utility = self.max(child, alpha, beta)

            if utility < min_utility:
                min_child, min_utility = child, utility

            if min_utility <= alpha:
                break

            if min_utility < beta:
                beta = min_utility

        return min_child, min_utility

    def max(self, node, alpha, beta):

        if node.getDepth() >= MAX_DEPTH:
            return node, self.calculate_value(node.grid)

        max_child, max_utility = None, MIN_INT

        for child in self.get_children(node):
            self.num_nodes+=1

            _, utility = self.min(child, alpha, beta)

            if utility > max_utility:
                max_child, max_utility = child, utility

            if max_utility >= beta:
                break

            if max_utility > alpha:
                alpha = max_utility

        return max_child, max_utility

    def calculate_value(self, grid):

        """
        Most of the heuristics used to evaluate a grid score were based
        on this epic Stackoverflow answer:

        https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048

        The weights were adjusted manually.
        As a next step, employing machine learning techniques to find out best weights values
        is desirable. In particular, the weight for smoothness hasn't been tested much.

        Also implement smoothness in a loop lol.
        
        Monotonicity (higher values on the corner) should always be the dominant overall, 
        and the other three weights work 'resolving a tie' ""

        """
        
        blank_cells = len(grid.getAvailableCells())

        smoothness = 0

        smoothness += 10 if grid.map[0][0] == grid.map[0][1] else 0 # 1
        smoothness += 10 if grid.map[0][0] == grid.map[1][0] else 0 # 1

        smoothness += 10 if grid.map[0][1] == grid.map[0][2] else 0 # 2
        smoothness += 10 if grid.map[0][1] == grid.map[1][1] else 0 # 2

        smoothness += 10 if grid.map[0][2] == grid.map[0][3] else 0 # 3
        smoothness += 10 if grid.map[0][2] == grid.map[1][2] else 0 # 3

        smoothness += 10 if grid.map[0][3] == grid.map[1][3] else 0 # 4

        smoothness += 10 if grid.map[1][0] == grid.map[1][1] else 0 # 5
        smoothness += 10 if grid.map[1][0] == grid.map[2][0] else 0 # 5

        smoothness += 10 if grid.map[1][1] == grid.map[1][2] else 0 # 6
        smoothness += 10 if grid.map[1][1] == grid.map[2][1] else 0 # 6

        smoothness += 10 if grid.map[1][2] == grid.map[1][3] else 0 # 7
        smoothness += 10 if grid.map[1][2] == grid.map[2][2] else 0 # 7

        smoothness += 10 if grid.map[1][3] == grid.map[2][3] else 0 # 8

        smoothness += 10 if grid.map[2][0] == grid.map[2][1] else 0 # 9
        smoothness += 10 if grid.map[2][0] == grid.map[3][0] else 0 # 9

        smoothness += 10 if grid.map[2][1] == grid.map[2][2] else 0 # 10
        smoothness += 10 if grid.map[2][1] == grid.map[3][1] else 0 # 10

        smoothness += 10 if grid.map[2][2] == grid.map[2][2] else 0 # 11
        smoothness += 10 if grid.map[2][2] == grid.map[3][2] else 0 # 11

        smoothness += 10 if grid.map[2][3] == grid.map[3][3] else 0 # 12

        smoothness += 10 if grid.map[3][0] == grid.map[3][1] else 0 # 13
        smoothness += 10 if grid.map[3][1] == grid.map[3][2] else 0 # 13
        smoothness += 10 if grid.map[3][2] == grid.map[3][3] else 0 # 15

        mask = [[4096,1024,256,64],
                [1024,256,64,16],
                [256,64,16,4],
                [64,16,4,1]]

        monotonicity = 0
        for r in range(3):
            for c in range(3):
                monotonicity += grid.map[r][c] * mask[r][c]        

        bonus = 0
        if grid.getMaxTile() in (grid.map[0][0], grid.map[0][3], grid.map[3][0], grid.map[3][3]):
            bonus=10

        sum = 3*blank_cells + 1*monotonicity + 2*bonus + 1*smoothness
        return sum

    def get_children(self, node):

        category = node.getCategory()
        children = []

        if category in ("player", "root"):

            moves = node.getGrid().getAvailableMoves()
            curr_backup = self.clone(node.getGrid())

            for move in moves:

                curr_backup.move(move)
                children.append(Node(False, curr_backup, "computer", node, move))
                curr_backup = self.clone(node.getGrid())

        elif category == "computer":

            cells = node.getGrid().getAvailableCells()
            curr_backup = self.clone(node.getGrid())

            for cell in cells:

                curr_backup.setCellValue(cell, 2)
                children.append(Node(False, curr_backup, "player", node))
                curr_backup = self.clone(node.getGrid())
                curr_backup.setCellValue(cell,4)
                children.append(Node(False, curr_backup, "player", node))

        return children

    def clone(self, grid):

        #return grid.clone()
        gridCopy = Grid()
        gridCopy.map = [sublist[:] for sublist in grid.map]
        gridCopy.size = grid.size

        return gridCopy
