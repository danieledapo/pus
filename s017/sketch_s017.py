import vsketch

import math
import random

import numpy as np

from shapely.geometry import *
from shapely.affinity import *


def angle(dy, dx):
    a = -math.atan2(dy, dx)
    if a < 0:
        a += math.tau
    return a


def polar(a: float, r: float, c=(0, 0)):
    return c[0] + r * math.cos(a), c[1] + r * math.sin(a)


def arc_points(x: float, y: float, r: float, a0: float, a1: float):
    step = np.radians(1)

    aa = a0
    while abs(aa - a1) > step:
        yield polar(aa, r, c=(x, y))
        aa = (aa + step) % math.tau

    # yield polar(a1, r, c=(x, y))


def bit_on_count(n: int) -> int:
    return bin(n)[2:].count("1")


class S017Sketch(vsketch.SketchClass):
    n = vsketch.Param(3)
    grid = vsketch.Param(1)
    bits = vsketch.Param(-1)

    def draw_bits(self, bits: int, r: int, c=(0, 0)):
        points = []
        circles = []

        angs = [i * math.tau / self.n for i in range(self.n)]

        t0 = 0.5 if len(angs) % 2 != 0 else self.vsk.random(1 / math.sqrt(2), 0.5)
        t1 = 1 - t0

        for i, ca in enumerate(angs):
            pa = angs[i - 1]
            na = angs[(i + 1) % len(angs)]

            cx, cy = polar(ca, r)
            px, py = polar(pa, r)
            nx, ny = polar(na, r)

            on = (bits >> i) & 1 == 1

            rr = math.hypot(cx - px, cy - py) * [t0, t1][i % 2]

            a0 = math.tau - angle(py - cy, px - cx)
            a1 = math.tau - angle(ny - cy, nx - cx)
            if not on:
                a0, a1 = a1, a0

            pts = list(arc_points(c[0] + cx, c[1] + cy, rr, a0, a1))
            if not on:
                pts.reverse()

            points.extend(pts)
            if not on:
                circles.append(Point(c[0] + cx, c[1] + cy).buffer(rr * 0.7))

        blob = Polygon(points)

        blob, circles = GeometryCollection([blob]), GeometryCollection(circles)

        nbits = ((1 << self.n) - 1) ^ bits
        if bit_on_count(bits) > bit_on_count(nbits):
            blob, circles = circles, blob

        return blob, circles

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        vsk.penWidth("0.2mm")

        maxn = 1 << self.n

        if self.grid and self.bits < 0:
            blacks = []
            whites = []

            rows, cols = None, None
            mind = None
            for ci in range(0, self.n):
                cc = 1 << ci
                rr = (1 << self.n) // cc
                d = abs(rr - cc)
                if mind is None or d < mind:
                    rows, cols = rr, cc
                    mind = d

            for row in range(rows):
                for col in range(cols):
                    bits = row * cols + col

                    if bits >= maxn:
                        continue

                    b, c = self.draw_bits(bits, 1, c=(col * 4, row * 4))

                    blacks.extend(b.geoms)
                    whites.extend(c.geoms)

            blacks, whites = GeometryCollection(blacks), GeometryCollection(whites)
        else:
            bits = random.randrange(maxn) if self.bits < 0 else self.bits
            blacks, whites = self.draw_bits(bits, 1)

        l, t, r, b = GeometryCollection(list(blacks.geoms) + list(whites.geoms)).bounds
        o = (l + r) / 2, (t + b) / 2
        sf = min(25 / (b - t), 18 / (r - l))

        whites = scale(whites, sf, sf, origin=o)
        blacks = scale(blacks, sf, sf, origin=o)

        vsk.fill(1)
        vsk.geometry(blacks)
        vsk.noFill()

        vsk.strokeWeight(3)
        vsk.geometry(whites)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S017Sketch.display()
