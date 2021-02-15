#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Same game from Simon Tatham's Portable Puzzle Collection

import random as r
import time as t


M, N = 8, 8 # size rows*columns
colors = 3
nei = [(-1, 0), (1, 0), (0, -1), (0, 1)] # neighbors of a cell


# algoritm A : remove the biggest group each time
# algoritm B : remove color by color from biggest to smallest when possible
# algoritm C : remove color by color from smallest to biggest when possible
# algoritm D : remove the color that is most scattered first
# algoritm E : algoC but recalculates scattering of colors each step
# algoritm F : 


class SameGame():
    """"""
    def __init__(self, m=M, n=N):
        self.m, self.n = m, n

    def algoA(self):
        """"""
        while not self.is_end():
            color = 1
            biggest = 0
            for i in range(1, colors+1):
                try:
                    if len(self.groups[i][0]) > biggest:
                        biggest = len(self.groups[i][0])
                        color = i
                except IndexError: # when encountering a color with no groups
                    continue
            self.click_cell(color, 0)
            self.find_groups()

    def algoB(self):
        """"""
        while not self.is_end():
            for c in range(1, colors+1):
                if len(self.groups[c]):
                    self.click_cell(c, 0)
                    self.find_groups()
                    break

    def algoC(self):
        """"""
        while not self.is_end():
            for c in range(1, colors+1):
                if len(self.groups[c]):
                    self.click_cell(c, -1)
                    self.find_groups()
                    break

    def algoD(self):
        """"""
        colorClusters = [(i, len(self.groups[i])) for i in range(1, colors+1)]
        colorClusters.sort(key=lambda x: x[1])
        while not self.is_end():
            for c, j in colorClusters:
                if len(self.groups[c]):
                        self.click_cell(c, 0)
                        self.find_groups()
                        break

    def algoE(self):
        """"""
        while not self.is_end():
            colorClusters = [(i, len(self.groups[i])) for i in range(1, colors+1)]
            colorClusters.sort(key=lambda x: x[1])
            for c, j in colorClusters:
                if len(self.groups[c]):
                        self.click_cell(c, 0)
                        self.find_groups()
                        break

    def reset(self):
        """"""
        #self.grid = [[r.randint(1, colors) for j in range(self.n)]
        #             for i in range(self.m)]
        self.currM, self.currN = self.m, self.n # when row/col deleted
        self.selected = []
        self.selectedColor = 0
        self.groups = dict() # {color:list of all groups}
        self.score = 0
        self.find_groups()

    def is_end(self):
        for k, v in self.groups.items():
            try:
                if len(v[0]) > 1:
                    return False
            except:
                continue
        return True

    def cells_remaining(self):
        """Return the number of cells remaining on the grid"""
        r = 0
        for i in range(self.currM):
            for j in range(self.currN):
                if self.grid[i][j]:
                    r += 1
        return r

    def find_groups(self):
        """Find all groups of connected colors"""
        checked = []
        self.groups = {i:[] for i in range(colors+1)}
        for i in range(self.m):
            for j in range(self.n):
                if (i, j) in checked or self.grid[i][j] == 0:
                    continue
                self.selected.clear()
                self.selectedColor = self.grid[i][j]
                self.selected.append((i, j))
                self.select_area(i, j) # to update self.selected
                checked += self.selected
                if len(self.selected) <= 1:
                    continue
                self.groups[self.grid[i][j]].append(self.selected[:])
        for i in range(colors+1):
            self.groups[i].sort(key=len, reverse=True)

    def click_cell(self, color, index):
        for i, j in self.groups[color][index]:
            self.grid[i][j] = 0
        self.score += max(0, len(self.groups[color][index])-2)**2
        
        self.update_grid_left()
        self.update_grid_down()

    def select_area(self, row, col):
        """Update selected cells of the same color"""
        for i, j in nei:
            R, C = row+i, col+j
            # if on grid and not selected and same color
            if 0 <= R < self.m and 0 <= C < self.n and\
               (R, C) not in self.selected and\
               self.grid[R][C] == self.selectedColor:
                self.selected.append((R, C))
                self.select_area(R, C)

    def update_grid_left(self):
        """Push everything Left"""
        # push everything to the left
        for col in range(self.currN):
            allZero = True
            for i in range(self.currM):
                if self.grid[i][col] != 0:
                    allZero = False
                if not allZero:
                    break
            if allZero:
                for i in range(self.currM):
                    del self.grid[i][col]
                    self.grid[i].append(0)
                self.currN -= 1
                return self.update_grid_left()
    
    def update_grid_down(self):
        """Push everything down"""
        change = False
        for row in range(self.m-1, 0, -1):
            for j in range(self.currN):
                if self.grid[row][j] == 0 and self.grid[row-1][j] != 0:
                    self.grid[row][j] = self.grid[row-1][j]
                    self.grid[row-1][j] = 0
                    change = True
        if change:
            self.update_grid_down()

    def display(self):
        for i in self.grid:
            print("  ".join(map(str, i)))

if __name__ == '__main__':
    algorithms = ["algoA", "algoB", "algoC", "algoD", "algoE"]
    tests = 2000
    SG = SameGame(M, N)
    # generates grid before to make sure all algorithms has the same grids
    grids = tuple([[r.randint(1, colors) for j in range(N)]
                   for i in range(M)] for _ in range(tests))
    print(tests, "tests")
    for a in algorithms:
        scores, rests = [], []
        for i in range(tests):
            SG.grid = [i[:] for i in grids[i]]
            SG.reset()
            SG.__getattribute__(a)()
            scores.append(SG.score)
            rests.append(SG.cells_remaining())
        print("{}\tavg: {}\tmax: {}\tcompleted: {}"\
              .format(a, round(sum(scores)/tests), max(scores), rests.count(0)))
