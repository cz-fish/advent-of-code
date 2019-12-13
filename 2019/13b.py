#!/usr/bin/env python3

import curses
import intcode
import sys

with open('input13.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]
# insert 2 quarters
program[0] = 2


class Arcade():
    def __init__(self, stdscr, mach):
        self.stdscr = stdscr
        self.mach = mach
        self.outputs = []
        self.init_colors()
        self.ball_x = None
        self.paddle_x = None

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    def print_score(self, score):
        scr = self.stdscr
        size = scr.getmaxyx()
        self.stdscr.move(size[0] - 1, 0)
        self.stdscr.addstr(f'Score {score}')

    def print_tile(self, x, y, tileid):
        scr = self.stdscr
        atr = curses.color_pair(tileid)
        self.stdscr.move(y + 1, x * 2)
        scr.addstr("  ", atr)

    def input_fn(self):
        # auto controls
        self.stdscr.refresh()
        curses.napms(50)
        if self.paddle_x < self.ball_x:
            return 1
        elif self.paddle_x > self.ball_x:
            return -1
        else:
            return 0
        # manual controls
        """
        self.stdscr.move(0,0)
        self.stdscr.addstr('>')
        c = self.stdscr.getch()
        self.stdscr.move(0,0)
        self.stdscr.addstr(' ')
        if c == curses.KEY_LEFT:
            return -1
        elif c == curses.KEY_RIGHT:
            return 1
        elif c == 'q' or c == 27:
            sys.exit(0)
        else:
            return 0
        """

    def output_fn(self, val):
        self.outputs += [val]
        if len(self.outputs) == 3:
            # complete output
            # draw
            x = self.outputs[0]
            y = self.outputs[1]
            if x == -1 and y == 0:
                self.print_score(val)
            else:
                self.print_tile(x, y, val)
            # update game knowledge
            if val == 3:
                self.paddle_x = x
            elif val == 4:
                self.ball_x = x
            # clear
            self.outputs = []

    def loop(self):
        self.mach.run(self.input_fn, self.output_fn)
        self.stdscr.move(0, 0)
        self.stdscr.addstr('Finished')
        self.stdscr.getch()


def main(stdscr):
    mach = intcode.IntCode(program)

    screen = Arcade(stdscr, mach)
    stdscr.clear()
    screen.loop()


curses.wrapper(main)
