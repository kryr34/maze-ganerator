import sys
from itertools import chain
from typing import Tuple, Sequence
from collections import namedtuple
import random
from enum import Enum

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from mpl_toolkits.mplot3d.art3d import Line3D

class Point(namedtuple('Point', ['x', 'y', 'z'])):
    def __add__(self, other):
        return Point(*(np.array(self) + np.array(other)))

#Point = NDArray[np.int_]
P2P = Tuple[Point, Point]
Vector = Point
Rooms = NDArray[np.int_]

def dfs(shape: Tuple[int, int, int]) -> Sequence[P2P]:
    four_ways = [[1, 0],
                 [-1, 0],
                 [0, 1],
                 [0, -1]]
    directs: Sequence[Vector]= tuple(Point(x,y,z) for x,y in four_ways for z in (-1,0,1))
        
    roads: list[P2P] = []

    # chooce random point 
    start: Point = np.array([random.randrange(x) for x in shape])

    stk: list[Point] = [start]

    while stk:
        current: Point = stk.pop()
        #print(np.array(directs))
        #input()
        while True:
            move: Vector = random.choice(directs)
            nextP: Point = current + move
            try:
                if rooms[next] in (2, 3):
                    continue

                if move.z != 0:
                    # .?..rR.
                    # .?.rrR.
                    # --rrr--
                    # .Rrr.?.
                    # .Rr..?.
                    # R = Room  - = floor
                    # r = road  . = wall
                    # ? = possible room
                    po = current + move * [1, 2, 2]

                    if rooms[tuple(nextP)]:
                        raise IndexError

                    if rooms[tuple(current + nextP * [0, 1, 1])] in (2, 3, 4):
                        continue

                    if rooms[tuple(current + nextP * [1, 1, 1])] in (2, 3, 4):
                        continue

                if list(nextP) in map(list, chain.from_iterable(roads)):
                    continue

                if (nextP < 0).any():
                    continue

            except IndexError:
                continue
            # complete
            if p[0] != 0:
                if rooms[tuple(current + p * [0, 1, 1])] == 0:
                    print(current, n)
                    input()
                rooms[tuple(current + p * [0, 1, 1])] = 2
                rooms[tuple(current + p * [1, 1, 1])] = 3
            elif rooms[tuple(n)] == 1:
                rooms[tuple(n)] = 4

            roads.append((current, n))
            stk.append(current)
            stk.append(n)
            break


def display(roads: Sequence[Tuple[NDArray, NDArray]], h: int):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = [np.random.rand(3,) for _ in range(h)]

    lines_by_label: dict[int, list[Line3D]] = {i: [] for i in range(h)}

    for road in roads:
        b = np.array([[0, 0, 1],
                      [1, 0, 0],
                      [0, 1, 0]])
        road = np.matmul(road, b)

        groupby = road.T[2].min()

        line = ax.plot3D(*np.array(road).T, c=colors[groupby])[0]

        lines_by_label[groupby].append(line)

    rax = fig.add_axes([0.1, 0.5, 0.1, 0.15])
    chk = CheckButtons(
        ax=rax,
        labels=[str(i) for i in range(h)]
    )

    def cbk(label: str):
        lines = lines_by_label[int(label)]
        for line in lines:
            # print(line.get_data_3d())
            line.set_visible(not line.get_visible())
            line.figure.canvas.draw_idle()

    chk.on_clicked(cbk)

    plt.show()

class Room(Enum):
    NULL = 0
    ROAD = 1
    UP_STAIR = 2
    DOWN_STAIR = 3

if __name__ == '__main__':
    h, w, d = 3, 4, 4  # default parameters

    arg = tuple(map(int, sys.argv[1:]))
    if len(arg) == 3:
        h, w, d = arg
    elif len(arg) != 0:
        sys.exit("Wrong arguments")

    # def isEven(x):
    #     return x & 1 == 0

    # if isEven(w) or isEven(d):
    #     sys.exit("Arguments width or depth cannot be even number")

    print(h, w, d)

    rooms = np.zeros((h, w, d), dtype=Room)
    stairs = []
    roads = []

    print(rooms)

    roads: list[P2P] = dfs((h, w, d))

    print(rooms)
    #coinput()

    # print(rooms)
    # print(len(roads))
    roads = sorted(roads, key=lambda x: x[0][0])
    for r in roads:
        # print(r)
        pass
    # print(sorted(roads, key=lambda x,y: x[0]))
    display(roads, h)
    sys.exit()
