import vsketch
import math
import random

import numpy as np
import vpype as vp

from shapely.geometry import *
from shapely.ops import *


class S004Sketch(vsketch.SketchClass):
    with_moon = vsketch.Param(False)
    renderer = vsketch.Param("depthy", choices=["depthy", "flat"])

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        polys = []

        xs = [x for x in range(0, 10, 2) if vsk.random(1) > 0.3]
        random.shuffle(xs)

        vsk.line(-3, 22, 13, 22)

        for rocki, cx in enumerate(xs):
            l, t, r, b = cx - 3, 22 - vsk.random(9, 14), cx + 3, 22

            t1, t0 = vsk.random(0.2, 0.3), vsk.random(0.7, 0.8)
            t2, t3 = vsk.random(0.2, 0.4), vsk.random(0.2, 0.4)
            t4 = vsk.random(0.4, 0.6)

            b0 = (vsk.lerp(l, r, t0), b)
            b1 = (vsk.lerp(l, r, t1), b)
            l0 = (l, vsk.lerp(b, t, t2))
            t0 = (vsk.lerp(l, r, t4), t)
            r0 = (r, vsk.lerp(b, t, t3))

            boundary = Polygon([b0, b1, l0, t0, r0])

            if self.renderer == "depthy":
                while True:
                    x = (l + r) / 2 + vsk.random(0.5, 1.5)
                    y = (t + b) / 2 + vsk.random(0, 2)
                    if not boundary.contains(Point(x, y)):
                        continue

                    if boundary.exterior.distance(Point(x, y)) < 0.7:
                        continue

                    break

                xb = x - 0.6

                rock = [
                    Polygon([b1, l0, t0, (x, y), (xb, b)]),
                    Polygon([b0, b1, (x, y), t0, r0]),
                ]

                tex = MultiLineString(
                    [
                        [(x, b), (x + (r - l), t)]
                        for x in np.arange(
                            l - (r - l),
                            r + (r - l),
                            vsk.lerp(0.1, 0.2, rocki / len(xs)),
                        )
                    ]
                )
            else:
                rock = [boundary]

                def shading_lines(p0, p1):
                    d = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
                    for dt in np.arange(0, d, 0.1):
                        x, y = (
                            p0[0] + dt * (p1[0] - p0[0]) / d,
                            p0[1] + dt * (p1[1] - p0[1]) / d,
                        )
                        dd = vsk.random(0.4, 0.7)
                        yield [(x, y), (x + dd, y + dd)]

                tex = []
                tex.extend(shading_lines(b1, l0))
                tex.extend(shading_lines(l0, t0))
                tex = MultiLineString(tex)

            for i, p in enumerate(rock):
                for pp in polys:
                    p -= pp
                    if p.is_empty or not p.is_valid:
                        break
                else:
                    vsk.geometry(p)
                    if i == 0:
                        vsk.geometry(tex & p)
                    polys.append(p)

        if self.with_moon:
            moonx, moony = max(xs) + 3, 2
            w = vsk.random(2, 3)

            moon = Point(moonx, moony).buffer(w, resolution=64)
            shade = LineString(
                [
                    (p.real, p.imag)
                    for p in vp.arc(
                        moonx, moony, vsk.random(w * 0.8, w * 0.95), w, -90, 90
                    )
                ]
            )

            moon = split(moon, shade)
            vsk.geometry(moon)

            moon = max(moon.geoms, key=lambda g: -g.area)

            vsk.geometry(
                MultiLineString(
                    [
                        [(x, moony + w), (x + w, moony - w)]
                        for x in np.arange(moonx - w * 2, moonx + w, 0.1)
                    ]
                )
                & moon
            )

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S004Sketch.display()
