# My entry for #WCCChallenge: Blobs
#
# So, for this week's challenge I wanted to come up with my own way of creating
# blobby-like shapes because I'm can't figure out how to properly use bezier
# curves. I could have used noise, but dunno, I feel like I don't have that much
# control over it.
#
# So, I started messing around with this algorithm based on circle packing and
# drawing arcs which seemed to give good results at first, but the blobs are a
# bit too sharp and generating non-intersecting closed blobs turned out to be
# quite annoying to implement.
#
# Anyway, I was running out of time and decided to do a visualization of numbers
# with what I got.
#
# Here's the idea: Pick a given N=number of bits and divide a circle in N
# touching circles.
#
#                   N=3                                                N=4
#
#       ⠀⠀⠀⠀⠀⣀⡤⠤⠖⠒⠦⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠤⠤⠤⣄⡀
#       ⠀⠀⢀⡴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠀⠀⠀⠀⠈⠓⢄
#       ⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳
#       ⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇
#       ⢸⠀⠀⠀⠀⠀⠀⠀⢀⡠⠔⠒⠋⠉⠉⠉⠓⢺⠤⣀⠀⢀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢀⡠⠔⠒⠋⠉⠉⠉⠓⠒⠤⣀⠀⡇
#       ⢸⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⢸⣠⠜⠛⢯⡀⠀⠀⠀⠈⠉⠓⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠤⠤⠤⣤⡿⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡹⣧⡤⠤⠤⠤⣄⡀
#       ⠈⢇⠀⠀⠀⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠟⠁⠀⠀⠀⠳⡄⠀⠀⠀⠀⠀⠀⠙⢆⠀⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠀⠀⡴⠃⠈⠛⢆⡀⠀⠀⠀⠀⠀⠀⠀⣀⠞⠋⠀⠳⡄⠀⠀⠀⠈⠓⢄
#       ⠀⠈⢣⡀⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡏⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⢰⠋⠀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠈⢻⠒⠦⠤⠤⠤⠖⢺⠋⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠈⢳
#       ⠀⠀⠀⠉⡷⢤⣀⡀⠀⠀⠀⣀⣠⠴⠋⢹⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠈⡇
#       ⠀⠀⠀⠀⣧⠴⠒⠋⠉⠉⠉⠓⠲⢤⡀⢸⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⡇
#       ⠀⠀⡰⠊⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠺⡆⠀⠀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⡸⣁⡤⠤⠤⠤⣄⡹⡀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠀⠀⡸⠁
#       ⠀⡜⠁⠀⠈⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣄⠀⠀⠀⠀⣠⠏⠀⠀⠀⠀⠀⠀⢀⡜⠁⠀⠀⠀⠀⠀⠙⢆⡀⠀⠀⠀⠈⢧⡀⠀⣀⠞⠋⠀⠀⠀⠀⠀⠀⠈⠛⢆⡀⠀⣠⠏⠀⠀⠀⠀⣀⠞⠁
#       ⢸⠁⠀⠀⠀⠀⠱⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠳⢤⣀⡴⠁⠀⠀⠀⠀⠀⣠⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠒⠦⠤⠤⠤⠷⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡶⠧⠤⠤⠤⠖⠚⠁
#       ⢸⠀⠀⠀⠀⠀⠀⠀⠑⠦⣄⣀⠀⠀⠀⠀⢀⣸⡤⠖⠉⠙⠒⠒⠒⠒⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠑⠦⣄⣀⠀⠀⠀⠀⢀⣀⡤⠖⠉⡇
#       ⠸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⡇
#       ⠀⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠁
#       ⠀⠀⠙⢆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢆⡀⠀⠀⠀⠀⠀⠀⠀⣀⠞⠁
#       ⠀⠀⠀⠀⠉⠒⠦⠤⣄⣀⡤⠤⠖⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠒⠦⠤⠤⠤⠖⠚⠁
#
#
# Turn on/off each bit randomly and bits that are ON are merged together, bits
# that are off are circles on their own.
#
#          7 (0b111)                           0 (0b000)                           13 (0b1101)
#    ⠀⠀⠀⢀⣠⠤⠤⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠤⣀⣀
#    ⠀⣠⠞⠁⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠤⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⠋⠀⠀⠀⠀⠈⠓⣄
#    ⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠙⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇
#    ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸
#    ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡴⠚⠉⠀⠀⠀⠈⠙⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠤⠒⠢⠤⣧⡀⠀⠀⠀⠀⠀⠀⠀⣠⡧⠤⠒⠢⠤⣄
#    ⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⣀⠀⠀⠀⣀⡴⠃⣠⠄⢀⡴⠋⠁⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⢀⡴⠉⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠈⠱⣄
#    ⠀⠈⠲⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⣁⡠⠖⡏⠀⡞⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀
#    ⠀⠀⣠⠔⠚⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠓⠢⣄⡇⠀⣇⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃
#    ⢠⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠚⠉⠉⠉⠓⢦⡀⠻⠄⠘⢦⡀⠀⠀⠀⠀⣠⠞⠀⠀⠀⠀⠀⠘⢦⠀⠀⠀⠀⠀⠀⠀⢀⡴⠒⠊⠉⠒⠲⣄⠀⠀⠀⠀⠀⠀⠀⢠⠞
#    ⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⢦⣀⠀⠀⠀⠀⠀⢀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠉⠓⠒⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⠤⣀⡠⠤⠞⢁⡴⠋⠉⠉⠉⠳⣄⠙⠦⠤⣀⡠⠤⠞⠁
#    ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠈⠉⠒⠒⠒⠊⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡅⠀⠀⠀⠀⠀⠀⠀⢨⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⢸
#    ⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡀⠀⠀⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⠀⡸
#    ⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⠤⠤⠤⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⠤⠤⠤⠞⠁
#    ⠀⠀⠈⠑⠲⠤⠤⠤⠖⠊⠁
#
# P.S. this was all an excuse to draw some braille diagrams :D
#

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


