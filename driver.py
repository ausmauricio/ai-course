#!/usr/bin/env python

import sys
import resource
from timeit import default_timer as timer
from collections import deque
from heapq import heappop, heappush

# define some constants
 
actions_dict = {0:['D','R'],
                1:['D','L','R'],
                2:['D','L'],
                3:['U','D','R'],
                4:['U','D','L','R'],
                5:['U','D','L'],
                6:['U','R'],
                7:['U','L','R'],
                8:['U','L']}

swap_dict  = {"U":-3,"D":3,"L":-1,"R":1}
move_dict  = {"U": 'Up',"D": 'Down',"L": 'Left',"R": 'Right'}
goal_state = ['0','1','2','3','4','5','6','7','8']

pos_dict = {0:(0,0), 1:(1,0), 2:(2,0), 
            3:(0,1), 4:(1,1), 5:(2,1), 
            6:(0,2), 7:(1,2), 8:(2,2)}

class Node:

    """ A standard node class. """

    def __init__(self, state, parent = None, action = None, depth = 0):

        self.state  = state
        self.parent = parent
        self.action = action
        self.depth  = depth

    def __repr__(self):

        return ''.join(self.state)

    def get_state(self):

        return self.state

    def get_parent(self):

        return self.parent

    def get_action(self):

        return self.action

    def get_depth(self):

        return self.depth

class ASTNode(Node):

    """ Extends Node class with attributes for AST Search. """

    def __init__(self, state, parent = None, action = None, depth = 0):

        Node.__init__(self, state, parent, action, depth)
        
        self.distance = self.calculate_distance()

    def calculate_distance(self):

        """ Calculates the Manhattan distance to the goal. """     

        distance = 0

        for i in xrange(9):
            
            pos = pos_dict[int(self.state[i])]
            distance += (abs(pos[0]-pos_dict[i][0]) + abs(pos[1]-pos_dict[i][1]))        
        
        return distance

    def get_distance(self):

        return self.distance

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

    def is_empty(self):

        return True if self.size == 0 else False

    def membership_checking(self, node):

        """ Checks if node is in the frontier. """

        return True if node.__repr__() in self.frontier_dict else False

class Stack:

    """ Implements a LIFO Data Structure. """

    def __init__(self, first = None):
        
        self.frontier       = list()
        self.frontier_dict  = dict()
        self.size           = 0

        if first: self.push(first)

    def push(self, node):

        self.frontier.append(node)
        self.frontier_dict[node.__repr__()] = True
        self.size += 1

    def pop(self):

        node = self.frontier.pop()
        del self.frontier_dict[node.__repr__()]       
        self.size -= 1 
  
        return node

    def is_empty(self):

        return True if self.size == 0 else False

    def membership_checking(self, node):

        """ Checks if node is in the frontier. """

        return True if node.__repr__() in self.frontier_dict else False

class Heap:

    """ Implements a Priority Queue. """

    def __init__(self, first = None):
        
        self.frontier       = []
        self.frontier_dict  = dict()
        self.size           = 0

        if first: self.push(first, first.get_distance())

    def push(self, node, priority):

        heappush(self.frontier, (priority, node))  
        self.frontier_dict[node.__repr__()] = True
        self.size += 1

    def pop(self):

        node = heappop(self.frontier)[1]
        del self.frontier_dict[node.__repr__()]       
        self.size -= 1 
  
        return node

    def decrease_key(self, node, priority):

        """ Decrease key implementation. """

        # messy but it works

        old_priority = 10000000

        i = 0

        for tup in self.frontier:
            
            if tup[1].__repr__() == node.__repr__():

                old_priority = tup[0]
                break     

            i+=1     
        
        #assert(self.frontier[i][1].__repr__() == node.__repr__())

        if old_priority < priority: 
        
            pass
        
        else: 

            del self.frontier[i]

            heappush(self.frontier, (priority, node))  

    def is_empty(self):

        return True if self.size == 0 else False

    def membership_checking(self, node):

        """ Checks if node is in the frontier. """

        return True if node.__repr__() in self.frontier_dict else False

