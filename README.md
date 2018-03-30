# edX Artificial Intelligence Project 1

Project 1 of Artificial Intelligence course on edX by Columbia University. [Link to course.](https://www.edx.org/course/artificial-intelligence-ai-columbiax-csmm-101x-2)

# Introduction

This project solves the [8-puzzle game](http://mypuzzle.org/sliding) using search algorithms, namely, BFS, DFS and A-Star search.

# Instruction

Your job in this assignment is to write driver.py, which solves any 8-puzzle board when given an arbitrary starting configuration. The program will be executed as follows:

```$ python driver.py <method> <board>```

The method argument will be one of the following. You need to implement all three of them:

	1. bfs (Breadth-First Search)
	
	2. dfs (Depth-First Search)
	
	3. ast (A-Star Search)
	

The board argument will be a comma-separated list of integers containing no spaces. For example, to use the bread-first search strategy to solve the input board given by the starting configuration {0,8,7,6,5,4,3,2,1}, the program will be executed like so (with no spaces between commas):

```$ python driver.py bfs 0,8,7,6,5,4,3,2,1```

# Output

When executed, your program will create / write to a file called output.txt, containing the following statistics:

	1. path_to_goal: the sequence of moves taken to reach the goal
	
	2. cost_of_path: the number of moves taken to reach the goal
	
	3. nodes_expanded: the number of nodes that have been expanded
	
	4. search_depth: the depth within the search tree when the goal node is found
	
	5. max_search_depth:  the maximum depth of the search tree in the lifetime of the algorithm
	
	6. running_time: the total running time of the search instance, reported in seconds
	
	7. max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes

# Example Using Breadth-First Search

Suppose the program is executed for breadth-first search as follows:

```$ python driver.py bfs 1,2,5,3,4,0,6,7,8```

Which should lead to the following solution to the input board:

![ImageBFS](https://studio.edx.org/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block@pset1_diagram.png)

The output file will contain exactly the following lines:

1. path_to_goal: ['Up', 'Left', 'Left']
2. cost_of_path: 3
3. nodes_expanded: 10
4. search_depth: 3
5. max_search_depth: 4
6. running_time: 0.00188088
7. max_ram_usage: 0.07812500

# Example Using Depth-First Search

Suppose the program is executed for depth-first search as follows:

```$ python driver.py dfs 1,2,5,3,4,0,6,7,8```

Which should lead to the following solution to the input board:

![ImageDFS](https://studio.edx.org/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block@pset1_diagram.png)

Should output:

1. path_to_goal: ['Up', 'Left', 'Left']
2. cost_of_path: 3
3. nodes_expanded: 181437
4. search_depth: 3
5. max_search_depth: 66125
6. running_time: 5.01608433
7. max_ram_usage: 4.23940217
