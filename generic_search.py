from __future__ import annotations
from typing import Generic, TypeVar, List, Optional, Deque, Callable, Set, Dict
from heapq import heappop, heappush
# from maze_graphics import MazeWin


T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def list(self):
        return self._container

    def __repr__(self):
        return repr(self._container)


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container
        # returns true if container is empty

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def list(self):
        return self._container

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def list(self):
        return self._container

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0,
                 heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:  # used for A* search
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial: T, goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]],
        graphics: Optional[MazeWin] = None) -> Optional[Node[T]]:
    # The line below is literally the only line that's different from bfs:
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored is where we have been
    explored: Set[T] = {initial}

    steps_considered = 0
    # keep going while we can still explore
    while not frontier.empty:
        steps_considered += 1
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # see if we're there yet
        if goal_test(current_state):
            print(f'BFS reached goal after consideration of {steps_considered} possible moves.')
            return current_node

        # see where we can go next
        # but haven't already been
        child = None
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
        if graphics:
            graphics.show_search(current_state, frontier, child)

    print(f'BFS failed to reach goal after consideration of {steps_considered} possible moves.')
    return None  # if all options exhausted


def bfs(initial: T, goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]],
        graphics: Optional[MazeWin] = None) -> Optional[Node[T]]:
    # The line below is literally the only line that's different from dfs:
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we have been
    explored: Set[T] = {initial}

    steps_considered = 0
    # keep going while we can still explore
    while not frontier.empty:
        steps_considered += 1
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # see if we're there yet
        if goal_test(current_state):
            return current_node

        # see where we can go next
        # but haven't already been
        child = None
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
        if graphics:
            graphics.show_search(current_state, frontier, child)

    print(f'BFS failed to reach goal after consideration of {steps_considered} possible moves.')
    return None  # if all options exhausted


def astar(initial: T, goal_test: Callable[[T], bool],
          successors: Callable[[T], List[T]], heuristic: Callable[[T], float],
          graphics: Optional[MazeWin] = None) -> Optional[Node[T]]:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    explored: Dict[T, float] = {initial: 0.0}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        if goal_test(current_state):
            return current_node

        child = None
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
        if graphics:
            graphics.show_search(current_state, frontier, child)

    return None


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path
