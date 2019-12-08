#!/usr/bin/env python3

with open('input08.txt', 'rt') as f:
    iimage = f.readline().strip()

width = 25
height = 6

laysize = width * height
layers = len(iimage) // laysize
image = [[] for i in range(layers)]

for lay in range(layers):
    offset = lay * laysize
    for row in range(height):
        lineoff = offset + row * width
        line = iimage[lineoff : lineoff + width]
        image[lay] += [line]

stats = []
best = None
besti = None
for lay in range(layers):
    all = ''.join(image[lay])
    stats += [(all.count('0'), all.count('1'), all.count('2'))]
    # print(lay, stats[lay])
    if not best or stats[lay][0] < best:
        best = stats[lay][0]
        besti = lay

print("Checksum", stats[besti][1] * stats[besti][2])

render = [['2'] * width for i in range(height)]

for lay in image:
    for r in range(height):
        for c in range(width):
            if render[r][c] == '2':
                render[r][c] = lay[r][c]

with open('08.xpm', 'wt') as f:
    f.writelines([
        "! XPM2\n",
        f"{width} {height} 3 1\n",
        "0 c #000000\n",
        "1 c #FFFFFF\n",
        "2 c #00FF00\n"])
    for r in range(height):
        f.write(''.join(render[r]) + '\n')
