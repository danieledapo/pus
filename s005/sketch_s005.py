from matplotlib.pyplot import text
import math
import random

import vpype as vp
import vsketch
import numpy as np

from shapely.geometry import *
from shapely.ops import *
from shapely.affinity import *


def polar(
    a: float, r: float = 1, c: tuple[float, float] = (0, 0)
) -> tuple[float, float]:
    return c[0] + r * math.cos(a), c[1] + r * math.sin(a)


class S007Sketch(vsketch.SketchClass):
    n = vsketch.Param(10)
    shape = vsketch.Param("square", choices=["square", "circle"])

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        if self.shape == "square":
            shapes = [box(-8, -8, 8, 8)]
        elif self.shape == "circle":
            shapes = [Point(0, 0).buffer(8)]

        for _ in range(self.n):
            l, t, r, b = GeometryCollection(shapes).bounds

            cx, cy = (l + r) / 2, (t + b) / 2
            r = 5 + max(r - l, b - t) / 2

            a0 = vsk.random(math.pi * 2)
            a1 = a0 + math.pi + vsk.random(-math.pi / 3, math.pi / 3)

            x0, y0 = polar(a0, r, c=(cx, cy))
            x1, y1 = polar(a1, r, c=(cx, cy))

            m = (y1 - y0) / (x1 - x0)
            q = y0 - m * x0

            ll = LineString([(x0, y0), (x1, y1)])
            displacement = random.choice([1, -1]) * vsk.random(0.3, 1)

            new_shapes = []
            for s in shapes:
                for ss in split(s, ll).geoms:
                    p = ss.centroid
                    if p.y > m * p.x + q:
                        dd = 1
                    else:
                        dd = -1

                    dx, dy = x1 - x0, y1 - y0
                    l = math.hypot(dx, dy)
                    dx, dy = dx / l, dy / l

                    new_shapes.append(
                        translate(ss, dx * displacement * dd, dy * displacement * dd)
                    )
            shapes = new_shapes

        to_draw = []
        for s in shapes:
            s = s.buffer(-vsk.random(0.05, 0.15))
            if s.area < 0.5:
                continue
            to_draw.append(s)
        to_draw = GeometryCollection(to_draw)

        l, t, r, b = to_draw.bounds
        sf = min(16 / (r - l), 22 / (b - t))
        to_draw = scale(to_draw, sf, sf)

        textured = []
        for s in to_draw.geoms:
            vsk.geometry(s)
            if vsk.random(1) > 0.65:
                textured.append(s)

        if textured:
            textured = MultiPolygon(textured)
            l, t, r, b = textured.bounds
            tex = MultiLineString(
                [
                    [(x, t), (x + r - l, b)]
                    for x in np.arange(l - (r - l), r + (r - l), 0.2)
                ]
            )
            vsk.geometry(tex & textured)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S007Sketch.display()