def bits_on(n: int) -> int:
    return bin(n)[2:].count("1")


class S017Sketch(vsketch.SketchClass):
    n = vsketch.Param(3)
    mode = vsketch.Param("grid")
    page = vsketch.Param("a4", choices=["a4", "a5"])

    def draw_bits(self, bits: int, n: int, r: int = 1, c=(0, 0)):
        points = []
        circles = []

        angs = [i * math.tau / n for i in range(n)]

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
        if bits_on(bits) > bits_on(nbits):
            blob, circles = circles, blob

        return blob, circles

    def draw(self, vsk: vsketch.Vsketch) -> None:
        w, h = 18, 25
        if self.page == "a5":
            w, h = 12, 18

        vsk.size(self.page, landscape=False)
        vsk.scale("cm")

        vsk.penWidth("0.2mm")

        maxn = 1 << self.n

        if self.mode == "grid":
            ns = list(range(maxn))
            nbits = [self.n for _ in ns]
        elif self.mode == "random":
            ns = [random.randrange(maxn)]
            nbits = [self.n]
        else:
            ns = [int(s) for p in self.mode.strip().split(",") for s in p.split() if s]
            nbits = [max(self.n, len(bin(n)[2:])) for n in ns]

        if not ns:
            return

        rows, cols = None, None
        mind = None
        for rr in range(len(ns) + 1):
            for cc in range(len(ns) + 1):
                d = abs(rr - cc)
                if rr * cc < len(ns):
                    continue

                if mind is None or d < mind:
                    rows, cols = rr, cc
                    mind = d

        blacks = []
        whites = []
        for row in range(rows):
            for col in range(cols):
                i = row * cols + col
                if i >= len(ns):
                    continue

                b, c = self.draw_bits(ns[i], nbits[i], c=(col * 4, row * 4))

                blacks.extend(b.geoms)
                whites.extend(c.geoms)
        blacks, whites = GeometryCollection(blacks), GeometryCollection(whites)

        l, t, r, b = GeometryCollection(list(blacks.geoms) + list(whites.geoms)).bounds
        o = (l + r) / 2, (t + b) / 2
        sf = min(h / (b - t), w / (r - l))

        whites = scale(whites, sf, sf, origin=o)
        blacks = scale(blacks, sf, sf, origin=o)

        vsk.fill(1)
        for b in range(1):
            vsk.geometry(blacks.buffer(-0.1 * b))
        vsk.noFill()

        vsk.strokeWeight(3)
        vsk.geometry(whites)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S017Sketch.display()
