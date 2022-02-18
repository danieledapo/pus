from locale import normalize
import vsketch
import random
import math

import numpy as np
from shapely.geometry import *


def lerp_seg(a, b, t, normalize=True):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l = math.sqrt(dx**2 + dy**2)
    if normalize:
        dx, dy = dx / l, dy / l

    return a[0] + t * dx, a[1] + t * dy


class S18022022Sketch(vsketch.SketchClass):
    flip = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        vsk.scale(1, -1)

        x0, x1 = 4, 10
        yl, yr = 0, 0

        quads = []

        while yl < 26 and yr < 26:
            dyl = random.randrange(2, 6)
            dyr = dyl + random.randrange(1, 2)

            q = [
                (x0, yl),
                (x0, min(yl + dyl, 26)),
                (x1, min(yr + dyr, 26)),
                (x1, yr),
            ]
            quads.append(q)
            yl, yr = yl + dyl, yr + dyr

            s = 1 if len(quads) % 2 == 0 else -1
            s *= vsk.random(0.3, 1.3)

            x0, yl = lerp_seg(q[1], q[2], -s)
            if self.flip:
                x1, yr = lerp_seg(q[2], q[1], -s)
            else:
                x1, yr = lerp_seg(q[2], q[1], s)

        for i, q in enumerate(quads):
            vsk.polygon(q, close=True)

            xl, y0 = q[0]
            _, y1 = q[1]

            lines = []
            for y in np.arange(y0, y1, 0.05):
                lines.append(LineString([(xl, y), (xl + vsk.random(0.3, 0.8), y)]))

            vsk.geometry(MultiLineString(lines) & Polygon(q))

            for y in np.arange(y1, y1 + 0.5, 0.05):
                l = LineString([(xl, y), (xl + 3, y)]) & Polygon(q)
                if l.is_empty:
                    continue
                p0, _ = l.coords
                vsk.line(p0[0], y, p0[0] + vsk.random(0.3, 0.8), y)

            vsk.strokeWeight(5)
            t = 1 - i / len(quads)
            t = vsk.random(max(0.1, t - 1 / len(quads)), t)

            vsk.line(*q[0], *lerp_seg(q[0], q[3], t, normalize=False))
            vsk.line(*q[1], *lerp_seg(q[1], q[2], t, normalize=False))

            vsk.strokeWeight(1)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    D18022022Sketch.display()
