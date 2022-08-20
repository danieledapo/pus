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
    swap = start > end
    if swap:
        start, end = end, start
    ll = []
    for d in np.arange(start, end + 0.1, 0.1):
        p = l.interpolate(d)
        ll.append((p.x, p.y))
    if swap:
        ll = ll[::-1]
    return LineString(ll)


def fit_in(lg: LineString, w: int, h: int) -> LineString:
    l, t, r, b = lg.bounds
    sf = min(w, h) / max(b - t, r - l)
    return scale(lg, sf, sf, origin=(0, 0))


class S015Sketch(vsketch.SketchClass):
    squiggliness = vsketch.Param(0.2, 0.0)

    def perturb(self, l: LineString, xlate=0.2, rot=3) -> LineString:
        return translate(
            rotate(l, self.vsk.random(-rot, rot)),
            self.vsk.random(-xlate, xlate),
            self.vsk.random(-xlate, xlate),
        )

    def break_sometimes(self, l: LineString, step=0.05) -> Iterator[LineString]:
        ll = []
        for d in np.arange(0, l.length + step, step):
            if self.vsk.random(1) > 0.5:
                ll.append(l.interpolate(d))
            else:
                if len(ll) > 1:
                    yield LineString(ll)
                ll = []

        if len(ll) > 1:
            yield LineString(ll)

    def squiggle(self, l: LineString, s: float = None) -> LineString:
        s = s if s is not None else self.squiggliness
        if s <= 0:
            return l

        x, y = [], []

        for d in np.arange(0, l.length + 0.1, 0.1):
            p = l.interpolate(d)
            x.append(p.x)
            y.append(p.y)

        x, y = np.array(x), np.array(y)

        a = self.vsk.noise(x, y, grid_mode=False) * (np.pi * 2)
        x += np.cos(a) * s
        y += np.sin(a) * s

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
                yield maxll

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=True)
        vsk.scale("cm")

        beta = vsk.random(0.1, 0.3)
        turns = random.randrange(2, 5)

        # logarithmic spiral
        thetas = np.arange(0, np.pi * 2 * turns, np.radians(3))
        rrs = np.exp(thetas * beta)
        lg = LineString(zip(rrs * np.cos(thetas), rrs * np.sin(thetas)))

        lg = self.squiggle(fit_in(lg, 15, 21))
        vsk.geometry(lg)

        breakd = 1e30
        for d in np.arange(lg.length, 0, -0.1):
            p = lg.interpolate(d)
            if p.x < 0 and p.y > 0:
                breakd = d
                break

        for _ in range(8):
            center = line_segment(lg, 0, vsk.random(0.75 * breakd, breakd * 1.25))
            vsk.geometry(self.perturb(center, xlate=0.08))

            last = line_segment(
                lg, max(0, vsk.random(1.25 * breakd, 1.75 * breakd)), lg.length
            )
            vsk.geometry(self.perturb(last, xlate=0.08, rot=0))

        lgg = lg
        for _ in range(8):
            lgg = scale(lgg, 0.98, 0.98)
            for _ in range(2):
                for ll in self.break_sometimes(self.perturb(lgg)):
                    vsk.geometry(ll)

        nsegs = vsk.random(10, 30)
        for ll in self.shading_lines(lg, step=lg.length / nsegs):
            for _ in range(2):
                ls = self.squiggle(self.perturb(ll), self.squiggliness)
                for lp in self.break_sometimes(ls):
                    vsk.geometry(lp)

        ls = list(self.shading_lines(lg, step=lg.length, maxdist=9999))[-1]
        ls = self.squiggle(ls, self.squiggliness)
        vsk.geometry(ls)
        for _ in range(7):
            vsk.geometry(self.perturb(ls, xlate=0.05, rot=1))

        vsk.vpype("layout -l -m 2cm a5")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge -t 0.2mm linesimplify reloop linesort")


if __name__ == "__main__":
    S015Sketch.display()
