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


def smax(d1, d2, k):
    h = 0.5 - 0.5 * (d2 + d1) / k
    h = max(min(h, 1), 0)
    return ((1 - h) * d2 + h * (-d1)) + k * h * (1.0 - h)


def unit():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)

    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return (x, y, z)


class S001Sketch(vsketch.SketchClass):
    n = vsketch.Param(100)
    nballs = vsketch.Param(18)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("13cm")

        self.metaballs = []
        for _ in range(self.nballs):
            if not self.metaballs:
                self.metaballs.append((0, 0, 0, 0.2))
                continue

            while True:
                x, y, z, r = random.choice(self.metaballs)
                dx, dy, dz = unit()
                l = r + vsk.random(0.05, 0.25)
                xx, yy, zz = x + dx * l, y + dy * l, z + dz * l
                rr = vsk.random(0.05, 0.1)

                if all(-1 <= c + rr <= 1 and -1 <= c - rr <= 1 for c in (xx, yy, zz)):
                    self.metaballs.append((xx, yy, zz, rr))
                    break

        drawn = []
        for z in np.linspace(-1, 1, self.n):
            cs = self.slice(z, self.n)

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
        for y in np.linspace(-1, 1, n * 2):
            grid.append([])
            for x in np.linspace(-1, 1, n * 2):
                d = float("inf")
                for i, (mx, my, mz, r) in enumerate(self.metaballs):
                    dd = math.hypot(x - mx, y - my, z - mz) - r
                    if i % 3 == 0:
                        d = smax(dd, d, 0.15)
                    else:
                        d = smin(dd, d, 0.15)

                grid[-1].append(d)

        cs = []
        for c in find_contours(np.asarray(grid), 0.1):
            cs.append([(-1 + 2 * x / n / 2, -1 + 2 * y / n / 2) for x, y in c])

        return cs

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge -t 0.5 linesimplify reloop linesort")


if __name__ == "__main__":
    S001Sketch.display()
