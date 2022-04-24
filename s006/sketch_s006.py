import vsketch
import math

import numpy as np

from shapely.geometry import *
from shapely.ops import *
from shapely.affinity import *


class S006Sketch(vsketch.SketchClass):
    n = vsketch.Param(3)
    erode = vsketch.Param(0.05, 0)
    threshold = vsketch.Param(0.6, 0, 1)
    clip = vsketch.Param("circle", choices=["circle", "square"])

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        if self.clip == "square":
            shapes = [box(-8, -8, 8, 8)]
        elif self.clip == "circle":
            shapes = [Point(0, 0).buffer(8)]

        for i in range(self.n):
            phase = vsk.random(math.pi * 2)
            y0 = vsk.random(-3, 3)
            freq = vsk.random(2, 4)

            l = []
            for x in np.arange(-10, 10, 0.1):
                xt = (x + 10) / 20
                y = y0 + math.sin(phase + xt * math.pi * freq) * 4
                l.append((x, y))

            if i % 2 == 1:
                l = [(y, x) for x, y in l]

            new_shapes = []
            for s in shapes:
                new_shapes.extend(split(s, LineString(l)).geoms)
            shapes = new_shapes

        shapes = [s.buffer(-self.erode) for s in shapes]

        for g in shapes:
            vsk.geometry(g)

        tex = MultiLineString([[(x, -8), (x + 16, 8)] for x in np.arange(-32, 16, 0.1)])
        total_area = sum((s.area for s in shapes))
        area = 0
        while shapes and area <= total_area * self.threshold:
            i = max(range(len(shapes)), key=lambda i: shapes[i].area)
            shape = shapes.pop(i)
            area += shape.area

            vsk.geometry(tex & shape)

            neighbors = []
            bigshape = shape.buffer(self.erode * 2)
            for j, bs in enumerate(shapes):
                bs = bs.buffer(self.erode * 2)
                intr = bs & bigshape
                if not intr.is_valid or intr.is_empty:
                    continue

                neighbors.append((bs.area * intr.area, j))
            neighbors.sort(reverse=True)
            to_remove = {j for _, j in neighbors[:2]}
            shapes = [s for k, s in enumerate(shapes) if k not in to_remove]

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S006Sketch.display()
