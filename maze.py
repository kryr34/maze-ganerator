import sys
from itertools import chain
import random

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from mpl_toolkits.mplot3d.art3d import Line3D


def dfs(rooms: NDArray[np.int_], roads):
    start: NDArray[np.int_] = np.array([random.randrange(x) for x in rooms.shape])
    while rooms[tuple(start)] == 1:
        start = np.array([random.randrange(x) for x in rooms.shape])

    stk = [start]
    while stk:
        current = stk.pop()
        directs = [[0, 1, 0],
                   [0, -1, 0],
                   [0, 0, 1],
                   [0, 0, -1]]
        if rooms[tuple(current)] == 0:
            directs.extend([[1, 1, 0],
                            [1, -1, 0],
                            [1, 0, 1],
                            [1, 0, -1],
                            [-1, 1, 0],
                            [-1, -1, 0],
                            [-1, 0, 1],
                            [-1, 0, -1]])
        while True:
            if not directs:
                break
            p: NDArray[np.int_] = np.array(random.choice(directs))
            directs.remove(list(p))
            n = current + p
            try:
                if rooms[tuple(n)] in (2, 3):
                    continue

                if p[0] != 0:
                    n = current + p * [1, 2, 2]

                    if rooms[tuple(n)]:
                        raise IndexError

                    if rooms[tuple(current + p * [0, 1, 1])] in (2, 3, 4):
                        continue

                    if rooms[tuple(current + p * [1, 1, 1])] in (2, 3, 4):
                        continue

                if list(n) in map(list, chain.from_iterable(roads)):
                    continue

                if (n < 0).any():
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


def display(roads, h: int):
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

    # movq    16(%rsp), %rax
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


if __name__ == '__main__':
    h, w, d = 5, 5, 5  # default parameters

    arg = tuple(map(int, sys.argv[1:]))
    if len(arg) == 3:
        h, w, d = arg
    elif len(arg) != 0:
        sys.exit("Wrong arguments")

    def isEven(x):
        return x & 1 == 0

    if isEven(w) or isEven(d):
        sys.exit("Arguments width or depth cannot be even number")

    print(h, w, d)

    rooms = np.array(
        [
            np.array([x & 1 for x in range(w * d)]).reshape(w, d)
            for x in range(h)
        ])
    stairs = []
    roads = []

    dfs(rooms, roads)

    # print(rooms)
    # print(len(roads))
    roads = sorted(roads, key=lambda x: x[0][0])
    for r in roads:
        # print(r)
        pass
    # print(sorted(roads, key=lambda x,y: x[0]))
    display(roads, h)
    sys.exit()
