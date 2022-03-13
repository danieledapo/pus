import vsketch
import random
import math

import numpy as np
from shapely.geometry import *
from shapely.validation import *
from skimage.measure import find_contours


def rotate_x(l, a):
    c, s = math.cos(a), math.sin(a)
    for i in range(len(l)):
        x, y, z = l[i]
        l[i] = (x, y * c - z * s, y * s + z * c)


def smin(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h * h * k * (1.0 / 4.0)


def unit():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)

    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return (x, y, z)


class S001Sketch(vsketch.SketchClass):
    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("13cm")

        self.metaballs = []
        for _ in range(20):
            if not self.metaballs:
                self.metaballs.append((0, 0, 0, 0.2))
                continue

            while True:
                x, y, z, r = random.choice(self.metaballs)
                dx, dy, dz = unit()
                l = r + vsk.random(0.05, 0.25)
                xx, yy, zz = x + dx * l, y + dy * l, z + dz * l
                if -1 <= xx <= 1 and -1 <= yy <= 1 and -1 <= zz <= 1:
                    self.metaballs.append((xx, yy, zz, vsk.random(0.05, 0.1)))
                    break

        drawn = []
        for z in np.linspace(-1, 1, 100):
            cs = self.slice(z, 100)

            for c in cs:
                if len(c) <= 2:
                    continue

                c = [(x, y, z) for x, y in c]

                rotate_x(c, 30 / 180 * math.pi)

                p = make_valid(Polygon([(x, z) for x, _, z in c]))
                for pp in drawn:
                    if p.is_empty or not p.is_valid:
                        break
                    p -= pp
                else:
                    vsk.geometry(p)
                    drawn.append(p)

    def slice(self, z, n):
        grid = []
        for y in np.linspace(-1, 1, n):
            grid.append([])
            for x in np.linspace(-1, 1, n):
                d = float("inf")
                for mx, my, mz, r in self.metaballs:
                    dd = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) - r
                    d = smin(dd, d, 0.15)

                grid[-1].append(d)
        grid = np.asarray(grid)

        cs = []
        for c in find_contours(grid, 0.1):
            cs.append([(-1 + 2 * x / n, -1 + 2 * y / n) for x, y in c])

        return cs

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S001Sketch.display()
