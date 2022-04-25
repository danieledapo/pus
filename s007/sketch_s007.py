from typing import Union
import vsketch
import math

import numpy as np

from shapely.geometry import *
from shapely.ops import *
from shapely.affinity import *


class S007Sketch(vsketch.SketchClass):
    n = vsketch.Param(20, 0)

    def split(
        self, shape: Union[Polygon, MultiPolygon]
    ) -> tuple[MultiPolygon, MultiPolygon]:
        split_line = LineString([(0, -20), (0, 20)])

        left, right = [], []
        for g in split(shape, split_line).geoms:
            l, _, r, _ = g.bounds
            if l < 0:
                left.append(g)
            elif r > 0:
                right.append(g)

        return MultiPolygon(left), MultiPolygon(right)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        back = box(-8, -10, 8, 10)

        subj = []
        for _ in range(self.n):
            cx, cy = vsk.random(-5, 7), vsk.random(-6, 6)
            tx = (cx + 5) / (10)
            r = vsk.lerp(2, 0.7, tx)
            # cx, cy = vsk.random(-7, 7), vsk.random(-6, 5)
            # r = 2 + 5 * vsk.noise(cx * 0.05, cy * 0.05)
            a0, a1, a2 = (
                vsk.random(math.tau / 3),
                vsk.random(math.tau / 3, math.tau / 3 * 2),
                vsk.random(math.tau / 3 * 2, math.tau),
            )

            p0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
            p1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
            p2 = cx + r * math.cos(a2), cy + r * math.sin(a2)

            pp = Polygon([p0, p1, p2]) & back
            for p in subj:
                pp -= p
                if not pp.is_valid or pp.is_empty:
                    break
            else:
                pp = pp.buffer(-vsk.random(0.1, 0.3))
                geos = [pp] if isinstance(pp, Polygon) else pp.geoms
                subj.extend((g for g in geos if g.area > 0.01))

        subj = MultiPolygon(subj)
        # vsk.geometry(subj)
        # vsk.geometry(back)
        # return

        backl, backr = self.split(back)
        subjl, subjr = self.split(subj)

        backl, backr = backl - subjl, backr - subjr

        tex = MultiLineString(
            [[(x, -11), (x + 16, 11)] for x in np.arange(-32, 32, 0.2)]
        )

        for sign, b, s in [(-0.5, backl, subjl), (0.5, subjr, backr)]:
            with vsk.pushMatrix():
                vsk.translate(sign, sign * 2)

                vsk.geometry(b)
                vsk.geometry(s)
                vsk.geometry(tex & s)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S007Sketch.display()
