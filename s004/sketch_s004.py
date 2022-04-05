import vsketch
import math
import random

import numpy as np
from shapely.geometry import *


class S004Sketch(vsketch.SketchClass):
    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        polys = []

        xs = [x for x in range(0, 10, 2) if vsk.random(1) > 0.3]
        random.shuffle(xs)

        vsk.line(-2, 22, 12, 22)

        for cx in xs:
            l, t, r, b = cx - 2, 22 - vsk.random(5, 8), cx + 2, 22

            t1, t0 = vsk.random(0.2, 0.3), vsk.random(0.7, 0.8)
            t2, t3 = vsk.random(0.3, 0.5), vsk.random(0.3, 0.5)
            t4 = vsk.random(0.4, 0.6)

            b0 = (vsk.lerp(l, r, t0), b)
            b1 = (vsk.lerp(l, r, t1), b)
            l0 = (l, vsk.lerp(b, t, t2))
            t0 = (vsk.lerp(l, r, t4), t)
            r0 = (r, vsk.lerp(b, t, t3))

            p = Polygon([b0, b1, l0, t0, r0])

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

            for pp in polys:
                p -= pp
                if p.is_empty or not p.is_valid:
                    break
            else:
                vsk.geometry(p)
                vsk.geometry(MultiLineString(tex) & p)
                polys.append(p)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S004Sketch.display()
