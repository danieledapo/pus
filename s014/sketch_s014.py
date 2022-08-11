import random

import vsketch

import numpy as np

from shapely.affinity import translate
from shapely.geometry import MultiLineString, Polygon, box
from shapely.ops import clip_by_rect


class S014Sketch(vsketch.SketchClass):
    yreps = vsketch.Param(1, 0)
    xreps = vsketch.Param(4, 0)

    def decorations_tex(self, x0, y0, x1, y1):
        tex = MultiLineString([[(x, 0), (x + 20, 50)] for x in np.arange(-20, x1, 0.1)])
        return clip_by_rect(tex, x0, y0, x1, y1)

    def small_shadow_tex(self, x0, y0, x1, y1):
        return MultiLineString(
            [[(x0, y), (x1, y)] for y in np.arange(y0, y1, 0.13)]
        ) | self.decorations_tex(x0, y0, x1, y1)

    def concrete_tex(self, x0, y0, x1, y1):
        lines = []

        for x in np.arange(x0, x1, 0.2):
            l = []
            for y in np.arange(y0, y1 + 0.1, 0.1):
                t = max(0, 1 - (y - y0) / (y1 - y0))
                if t <= self.vsk.random(0.5):
                    l.append((x, y))
                elif len(l) > 1:
                    lines.append(l)
                    l = []
            if len(l) > 1:
                lines.append(l)

        return MultiLineString(lines)

    def draw_shadow(self, lastw, w, y, maxsh=0.7):
        vsk = self.vsk
        vsk.fill(1)
        sh = vsk.random(0.1, maxsh)
        shadow = Polygon(
            [
                (-lastw / 2, y),
                (lastw / 2, y),
                (w / 2, y + sh),
                (-w / 2, y + sh),
            ]
        )
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

            h = vsk.random(2, 6)
            if y + h > maxy:
                break

            if w > lastw:
                if vsk.random(1) > 0.3:
                    sh = self.draw_shadow(lastw, w, y)
                else:
                    sh = vsk.random(0.5, 1)
                    sw = lastw * 0.8
                    shadow = box(-sw / 2, y, sw / 2, y + sh)
                    vsk.geometry(shadow)
                    vsk.geometry(self.small_shadow_tex(-sw / 2, y, sw / 2, y + sh))

                y += sh
                h -= sh

            yreps = random.randrange(1, self.yreps + 1)
            xreps = random.randrange(1, self.xreps + 1)

            ww = w / xreps

            x0 = -w / 2
            block = box(x0, y, x0 + ww, y + h)

            # decorations
            decorations = Polygon()
            decs_tex = Polygon()
            if vsk.random(1) > 0.4:
                sx, sy = x0 + ww * 0.1, y + h * 0.1
                dw, dh = ww * 0.8, h * 0.8
                for _ in range(random.randrange(1, 3)):
                    if dw > dh:
                        sx = sx + dw / 2 if vsk.random(1) > 0.5 else sx
                        dw /= 2
                    else:
                        sy = sy + dh / 2 if vsk.random(1) > 0.5 else sy
                        dh /= 2

                decorations = box(sx, sy, sx + dw, sy + dh)
                decs_tex = self.decorations_tex(*decorations.bounds)

            # draw the block
            for i in range(yreps):
                concrete_tex = self.concrete_tex(x0, y, x0 + ww * xreps, y + h)

                for j in range(xreps):
                    b = translate(block, j * ww, i * h)
                    d = translate(decorations, j * ww, i * h)

                    vsk.geometry(b)
                    vsk.geometry(d)
                    vsk.geometry((concrete_tex & b) - d.buffer(0.1))
                    vsk.geometry(translate(decs_tex, j * ww, i * h))

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
        x0 = random.choice([1, -1]) * vsk.random(w * 0.25, w * 0.4)
        ch = vsk.random(1.4, 3)
        n = random.randrange(0, 4)
        for i in range(n):
            xx = x0 + i * 0.5
            if xx + 0.5 > w / 2:
                break

            chimney = box(xx, y, xx + 0.2, y + (i + 1) * ch / (n + 1))
            vsk.geometry(chimney)
            vsk.geometry(self.small_shadow_tex(*chimney.bounds))

        vsk.vpype("layout -m 2cm a4 squiggles")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort -t -p 10000")


if __name__ == "__main__":
    S014Sketch.display()
