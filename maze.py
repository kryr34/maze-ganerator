import numpy as np
from itertools import chain
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

def dfs(rooms, roads):
    start = np.array([random.randrange(x) for x in rooms.shape])
    while rooms[tuple(start)]==1:
        start = np.array([random.randrange(x) for x in rooms.shape])

    stk = [start]
    while stk:
        current = stk.pop()
        directs = [[0,1,0],
                   [0,-1,0],
                   [0,0,1],
                   [0,0,-1]]
        if rooms[tuple(current)] == 0:
            directs.extend([[1,1,0],
                            [1,-1,0],
                            [1,0,1],
                            [1,0,-1],
                            [-1,1,0],
                            [-1,-1,0],
                            [-1,0,1],
                            [-1,0,-1]])
        while True:
            if not directs:
                break
            p = np.array(random.choice(directs))
            directs.remove(list(p))
            n = current + p
            try:
                if rooms[tuple(n)] in (2,3): continue
                if p[0] != 0:
                    n = current + p*[1,2,2]
                    rooms[tuple(n)]
                    if rooms[tuple(current + p*[0,1,1])] in (2,3,4):
                        continue
                    if rooms[tuple(current + p*[1,1,1])] in (2,3,4):
                        continue
                if list(n) in map(list,chain.from_iterable(roads)):
                    continue
                if (n<0).any(): continue
            except IndexError:
                continue
            #complete
            if p[0] != 0:
                if rooms[tuple(current + p*[0,1,1])] == 0:
                    print(current, n)
                    input()
                rooms[tuple(current + p*[0,1,1])] = 2
                rooms[tuple(current + p*[1,1,1])] = 3
            elif rooms[tuple(n)] == 1:
                rooms[tuple(n)] = 4

            roads.append((current,n))
            stk.append(current)
            stk.append(n)
            break

def display(roads, h):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = [np.random.rand(3,) for _ in range(h)]
    for r in roads:
        b = np.array([[0,0,1],
                      [1,0,0],
                      [0,1,0]])
        r = np.matmul(r,b)
        ax.plot3D(*np.array(r).T, c=colors[r.T[2].min()])
    plt.show()

if __name__ == '__main__': 
    #h,w,d = 3,3,3
    h,w,d = 5,5,5
    arg = tuple(map(int, sys.argv[1:]))
    if len(arg) == 3:
        for a in arg:
            if a&1 == 0:
                break
        else:
            h,w,d = arg
    print(h,w,d)
    rooms = np.array([
            np.array([x&1 for x in range(w*d)]).reshape(w,d)
            for x in range(h)])
    stairs = []
    roads = []
    dfs(rooms, roads)
    #print(rooms)
    print(len(roads))
    roads = sorted(roads, key=lambda x: x[0][0])
    for r in roads:
        print(r)
    #print(sorted(roads, key=lambda x,y: x[0]))
    display(roads, h)
