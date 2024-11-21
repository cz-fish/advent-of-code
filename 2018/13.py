#!/usr/bin/python3.8

from pyaoc import Env, Grid

e = Env(13, raw_lines=True)
e.T(r"""/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """, "7,3", None)

e.T(r"""/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""", None, "6,4")


def find_carts(grid):
    carts = []
    symb = '<^>v'
    repl = '-|-|'
    for y in range(grid.h):
        for x in range(grid.w):
            if not grid.is_in(y, x):
                continue
            v = grid.get(y, x)
            if v in symb:
                # Remove the cart from the grid
                facing = symb.index(v)
                grid.grid[y][x] = repl[facing]
                carts.append({'row': y, 'col': x, 'facing': facing, 'turns': 0})
    return carts


def sort_carts(carts):
    carts.sort(key=lambda c: (c['row'], c['col']))


def move_one_cart(cart, grid):
    x = cart['col']
    y = cart['row']
    # Facing: L,U,R,D
    nextpos = {
        0: (y, x-1),
        1: (y-1, x),
        2: (y, x+1),
        3: (y+1, x)
    }[cart['facing']]
    tile = grid.get(nextpos[0], nextpos[1])
    if tile == '/':
        # turn
        cart['facing'] = 3 - cart['facing']
        """
        ^ the above formula more explicitly explained:
        cart['facing'] = {
            0: 3 # L -> D
            1: 2 # U -> R
            2: 1 # R -> U
            3: 0 # D -> L
        }[cart['facing']]
        """
    elif tile == '\\':
        # turn
        cart['facing'] = cart['facing'] ^ 1
        """
        ^ the above formula more explicitly explained:
        cart['facing'] = {
            0: 1 # L -> U
            1: 0 # U -> L
            2: 3 # R -> D
            3: 2 # D -> R
        }[cart['facing']]
        """
    elif tile == '+':
        # maybe turn
        whichturn = cart['turns'] % 3 # left=0, straight=1, right=2
        cart['turns'] += 1
        if whichturn == 0:
            # turn left (counter-clockwise)
            cart['facing'] = (cart['facing'] - 1) % 4
        elif whichturn == 2:
            # turn right (clockwise)
            cart['facing'] = (cart['facing'] + 1) % 4
    # else no turn
    return nextpos


def move_carts(carts, grid):
    crash = None
    # collect all currently occupied positions
    occupied = set([(c['row'], c['col']) for c in carts])
    #print(occupied)
    # move each cart in turn
    for cart in carts:
        newpos = move_one_cart(cart, grid)
        if newpos in occupied:
            # Collision
            return newpos
        # Old position is no longer occupied
        occupied.remove((cart['row'], cart['col']))
        occupied.add(newpos)
        cart['row'] = newpos[0]
        cart['col'] = newpos[1]
    # If we got here, there was no crash
    return None


def part1(input):
    g = Grid(input.get_valid_lines(), rectangular=False)
    carts = find_carts(g)
    counter = 0
    while True:
        sort_carts(carts)
        #print(carts)
        crash = move_carts(carts, g)
        if crash:
            break
        counter += 1
        if counter % 10000 == 0:
            print(f"No crash after {counter} loops")
    return f"{crash[1]},{crash[0]}"


e.run_tests(1, part1)
e.run_main(1, part1)


def move_and_crash_carts(carts, grid):
    crashed = set()
    # collect all currently occupied positions
    occupied = set([(c['row'], c['col']) for c in carts])
    # move each cart in turn
    for cart in carts:
        oldpos = (cart['row'], cart['col'])
        if oldpos in crashed:
            continue
        newpos = move_one_cart(cart, grid)
        if newpos in occupied:
            crashed.add(newpos)
        # Old position is no longer occupied
        occupied.remove((cart['row'], cart['col']))
        occupied.add(newpos)
        cart['row'] = newpos[0]
        cart['col'] = newpos[1]
    # If we got here, all carts have moved or crashed
    return crashed


def part2(input):
    g = Grid(input.get_valid_lines(), rectangular=False)
    carts = find_carts(g)
    counter = 0
    while True:
        sort_carts(carts)
        crashed = move_and_crash_carts(carts, g)
        carts = [cart for cart in carts if (cart['row'], cart['col']) not in crashed]
        if len(carts) == 0:
            assert False, "No carts left!"
        elif len(carts) == 1:
            break
        counter += 1
        if counter % 10000 == 0:
            print(f"Still {len(carts)} carts after {counter} loops")
    return f"{carts[0]['col']},{carts[0]['row']}"


e.run_tests(2, part2)
e.run_main(2, part2)
