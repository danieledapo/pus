import random
from typing import Iterator

import vsketch

from shapely.geometry import *
from shapely.affinity import *

import numpy as np


def unit(x, y):
    l = np.hypot(x, y)
    return (x / l, y / l)


def line_segment(l: LineString, start: float, end: float) -> LineString:
    ll = []
    for d in np.arange(start, end + 0.1, 0.1):
        p = l.interpolate(d)
        ll.append((p.x, p.y))
    return LineString(ll)


class S015Sketch(vsketch.SketchClass):
    squiggliness = vsketch.Param(0.3, 0.0)

    def perturb(self, l: LineString, xlate=0.2) -> LineString:
        return translate(
            rotate(l, self.vsk.random(-3, 3)),
            self.vsk.random(-xlate, xlate),
            self.vsk.random(-xlate, xlate),
        )

    def break_sometimes(
        self, l: LineString, step=0.1, select=None
    ) -> Iterator[LineString]:
        if select is None:
            select = lambda t: self.vsk.random(1) > 0.5

        ll = []
        for d in np.arange(0, l.length + step, step):
            t = d / (l.length + step)
            if select(t):
                ll.append(l.interpolate(d))
            else:
                if len(ll) > 1:
                    yield LineString(ll)
                ll = []

        if len(ll) > 1:
            yield LineString(ll)

    def squiggle(self, l: LineString) -> LineString:
        x, y = [], []

        for d in np.arange(0, l.length + 0.1, 0.1):
            p = l.interpolate(d)
            x.append(p.x)
            y.append(p.y)

        x, y = np.array(x), np.array(y)

        if self.squiggliness > 0:
            a = self.vsk.noise(x, y, grid_mode=False) * (np.pi * 2)
            x += np.cos(a) * self.squiggliness
            y += np.sin(a) * self.squiggliness

        return LineString(zip(x, y))

    def shading_lines(
        self,
        l: LineString,
        focus: tuple[float, float] = (0, 0),
        step: float = 5,
        maxdist=None,
    ):
        for t in np.arange(0, l.length + step, step):
            x1, y1 = l.interpolate(t).coords[0]
            dx, dy = unit(focus[0] - x1, focus[1] - y1)

            maxd = np.hypot(x1, y1) / 2 if maxdist is None else maxdist

            maxll = None
            for d in np.arange(0.2, maxd, 0.1):
                ll = LineString(
                    [
                        (x1 + dx * 0.1, y1 + dy * 0.1),
                        (x1 + dx * d, y1 + dy * d),
                    ]
                )

                if ll.intersects(l):
                    break

                maxll = LineString(
                    [
                        (x1, y1),
                        (x1 + dx * d, y1 + dy * d),
                    ]
                )

            if maxll is not None:
                yield self.squiggle(maxll)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")

        l = []
        a = 0
        r = 0.3

        n = random.randrange(120 * 2, 120 * 4)
        div = random.randrange(100, 200)
        da = np.radians(3)

        geos = []

        for i in range(n):
            x, y = np.cos(a) * r, np.sin(a) * r
            l.append((x, y))
            a += da
            r += max(0.02, r / div) * (1 + (i / n) * 0.5)

        lg = LineString(l)
        lg = self.squiggle(lg)
        geos.append(lg)

        for _ in range(5):
            center = line_segment(lg, 0, vsk.random(4, 8))
            geos.append(self.perturb(center, xlate=0.08))

            last = line_segment(lg, max(0, lg.length - vsk.random(60, 100)), lg.length)
            geos.append(self.perturb(last, xlate=0.08))

        for _ in range(5):
            lg = scale(lg, 0.98, 0.98)
            for _ in range(2):
                for ll in self.break_sometimes(self.perturb(lg)):
                    geos.append(ll)

        lg = LineString(l)

        nsegs = 50
        for ll in self.shading_lines(lg, step=lg.length / nsegs):
            for lp in self.break_sometimes(ll):
                geos.append(lp)

        ls = list(self.shading_lines(lg, step=lg.length / nsegs, maxdist=999999))[-1]
        geos.append(ls)
        for _ in range(3):
            geos.append(self.perturb(ls, xlate=0.1))

        geos = GeometryCollection(geos)

        geos = rotate(
            geos,
            -np.arctan2(
                ls.coords[-1][1] - ls.coords[0][1], ls.coords[-1][0] - ls.coords[0][0]
            ),
            use_radians=True,
        )

        l, t, r, b = geos.bounds
        if r - l > b - t:
            geos = rotate(geos, -90)

        vsk.geometry(geos)

        vsk.vpype("layout -m 2cm a5")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge -t 0.2mm linesimplify reloop linesort")


if __name__ == "__main__":
    S015Sketch.display()
