from graphics import GraphWin, Point, Rectangle
from mazes import MazeLocation


class MazeRect:
    UNIT_SIZE = 25
    GRID_COLORS = ({'empty': 'white',
                    'start': 'green',
                    'goal': 'red',
                    'obstacle': 'black',
                    'frontier': 'cyan',
                    'explored': 'blue',
                    'current': 'navy',
                    'path': 'orange'})
    EDGE_COLOR = 'gray'
    EDGE_WEIGHT = 0.5
    CURRENT_OUTLINE = 'orange'
    CURRENT_WEIGHT = 4

    def __init__(self, location: MazeLocation, type=None) -> None:
        self._location = location
        self.type = type
        self._min_bound = Point(self._location.column * MazeRect.UNIT_SIZE,
                                self._location.row * MazeRect.UNIT_SIZE)
        self._max_bound = Point((self._location.column + 1) * MazeRect.UNIT_SIZE,
                                (self._location.row + 1) * MazeRect.UNIT_SIZE)
        self.rect = Rectangle(self._min_bound, self._max_bound)
        self.rect.setOutline(MazeRect.EDGE_COLOR)
        self.set_type(type)

    def set_type(self, type):
        self.rect.setFill(MazeRect.GRID_COLORS[type])
        if type == 'current':
            self.rect.setWidth(MazeRect.CURRENT_WEIGHT)
            self.rect.setOutline(MazeRect.CURRENT_OUTLINE)
        else:
            self.rect.setWidth(MazeRect.EDGE_WEIGHT)
            self.rect.setOutline(MazeRect.EDGE_COLOR)


class MazeWin:
    def __init__(self, maze):
        self.maze = maze
        self._rows = self.maze.upper_limit.row # - self.maze.lower_limit.row
        self._columns = self.maze.upper_limit.column# - self.maze.lower_limit.column
        self._width = self._columns * MazeRect.UNIT_SIZE
        self._height = self._rows * MazeRect.UNIT_SIZE
        self._window = GraphWin("Maze", self._width, self._height, autoflush=False)
        self.locations = dict()

        for r in range(self._rows):
            for c in range(self._columns):
                loc = MazeLocation(r, c)
                if loc == self.maze.start:
                    loc_type = 'start'
                elif loc == self.maze.goal:
                    loc_type = 'goal'
                elif loc in self.maze.obstacles:
                    loc_type = 'obstacle'
                else:
                    loc_type = 'empty'
                # offset maze location based off of minimum bounds
                # loc = MazeLocation(r - self.maze.lower_limit.row, c - self.maze.lower_limit.column)
                self.locations[loc] = MazeRect(loc, loc_type)

        self.draw_background()

    def draw_background(self):
        for loc in self.locations:
            self.locations[loc].rect.draw(self._window)
        self._window.update()

    def update_location(self, location, new_type):
        if location not in self.locations:
            self.locations[location] = MazeRect(location, new_type)
        elif location not in [self.maze.start, self.maze.goal]:
            self.locations[location].set_type(new_type)

    def show_search(self, current_state, frontier, explored=None):
        self.update_location(current_state, 'current')
        self.update_location(explored, 'explored')
        for location in frontier.list():
            self.update_location(location.state, 'frontier')

        self._window.update()
        self.update_location(current_state, 'explored')

    def show_path(self, node):
        if not node:
            return
        while node.parent:
            self.locations[node.state].set_type('path')
            node = node.parent
            self._window.update()


    def exit_on_click(self):
        self._window.getMouse()
        self._window.close()




