# edX Artificial Intelligence Project 2

Project 2 of Artificial Intelligence course on edX by Columbia University. [Link to course.](https://www.edx.org/course/artificial-intelligence-ai-columbiax-csmm-101x-2)

# Introduction

This is an implementation of an agent capable of 'winning' [the 2048-puzzle game](http://gabrielecirulli.github.io/2048) using advanced techniques to probe the search space of the game. It is based on an adversarial search algorithm that plays the game intelligently, perhaps much more so than playing by hand.

# Instruction

To see the game in action you should run:

```$ python2 GameManager.py```

# Strategy

The agent PlayerAI.py implements a strategy based on:

1. The minimax algorithm. 
2. Alpha-beta pruning. This should speed up the search process by eliminating irrelevant branches. 
3. Heuristic functions. To be able to cut off your search at any point, you must employ heuristic functions to allow you to assign approximate values to nodes in the tree. 
4. Heuristic weights, since it uses more than one heuristic function. 




