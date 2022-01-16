#!/usr/bin/python3.8

import pygame


SERIAL_NUM = 3031
#SERIAL_NUM = 18

def get_cell_power(x, y, serial_num):
    rack_id = x + 10
    power_level = (rack_id * y + serial_num) * rack_id
    power_digit = (power_level % 1000) // 100
    return power_digit - 5


def get_all_cell_powers(serial_num):
    all_powers = []
    for y in range(1, 301):
        all_powers.append([])
        for x in range(1, 301):
            all_powers[-1].append(get_cell_power(x, y, serial_num))
    return all_powers


def find_best_of_size(all_powers, size):
    hei = len(all_powers)
    wid = len(all_powers[0])
    best = None
    best_coord = None
    columns = [
        sum(all_powers[y][x] for y in range(size))
        for x in range(wid)
    ]
    for y in range(hei - size + 1):
        value = sum(columns[0:size])
        for x in range(0, wid - size + 1):
            if best is None or value > best:
                best = value
                best_coord = (x, y)
            if x < wid - size:
                value = value - columns[x] + columns[x+size]
        if y < hei - size:
            for x in range(wid):
                columns[x] = columns[x] - all_powers[y][x] + all_powers[y+size][x]
    return best_coord, best


def solve(serial_num):
    all_powers = get_all_cell_powers(serial_num)
    progress = []
    overall_best = None
    best_pos = None
    # Go backwards from large squares to small ones
    for size in range(300, 0, -1):
    # Go from small squares to large ones
    #for size in range(1, 301):
        best_coord, best = find_best_of_size(all_powers, size)
        if overall_best is None or best > overall_best:
            overall_best = best
            best_pos = (size, best_coord)
        progress.append((size, best, best_coord, overall_best, best_pos))
    return all_powers, progress


print("Solving...")
all_powers, progress = solve(SERIAL_NUM)
print("Done")

# --- visualization ---

EDGE_SIZE=3
OFFSET=30

pygame.init()
pygame.display.init()

WIN_SIZE = (300 * EDGE_SIZE + 2 * OFFSET, 300 * EDGE_SIZE + 2 * OFFSET + 100)
screen = pygame.display.set_mode(WIN_SIZE)

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

def paint_all_powers(all_powers):
    surface = pygame.Surface(WIN_SIZE)
    hei = len(all_powers)
    wid = len(all_powers[0])
    for y in range(hei):
        for x in range(wid):
            val = all_powers[y][x] + 6
            shade = pygame.Color(5 * val, 24 * val, 5 * val)
            pygame.draw.rect(surface, shade, pygame.Rect(OFFSET + x * EDGE_SIZE, OFFSET + y * EDGE_SIZE, EDGE_SIZE, EDGE_SIZE))
    return surface

def paint_best(size, this, this_pos, overall_best, best_pos):
    global screen
    other = pygame.Surface(WIN_SIZE)
    other.set_alpha(128)

    def put(pos, size, color):
        left = OFFSET + pos[0] * EDGE_SIZE
        top = OFFSET + pos[1] * EDGE_SIZE
        wid = EDGE_SIZE * size
        pygame.draw.rect(other, color, pygame.Rect(left, top, wid, wid), 0)

    if this != overall_best:
        put(this_pos, size, (255, 255, 255))
    put(best_pos[1], best_pos[0], (255, 0, 0))

    screen.blit(other, (0,0))
    text = font.render(f'Size {size}, power {this} {this_pos}. Best size {best_pos[0]}, power {overall_best} {best_pos[1]}', False, (255, 255, 255))
    screen.blit(text, (OFFSET, 2 * OFFSET + 300 * EDGE_SIZE))


TIME_DELAY_MS = 100

screen.fill((0,0,0))
power_surf = paint_all_powers(all_powers)
screen.blit(power_surf, (0,0))
text = font.render("Press Enter to start", False, (255, 255, 255))
screen.blit(text, (OFFSET, 2 * OFFSET + 300 * EDGE_SIZE))
pygame.display.flip()

running = True
started = False
pos = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if not started:
                    # Start animation
                    pygame.time.set_timer(pygame.USEREVENT + 1, TIME_DELAY_MS)
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, {}))
                    started = True
        elif event.type == pygame.USEREVENT + 1:
            pos += 1
            if pos >= len(progress):
                # Done - disable timer
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                started = False
                pos = 0
            else:
                # Move to the next size (next frame)
                size, this, this_pos, overall_best, best_pos = progress[pos]
                screen.fill((0,0,0))
                screen.blit(power_surf, (0,0))
                paint_best(size, this, this_pos, overall_best, best_pos)
                pygame.display.flip()

