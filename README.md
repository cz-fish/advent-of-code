# Advent of Code

[Pages](https://cz-fish.github.io/advent-of-code/)

Solutions for AoC are in respective directories, by year. Python utility library is called `pyaoc`. To use it, create Python virtual environment, and install the library and its requirements into it.

```sh
python3.12 -m venv dev
source dev/bin/activate
pip install -e pyaoc/
```

If any year's solutions have additional dependencies, those might be in their respective `requirements.txt` files

```sh
pip install -r 2023/requirements.txt
```

Import required modules from the pyaoc library

```py
from pyaoc import Env, Grid #...
```

Generate boilerplate file for a new day with

```sh
newday     # for current day
newday 11  # create day 11 regardless of current date
```

## 2024
* **25** - locks and keys
* **24** - addition from logical ops
* **23** - LAN party clique
* **22** - pseudorandom numbers
* **21** - robot remote controls
* **20** - circuit race with cheating
* **19** - arranging towels
* **18** - shortest path with falling obstacles
* **17** - computer producing a quine
* **16** - paths in maze with fewest turns
* **15** - pushing boxes Sokoban style
* **14** - robots moving in lines, forming a Christmas tree
* **13** - clamp machines, vector addition
* **12** - calculating fence
* **11** - blinking at stones
* **10** - find hiking trails
* **9** - defragmenting hard disk
* **8** - antennas
* **7** - add math operators
* **6** - guard roaming around
* **5** - ordering pages
* **4** - X-MAS word search
* **3** - valid multiplications
* **2** - count monotonous sequences
* **1** - list similarity score

## 2023
* **25** - connected components
* **24** - intersecting linear paths of hails
* **23** - find longest path in maze
* **22** - falling bricks of sand
* **21** - making steps in the garden
* **20** - cables with flip flops
* **19** - part numbers satisfying inequality conditions
* **18** - calculate area inside dig path
* **17** - find path with minimal heatloss
* **16** - reflecting and splitting light beams
* **15** - HASHMAP of lenses in boxes
* **14** - tilt board with moving stones
* **13** - finding mirror symmetry
* **12** - fit blocks of damaged sprigs (nonogram-like)
* **11** - distances between expanding galaxies
* **10** - tracing pipe loop in a grid
* **9** - predict number series
* **8** - walking in circles in haunted desert
* **7** - comparing poker hands
* **6** - boat race quadratic equation
* **5** - seed dependency chain, interval mapping
* **4** - count winning lottery tickets
* **3** - find gears in grid
* **2** - counting colored cubes
* **1** - parse two digit numbers

## 2022
* **25** - snafu numbers
* **24** - going through blizzards
* **23** - elves spreading out - cellular automaton
* **22** - walking on a cube
* **21** - monkey expression tree
* **20** - mixing numbers in a circular list
* **19** - robots cracking geodes - material supply chain
* **18** - count surfaces of voxelated shape
* **17** - tetris
* **16** - elephants turning valves in maze
* **15** - beacons and sensor coverage
* **14** - sand flooding
* **13** - distress signal - sorting lists of ints
* **12** - shortest path in elevation grid
* **11** - monkeys throwing stuff
* **10** - display signal timings
* **9** - snapping rope
* **8** - tree heights for tree house
* **7** - cleaning filesystem
* **6** - finding start of packet
* **5** - stacking crates
* **4** - overlapping ranges
* **3** - organising rucksacks
* **2** - rock paper scissors
* **1** - count calories

## 2021
* **25** - moving sea-cucumbers (Biham-Middleton-Levine traffic model)
* **24** - reverse engineer ALU - find model number
* **23** - amphipods moving between houses
* **22** - partitioning cube space
* **21** - Dirac dice, 3-way universe splitting
* **20** - enhance image with "FFT"
* **19** - align scanners in 3D space
* **18** - add snailfish numbers
* **17** - discrete parabolas
* **16** - binary encoded packets
* **15** - find path with lowest cost
* **14** - insert elements into polymers
* **13** - folding dots on paper
* **12** - count distinct paths through caves
* **11** - flashing octopuses
* **10** - balanced parentheses
* **9** - finding low points and basins, counting clouds
* **8** - reconstruct 7-segment display
* **7** - aligning crabs
* **6** - count multiplying lanternfish
* **5** - Crossing lines
* **4** - Bingo
* **3** = count common bits
* **2** - submarine navigation
* **1** - count positive differences

## 2020
* **25** - crack the encryption
* **24** - hexagonal game of life
* **23** - shell game
* **22** - crab card game
* **21** - ingredient/allergen sudoku
* **20** - fractured image, monsters in a grid
* **19** - regular and not so regular rule matching
* **18** - expressions in elf math
* **17** - game of life in 3d and 4d
* **16** - ticket validation
* **15** - Van Eck sequence
* **14** - binary masks
* **13** - Bus schhedule - Chinese remainders problem
* **12** - ship navigation
* **11** - game of life with seats
* **10** - power adapters, tribonacci
* **9** - sums in sequences of numbers
* **8** - assembly with infinite loop
* **7** - graph of bags inside bags
* **6** - find any, find all
* **5** - binary space partition
* **4** - Passport validator
* **3** - Counting trees on slope
* **2** - Password validation - count characters
* **1** - Do they add up?

## 2019

* **25** - Intcode text Adventure
* **24** - Recursive Game of Life
* **23** - Nework of intcode computers
* **22** - Shuffle deck of cards - modular arithmetic
* **21** - ASCII Intcode jumping robot - bool formulas
* **20** - Recursive donut maze
* **19** - Tractor beam intcode
* **18** - Maze with doors
* **17** - Intcode ladders - robot's movement
* **16** - FFT - recursive sums of very long array
* **15** - Labyrinth - shortest and longest path
* **14** - Fuel - material chain
* **13** - Breakout game
* **12** - N-body simulation
* **11** - IntCode turtle graphics
* **10** - Asteroid grid, visibility and raycasting
* **9** - Finalize IntCode computer
* **8** - Render image from semitransparent layers
* **7** - Multiple IntCode machines with in/out chained
* **6** - Tree - distance to nearest common parent
* **5** - IntCode machine - inputs, outputs, conditionals
* **4** - Password check - properties of range of 6-digit numbers
* **3** - Trace wires in 2D grid - find nearest intersections
* **2** - IntCode machine - add and multiply
* **1** - Recurrent formula

## 2018
* **25** - count connected components
* **24** - battle of the immune system
* **23** - nanobot cloud with manhattan distances
* **22** - pathfinding in randomly generated terrain
* **21** - wristwatch computer: assembly analysis
* **20** - regex maze
* **19** - wristwatch computer: instruction pointer, loops, assembly analysis
* **18** - 3-state game of life with plasma effects
* **17** - water sinking in the soil
* **16** - wristwatch computer: figure out assembly opcodes
* **15** - elves fighting goblins
* **14** - mixing recipes - combining digits
* **13** - carts going around and crashing
* **12** - 1D game of life with plants
* **11** - find square with highest value
* **10** - iteratively move points + counting clouds
* **9** - game with marbles
* **8** - summing trees
* **7** - dependency graph
* **6** - Manhattan distances from coordinates
* **5** - candy crush
* **4** - sleeping guards
* **3** - overlapping rectangles of fabric
* **2** - string checksum - one letter differences
* **1** - sum of ints

## 2017
* **12** - connected components
* **11** - hexagonal grid
* **10** - Knot hash
* **9** - remove garbage from string
* **8** - conditional instructions
* **7** - balance process tree
* **6** - redistributing memory blocks - infinite loop
* **5** - Incrementing instructions
* **4** - Passwords - non-repeating strings and anagrams
* **3** - Manhattan distance on spiral
* **2** - Grid checksums - min, max and divisors
* **1** - Find pairs of same digits in a number

## 2016
* **25** - assembly signal generator
* **24** - navigate robot in a maze
* **23** - cracking safe code, self modifying assembly
* **22** - moving data in grid network
* **21** - password scrambling
* **20** - intervals of blocked IP addresses
* **19** - elf circle - Josephus problem
* **18** - count safe spaces in procedural grid
* **17** - path in md5 maze
* **16** - dragon curve and checksum
* **15** - timing dropping capsule, modular
* **14** - md5 hashes
* **13** - navigate bitcounting maze (A*, BFS)
* **12** - Interpretting assembly
* **11** - Moving chips and generators in a lift (goat and wolf problem)
* **10** - Network of bots passing numbers
* **9** - Word expansion
* **8** - Rotate pixels on small display
* **7** - Find palindromes of size 3 and 4
* **6** - Most frequent letters
* **5** - MD5 hashes again
* **4** - Decode meeting room names
* **3** - Detect valid triangles
* **2** - Move across a keypad
* **1** - Navigate in 2d street grid

## 2015
* **25** - diagonal security code
* **24** - balancing sleigh, split into equal weight groups
* **23** - Collatz in assembly
* **22** - RPG boss fight as wizard
* **21** - RPG boss fight
* **20** - infinite houses
* **19** - molecule formula; grammar
* **18** - game of life
* **17** - choose pots - kind of knapsack
* **16** - Aunt Sue
* **15** - combining cooking ingredients
* **14** - racing reindeers
* **13** - permutations of people
* **12** - parsing JSON
* **11** - find next valid password
* **10** - Look and Say numbers
* **9** - travelling salesman
* **8** - count escaped characters in strings
* **7** - Logical Circuit
* **6** - Light patterns (overlapping rectangles)
* **5** - Count nice words
* **4** - MD5 hashes
* **3** - Santa walking in a grid
* **2** - wrapping presents - how much material do we need?
* **1** - Count floors (parentheses)
