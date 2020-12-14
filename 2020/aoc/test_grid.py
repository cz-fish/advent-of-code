from aoc import Grid

TEST_GRID_RECT = [
    "#####",
    "#..##",
    "##..#",
    "#####"
]

TEST_GRID_IRREG = [
    " #####",
    "#....##",
    " ##.##",
    "  ###"
]


def test_grid_construction():
    gr = Grid(TEST_GRID_RECT)
    assert(gr.w == 5)
    assert(gr.h == 4)
    assert(gr.min_width == 5)
    assert(gr.max_width == 5)


def test_grid_construction_irregular():
    gr = Grid(TEST_GRID_IRREG, rectangular=False)
    assert(gr.h == 4)
    assert(gr.w == 7)
    assert(gr.min_width == 5)
    assert(gr.max_width == 7)


def test_get():
    gr = Grid(TEST_GRID_IRREG, rectangular=False)
    assert(gr.get(0, 0) == ' ')
    assert(gr.get(2, 1) == '#')
    assert(gr.get(1, 3) == '.')


def test_get_wrap():
    gr = Grid(TEST_GRID_IRREG, rectangular=False)
    assert(gr.get_wrap(0, 0) == ' ')
    assert(gr.get_wrap(0, -1) == '#')
    assert(gr.get_wrap(5, 2) == '.')
    assert(gr.get_wrap(-2, 3) == '.')


def test_is_in():
    gr = Grid(TEST_GRID_IRREG, rectangular=False)
    assert(gr.is_in(0, 0) == True)
    assert(gr.is_in(1, 6) == True)
    assert(gr.is_in(1, 7) == False)
    assert(gr.is_in(2, 6) == False)
    assert(gr.is_in(4, 0) == False)


def test_neighbors_4():
    gr = Grid(TEST_GRID_IRREG, rectangular=False)
    n = sorted(gr.neighbors4(2, 5))
    assert(n == [(1, 5), (2, 4)])


def test_neighbors_4_wrapped():
    gr = Grid(TEST_GRID_RECT)
    n = sorted(gr.neighbors4(0, 3, wrap=True))
    assert(n == [(0, 2), (0, 4), (1, 3), (3, 3)])


def test_neighbors_4_outside():
    gr = Grid(TEST_GRID_IRREG, rectangular=False)
    n = sorted(gr.neighbors4(2, 5, outside=True))
    assert(n == [(1, 5), (2, 4), (2, 6), (3, 5)])


def test_neighbors_8():
    gr = Grid(TEST_GRID_IRREG, rectangular=False)
    n = sorted(gr.neighbors8(0, 5))
    assert(n == [(0, 4), (1, 4), (1, 5), (1, 6)])

# TODO: test grid copy
