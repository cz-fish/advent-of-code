from typing import List, Tuple


class Grid:
    """A two-dimentional grid of characters.
       Use `.w` for width, `.h` for height, `.max_width`, `.min_width`
       for min/max width if the grid is not rectangular.
       Use `.grid` to access the grid, or the `get()` method.
    """

    def __init__(self, lines: List[str], rectangular=True):
        """Initialize the grid from a list of text lines - one
           character per cell.
           If `rectangular` is True, then each row is required
           to have the same width."""
        self.grid = []
        max_width = 0
        min_width = None
        for ln in lines:
            self.grid += [list(ln)]
            max_width = max(max_width, len(ln))
            if min_width is None:
                min_width = len(ln)
            else:
                min_width = min(min_width, len(ln))
        if rectangular:
            # Check that all lines are of the same size
            assert(max_width == min_width)
        self.max_width = max_width
        self.min_width = min_width
        self.w = max_width
        self.h = len(self.grid)

    def get(self, row:int, col:int) -> any:
        """Get value at the given coords"""
        return self.grid[row][col]

    def get_wrap(self, row:int, col:int) -> any:
        """Get value at the given coords, but wrap around if the
           coords are not in range."""
        r = row % self.h
        return self.grid[r][col % len(self.grid[r])]

    def is_in(self, row:int, col:int) -> bool:
        """Return True if given coordinates are in the grid, False
           if they're not"""
        if row < 0 or row >= self.h:
            return False
        if col < 0 or col >= len(self.grid[row]):
            return False
        return True

    def _neighborCoords(self, row:int, col:int, wrap:bool, outside:bool, dirs) -> List[Tuple[int, int]]:
        coords = []
        for dr, dc in dirs:
            nr = row + dr
            nc = col + dc
            if self.is_in(nr, nc):
                coords += [(nr, nc)]
            elif wrap:
                nr = nr % self.h
                nc = nc % len(self.grid[nr])
                assert(self.is_in(nr, nc))
                coords += [(nr, nc)]
            elif outside:
                coords += [(nr, nc)]
        return coords

    def neighbors4(self, row:int, col:int, wrap=False, outside=False) -> List[Tuple[int]]:
        """Get list of coordinate tuples of up to 4 neighbors of the given cell.
           The neighbors are only horizontal or vertical, not diagonal.
           If any of the neighbor coordinates is outside the grid then:
             * if `wrap`==False, `outside`==False -> the coordinate is discarded
             * if `wrap`==True -> the coordinate is wrapped around
             * if `wrap`==False, `outside`==True -> the coordinate is returned,
               even though it is outside the grid"""
        return self._neighborCoords(row, col, wrap, outside,
            [(-1, 0), (0, -1), (0, 1), (1, 0)])

    def neighbors8(self, row:int, col:int, wrap=False, outside=False) -> List[Tuple[int]]:
        """Get list of coordinate tuples of up to 8 neighbors of the given cell.
           The neighbors are horizontal, vertical, and diagonal.
           If any of the neighbor coordinates is outside the grid then:
             * if `wrap`==False, `outside`==False -> the coordinate is discarded
             * if `wrap`==True -> the coordinate is wrapped around
             * if `wrap`==False, `outside`==True -> the coordinate is returned,
               even though it is outside the grid"""
        return self._neighborCoords(row, col, wrap, outside,
            [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

