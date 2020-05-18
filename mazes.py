from typing import NamedTuple, List, Tuple, Optional
from enum import Enum
from math import sqrt
from generic_search import astar, node_to_path


# constants to use to display the cells in ASCII
class Cell(str, Enum):
    EMPTY = ' '
    START = 'S'
    GOAL = 'E'
    BLOCKED = '*'
    PATH = '~'


# named tuple for maze locations
class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, data_string: Optional[str] = None,
                 start: Optional[MazeLocation] = None,
                 goal: Optional[MazeLocation] = None,
                 obstacles: Optional[List[MazeLocation]] = None) -> None:
        self._data_string: Optional[str] = data_string
        if self._data_string is not None:
            self._data_builder()
        else:
            if not start or not goal:
                raise Exception('Error: Tried to initialize maze without start'
                                'and/or goal!')
            self.start: Optional[MazeLocation] = start
            self.goal: Optional[MazeLocation] = goal
            self.obstacles: Optional[List[MazeLocation]] = obstacles
            self._set_limits()

    def successors(self, start: MazeLocation,
                   ignore_obstacles: Optional[bool] = False) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        # hard coded possible knight moves (8)
        possible_moves: List[Tuple] = \
            [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for m in possible_moves:
            new_location: MazeLocation = MazeLocation(start.row + m[0],
                                                      start.column + m[1])
            if new_location in self.obstacles and not ignore_obstacles:
                continue
            elif not self._is_in_limits(new_location, pad=3):
                continue
            else:
                locations.append(new_location)

        return locations

    def successors_no_obst(self, start):
        return self.successors(start, ignore_obstacles=True)

    def knight_distance(self):
        def distance(ml: MazeLocation) -> int:
            xdist: int = abs(ml.column - self.goal.column)
            ydist: int = abs(ml.row - self.goal.row)
            if xdist == ydist and xdist < 3:
                return 4
            elif xdist == 0 or ydist == 0:
                if xdist + ydist == 1:
                    return 3
                elif xdist + ydist == 2:
                    return 2
                elif xdist + ydist == 3:
                    return 5
                elif xdist + ydist == 4:
                    return 2
                else:
                    # approximate
                    return (xdist + ydist) // 2
            elif xdist == 2 and yddist == 1 or xdist == 1 and ydist == 2:
                return 1
            else:
                # approximatee
                return (xdist + ydist) // 2

        return distance

    def knight_distance_recursive(self):
        # TODO: Write better heuristic for knights movement
        #   This one isn't very good, and takes a long time.
        def distance(ml: MazeLocation) -> int:
            d = self.euclidian_distance()
            sol: Node[T] = astar(ml, self.goal_test,
                                 self.successors_no_obst, d)
            path: List[T] = node_to_path(sol)
            return len(path)

        return distance

    def euclidian_distance(self):
        def distance(ml: MazeLocation) -> float:
            xdist: int = ml.column - self.goal.column
            ydist: int = ml.row - self.goal.row
            return sqrt(xdist ** 2 + ydist ** 2)

        return distance

    def goal_test(self, location: MazeLocation):
        return location == self.goal

    def _is_in_limits(self, location: MazeLocation, pad: int = 0) -> bool:
        row: int = location.row
        column: int = location.column
        if row > self.upper_limit.row + pad or \
                row < self.lower_limit.row - pad or \
                column > self.upper_limit.column + pad or \
                column < self.lower_limit.column - pad:
            return False
        return True

    def _set_limits(self) -> None:
        rmin, rmax = sorted([self.start.row, self.goal.row])
        cmin, cmax = sorted([self.start.column, self.goal.column])
        if self.obstacles:
            for o in self.obstacles:
                rmin = min(rmin, o.row)
                rmax = max(rmax, o.row)
                cmin = min(cmin, o.column)
                cmax = max(cmax, o.column)

        self.upper_limit = MazeLocation(rmax + 1, cmax + 1)
        self.lower_limit = MazeLocation(rmin, cmin)

    def _data_builder(self) -> None:
        """ Convert a stringsize.column representation of a chessboard to a maze """
        self.obstacles: List[MazeLocation] = []
        rows: List[str] = self._data_string.split('\n')

        for x, r in enumerate(rows):
            for y, c in enumerate(r):
                if c == Cell.START:
                    self.start: MazeLocation = MazeLocation(x, y)
                elif c == Cell.GOAL:
                    self.goal: MazeLocation = MazeLocation(x, y)
                elif c == Cell.BLOCKED:
                    self.obstacles.append(MazeLocation(x, y))

        if not self.start or not self.goal:
            raise Exception('Data Builder Error: Start and/or Goal are missing')
        self._set_limits()

    @property
    def limits(self):
        return self.lower_limit, self.upper_limit

    def __str__(self) -> str:
        board_str = ''
        for r in range(self.size.row):
            for c in range(self.size.column):
                position = MazeLocation(r, c)
                if position == self.start:
                    board_str += ''.join(Cell.START.value)
                elif position == self.goal:
                    board_str += ''.join(Cell.GOAL.value)
                elif position in self.obstacles:
                    board_str += ''.join(Cell.BLOCKED.value)
                else:
                    board_str += ''.join(Cell.EMPTY.value)
            board_str += '\n'
        return board_str