class Game:    

    """ Defines the Game class. """

    def __init__(self, initial_state, mode):

        self.nodes_expanded   = 0
        self.max_search_depth = 0

        self.solved     = False
        self.mode       = mode
        self.explored   = {}

        if self.mode == "bfs":
 
            self.solver = self.bfs_solver
            self.root   = Node(initial_state)

        elif self.mode == "dfs": 

            self.solver = self.dfs_solver
            self.root   = Node(initial_state)

        else:
            
            self.solver = self.ast_solver
            self.root   = ASTNode(initial_state)

    def add_explored(self, node):

        self.explored[node.__repr__()] = True

    def was_explored(self, node):

        return True if node.__repr__() in self.explored else False

    def goal_reached(self):

        return True if cmp(self.curr_state.get_state(), goal_state) == 0 else False

    def get_children(self):

        children = []

        zero_pos = self.curr_state.get_state().index("0")
            
        for action in actions_dict[zero_pos]:

            # state only
            # to be the child
            child  = self.curr_state.get_state()[:] 
            offset = zero_pos + swap_dict[action] 
            child[zero_pos], child[offset] = child[offset], child[zero_pos]

            is_ast = True if self.mode == "ast" else False

            if is_ast:
            
                children.append(ASTNode(child, self.curr_state, action, 
                                        self.curr_state.get_depth() + 1))

            else:

                children.append(Node(child, self.curr_state, action, 
                                     self.curr_state.get_depth() + 1))
            
        self.nodes_expanded += 1	
        
        return children

    def bfs_solver(self):

        frontier = Queue(self.root)

        while not(frontier.is_empty()):

            self.curr_state = frontier.dequeue()
            self.add_explored(self.curr_state)

            if self.goal_reached(): 
                self.solved = True
                return self.curr_state

            for node in self.get_children():
                if not(frontier.membership_checking(node)) and not(self.was_explored(node)):
                    frontier.enqueue(node)
                    if self.max_search_depth < node.get_depth(): self.max_search_depth = node.get_depth()

    def dfs_solver(self):  

        frontier = Stack(self.root)

        while not(frontier.is_empty()):

            self.curr_state = frontier.pop()
            self.add_explored(self.curr_state)

            if self.goal_reached(): 
                self.solved = True
                return self.curr_state

            for node in self.get_children()[::-1]:
                if not(frontier.membership_checking(node)) and not(self.was_explored(node)):
                    frontier.push(node)   
                    if self.max_search_depth < node.get_depth(): self.max_search_depth = node.get_depth()

    def ast_solver(self):

        frontier = Heap(self.root)

        while not(frontier.is_empty()):

            self.curr_state = frontier.pop()
            self.add_explored(self.curr_state)

            if self.goal_reached(): 
                self.solved = True
                return self.curr_state

            for node in self.get_children():

                if not(frontier.membership_checking(node)) and not(self.was_explored(node)):

                    frontier.push(node, node.get_distance() + node.get_depth())
                    if self.max_search_depth < node.get_depth(): self.max_search_depth = node.get_depth()

                elif frontier.membership_checking(node):

                    frontier.decrease_key(node, node.get_distance() + node.get_depth())
                    if self.max_search_depth < node.get_depth(): self.max_search_depth = node.get_depth()

    def write_output(self, rtime, rusage):

        assert(self.solved == True)

        node   = self.curr_state
        action = []

        # get path to goal. start from goal to root.

        while(node.get_state() != self.root.get_state()):
            
            action.append(move_dict[node.get_action()])
            node = node.get_parent()   

        self.path_to_goal = action[::-1]            
        
        output = open("output.txt","w") 

        output.write("path_to_goal: "     + str(self.path_to_goal) + "\n")
        output.write("cost_of_path: "     + str(len(self.path_to_goal)) + "\n")
        output.write("nodes_expanded: "   + str(self.nodes_expanded) + "\n")
        output.write("search_depth: "     + str(len(self.path_to_goal)) + "\n")
        output.write("max_search_depth: " + str(self.max_search_depth) + "\n")
        output.write("running_time: "     + str(rtime) + "\n")
        output.write("max_ram_usage: "    + str(rusage/(1048576.0)) + "\n")

	# 1048576 is to convert bytes to Mbytes

        output.close()

if __name__ == "__main__": 

    initial_state = list(sys.argv[2].replace(",",""))
    
    game = Game(initial_state, sys.argv[1])
    
    start = timer()

    game.solver()

    end = timer()  

    running_time = end - start  

    ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    game.write_output(running_time, ram_usage)
