# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

from asyncio.windows_events import NULL
import util
from util import heappush, heappop, Stack, Queue, PriorityQueue
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
      """
      Returns the start state for the search problem
      """
      util.raiseNotDefined()

    def isGoalState(self, state):
      """
      state: Search state

      Returns True if and only if the state is a valid goal state
      """
      util.raiseNotDefined()

    def getSuccessors(self, state):
      """
      state: Search state

      For a given state, this should return a list of triples,
      (successor, action, stepCost), where 'successor' is a
      successor to the current state, 'action' is the action
      required to get there, and 'stepCost' is the incremental
      cost of expanding to that successor
      """
      util.raiseNotDefined()

    def getCostOfActions(self, actions):
      """
      actions: A list of actions to take

      This method returns the total cost of a particular sequence of actions.  The sequence must
      be composed of legal moves
      """
      util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):

    # Curtis High - 9/27/2022

    # create a stack of states to search, and a set of visited states
    root = problem.getStartState()
    stateStack = Stack()
    stateStack.push(root)
    visited = {""}
    # create dictionary that maps states in stack to their actions taken
    actionMap = {root:[]}

    while not stateStack.isEmpty():
        state = stateStack.pop()
        actions = actionMap[state]
        # check if popped state is the goal state
        if problem.isGoalState(state):
            return actions
        # otherwise mark as visited and continue
        visited.add(state)

        # iterate over children, add them to stack if not visited
        children = problem.getSuccessors(state)
        for child in children:
            (childState, childAction, childCost) = child
            # update path of actions to get to child
            actionPath = actions.copy()
            actionPath.append(childAction)

            if childState not in visited:
                # push child state to top of stack, and add actions to map
                stateStack.push(childState)
                actionMap[childState] = actionPath

    #print("END - Did not find goal state")
    util.raiseNotDefined()
    

def breadthFirstSearch(problem):

    # Curtis High - 9/27/2022

    # create a queue of states to search, and a set of already reached (as opposed to visited) states
    root = problem.getStartState()
    stateQueue = Queue()
    stateQueue.push(root)
    reached = {root}
    # create dictionary that maps states in queue to their actions taken
    actionMap = {root:[]}

    while not stateQueue.isEmpty():
        state = stateQueue.pop()
        actions = actionMap[state]
        # check if popped state is the goal state
        if problem.isGoalState(state):
            return actions

        # iterate over children, add them to queue if not reached
        children = problem.getSuccessors(state)
        for child in children:
            (childState, childAction, childCost) = child
            # update path of actions to get to child
            actionPath = actions.copy()
            actionPath.append(childAction)

            if childState not in reached:
                # push child state to front of queue, mark as reached, and add actions to map
                stateQueue.push(childState)
                reached.add(childState)
                actionMap[childState] = actionPath

    #print("END - Did not find goal state")
    util.raiseNotDefined()

def uniformCostSearch(problem):

    # Curtis High - 9/27/2022
    
    # create a priority queue of states to search (ordered by cost), and a set of visited states
    root = problem.getStartState()
    stateQueue = PriorityQueue()
    stateQueue.push(root, 0)
    visited = {""}
    # create dictionary that maps states in queue to their actions taken and accumulated cost
    actionCostMap = {root:([],0)}

    while not stateQueue.isEmpty():
        state = stateQueue.pop()
        (actions, cost) = actionCostMap[state]
        # check if popped state is the goal state
        if problem.isGoalState(state):
            return actions
        # otheriwse mark as visited and continue
        visited.add(state)

        # iterate over children, add them to priority queue if not visited
        children = problem.getSuccessors(state)
        for child in children:
            (childState, childAction, childCost) = child
            # update path of actions and cumalitve cost to get to child
            actionPath = actions.copy()
            actionPath.append(childAction)
            childCost += cost

            # if child already visited: do not push or update
            # if child already in priority queue and dictionary: update actions, cost, and priority
            # if child not in priority queue and dictionary: push into both
            if childState not in visited:
                stateQueue.update(childState, childCost)    # update() method handles everything for priority queue
                if childState not in actionCostMap or childCost < actionCostMap[childState][1]:
                    actionCostMap[childState] = (actionPath, childCost)

    #print("END - Did not find goal state")
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    # Curtis High - 9/27/2022
    
    # create a priority queue of states to search (ordered by cost), and a set of visited states
    root = problem.getStartState()
    startHeur = heuristic(problem.getStartState(), problem)
    stateQueue = PriorityQueue()
    stateQueue.push(root, 0+startHeur)
    visited = {""}
    # create dictionary that maps states in queue to their actions taken and accumulated cost
    actionCostMap = {root:([],0)}

    while not stateQueue.isEmpty():
        state = stateQueue.pop()
        (actions, cost) = actionCostMap[state]
        # check if popped state is the goal state
        if problem.isGoalState(state):
            return actions
        # otheriwse mark as visited and continue
        visited.add(state)

        # iterate over children, add them to priority queue if not visited
        children = problem.getSuccessors(state)
        for child in children:
            (childState, childAction, childCost) = child
            # update path of actions, cumalitve cost, and heuristic goal proximity
            actionPath = actions.copy()
            actionPath.append(childAction)
            childCost += cost
            childHeur = heuristic(childState, problem)

            # if child already visited: do not push or update
            # if child already in priority queue and dictionary: update actions, cost, and priority
            # if child not in priority queue and dictionary: push into both
            if childState not in visited:
                stateQueue.update(childState, childCost+childHeur)  # update() method handles everything for priority queue
                if childState not in actionCostMap or childCost < actionCostMap[childState][1]:
                    actionCostMap[childState] = (actionPath, childCost)

    #print("END - Did not find goal state")
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
