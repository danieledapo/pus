import vsketch
import math

import numpy as np
from shapely.geometry import *


class S004Sketch(vsketch.SketchClass):
    n = vsketch.Param(70)
    circles = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        polys = []
        types = []

        for j in range(self.n):
            if self.circles and j / self.n > 0.5 and vsk.random(1) > 0.7:
                cx, cy = vsk.random(0, 6), vsk.random(0, 16)
                r = vsk.random(1, 2)
                polys.append(Point(cx, cy).buffer(r))
                polys.append(Point(-cx, cy).buffer(r))
                types.extend((2, 3))
            else:
                cx, cy = vsk.random(0, 6), vsk.random(0, 16)
                tri = []
                for i in range(3):
                    a, r = vsk.random(i / 2 * math.pi * 2), vsk.random(1, 3)
                    tri.append((cx + r * math.cos(a), cy + r * math.sin(a)))

                polys.append(Polygon(tri))
                polys.append(Polygon([(-x, y) for x, y in tri]))
                types.extend((0, 1))

        for i in range(len(polys)):
            tri = polys[i]
            for tt in polys[:i]:
                tri -= tt.buffer(0.2)

            if tri.is_empty or not tri.is_valid:
                continue

            for t in tri.geoms if isinstance(tri, MultiPolygon) else [tri]:
                if t.area < 0.2:
                    continue

                vsk.geometry(t)
                if vsk.random(1) > [0.8, 0.2, 0.2, 0.5][types[i]]:
                    dx = 45 if vsk.random(1) > 0.5 else -45
                    tex = MultiLineString(
                        [
                            [(x, -45), (x + dx, 45)]
                            for x in np.arange(-45, 45, vsk.random(0.1, 0.2))
                        ]
                    )
                    vsk.geometry(tex & t)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S004Sketch.display()
