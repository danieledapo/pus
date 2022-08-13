#
# Concrete Monoliths
#
# Raw concrete blocks stacked on top of one another to build monuments to the
# Brutalist Gods.
#
# This is my entry for WCC Brutalism.
#
# My intention was to generate some brutalist towers or buildings but eventually
# got lost in the details of windows and balconies. So, I decided to remove all
# of the details and just keep the raw blocks of concrete which also feels more
# in line with the brutalism idea :D.
#
# I focused more on the textures trying to find a good balance between dark and
# light areas. Not quite sure I got there, but I kinda like the plots anyway.
#

import random

import vsketch

import numpy as np

from shapely.affinity import translate
from shapely.geometry import MultiLineString, Polygon, box


class S014Sketch(vsketch.SketchClass):
    # sketch parameters
    block_hr = vsketch.Param(0.2, 0, 1)  # aspect ratio of the blocks
    yreps = vsketch.Param(1, 0)  # maximum number of block repetitions in Y
    xreps = vsketch.Param(4, 0)  # maximum number of block repetitions in X
    min_xreps = vsketch.Param(1, 0)  # minimum number of block repetitions in X
    erosion = vsketch.Param(0.5, 0, 1)  # how much of the block is eroded
    support = vsketch.Param(0.7, 0, 1)  # probability of drawing a support

    # texture of the support block
    def support_tex(self, x0, y0, x1, y1):
        lines = []
        for y in np.arange(y0, y1, 0.13):
            lines.append([(x0, y), (x1, y)])

        for x in np.arange(x0, x1, 0.13):
            lines.append([(x, y0), (x, y1)])

        return MultiLineString(lines)

    # texture of all the simple concrete blocks
    def concrete_tex(self, x0, y0, x1, y1):
        lines = []

        for x in np.arange(x0, x1, 0.2):
            l = []
            for y in np.arange(y0, y1 + 0.1, 0.1):
                t = max(0, 1 - (y - y0) / (y1 - y0))
                if t <= self.vsk.random(self.erosion):
                    l.append((x, y))
                elif len(l) > 1:
                    lines.append(l)
                    l = []
            if len(l) > 1:
                lines.append(l)

        return MultiLineString(lines)

    # draw a filled shadow
    def draw_shadow(self, lastw, w, y, maxsh=0.7):
        vsk = self.vsk
        sh = vsk.random(0.1, maxsh)
        shadow = Polygon(
            [
                (-lastw / 2, y),
                (lastw / 2, y),
                (w / 2, y + sh),
                (-w / 2, y + sh),
            ]
        )
        vsk.fill(1)
        vsk.geometry(shadow)
        vsk.noFill()
        return sh

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        vsk.scale(1, -1)

        maxy = 24

        lastw = 1e30
        y = 0

        vsk.line(-9, 0, 9, 0)

        while True:
            if y == 0:
                w = int(vsk.random(10, 16))
            else:
                w = lastw + random.choice(
                    [
                        dx
                        for dx in range(-3, 4, 2)
                        if dx != 0 and 1 <= lastw + dx <= 18 and lastw + dx >= 3
                    ]
                )

            # h = vsk.random(2, 6)
            h = vsk.random(w * self.block_hr / 2, w * self.block_hr)
            if y + h > maxy:
                break

            # draw a shadow or a support
            if y != 0 and vsk.random(1) < self.support:
                if w > lastw:
                    sh = self.draw_shadow(lastw, w, y)
                else:
                    sh = vsk.random(0.5, 1)
                    sw = w * 0.8
                    shadow = box(-sw / 2, y, sw / 2, y + sh)
                    vsk.geometry(shadow)
                    vsk.geometry(self.support_tex(-sw / 2, y, sw / 2, y + sh))

                y += sh

            yreps = random.randrange(1, self.yreps + 1)
            xreps = random.randrange(self.min_xreps, self.xreps + 1)

            ww = w / xreps

            x0 = -w / 2
            block = box(x0, y, x0 + ww, y + h)

            # draw and repeat the block
            for i in range(yreps):
                for j in range(xreps):
                    b = translate(block, j * ww, i * h)
                    vsk.geometry(b)
                    vsk.geometry(self.concrete_tex(*b.bounds))

                y += h
                if y > maxy:
                    break

            lastw = w

        # roof
        w = lastw + 0.3
        y += self.draw_shadow(lastw, w, y, 0.4)
        roof = box(-w / 2, y, w / 2, y + 0.4)
        vsk.geometry(roof)
        vsk.geometry(self.concrete_tex(*roof.bounds))
        y += 0.4

        # chimneys
        x0 = random.choice([1, -1]) * vsk.random(w * 0.25, w * 0.4)
        ch = vsk.random(1.4, 3)
        n = random.randrange(0, 4)
        for i in range(n):
            xx = x0 + i * 0.5
            if xx + 0.5 > w / 2:
                break

            chimney = box(xx, y, xx + 0.2, y + (i + 1) * ch / (n + 1))
            vsk.geometry(chimney)
            vsk.geometry(self.support_tex(*chimney.bounds))

        # the squiggles command does all the work of deforming the paths so that
        # they have this hand-drawn feel to them
        vsk.vpype("layout -m 2cm a4 squiggles")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        # these are optimizations really useful when plotting because here we're
        # merging and simplifying the paths and even re-arranging the paths to
        # minimize pen-up travel distance! Thanks, vpype :)!
        vsk.vpype("color black linemerge linesimplify reloop linesort -t -p 10000")


if __name__ == "__main__":
    S014Sketch.display()
