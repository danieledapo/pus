import vsketch
import vpype as vp

import io
import math

from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import *


class Day25Sketch(vsketch.SketchClass):
    n = vsketch.Param(50, 1)
    shape = vsketch.Param("circle", choices=["circle", "square", "triangle", "heart"])
    renderer = vsketch.Param(0, 0, 1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")

        if self.shape == "heart":
            shape, w, h = vp.read_svg(
                io.BytesIO(
                    b"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" height="315" width="342">
  <defs>
    <g id="heart">
      <path d="M0 200 v-200 h200      a100,100 90 0,1 0,200     a100,100 90 0,1 -200,0     z"/>
    </g>
  </defs>
  <use xlink:href="#heart" transform="rotate(225,150,121)"/>
</svg>
"""
                ),
                quantization=0.1,
            )
            shape = shape.as_mls()
            shape = scale(shape, 11 / w, 11 / w).buffer(1.5)
            l, t, r, b = shape.bounds
            shape = translate(shape, -(l + r) / 2, -(t + b) / 2)
        elif self.shape == "circle":
            shape = scale(Point(0, 0).buffer(5.5), [1.5, 1][self.renderer], 1)
        elif self.shape == "square":
            shape = box(-6, -6, 6, 6)
        elif self.shape == "triangle":
            shape = Polygon([(-6, 6), (0, -6), (6, 6)])

        l, t, r, b = shape.bounds

        nattractors = int(vsk.random(1, 7))
        attractors = []
        while self.renderer == 1 and len(attractors) != nattractors:
            x, y = vsk.random(l, r), vsk.random(t, b)
            if not shape.contains(Point(x, y)):
                continue
            if (
                not attractors
                or min((math.hypot(a[0] - x, a[1] - y) for a in attractors)) > 2
            ):
                attractors.append((x, y))

        pts = []
        while len(pts) < self.n:
            x, y = vsk.random(l, r), vsk.random(t, b)

            if self.renderer == 0:
                tt = 1 - (y - t) / (b - t)
                if vsk.random(1) < tt**0.1:
                    continue
            else:
                tt = min(
                    (
                        math.hypot((x - cx) / (r - l), (y - cy) / (b - t))
                        for cx, cy in attractors
                    ),
                    default=1,
                )
                if tt < 0.05 or vsk.random(1) < 1 - tt:
                    continue

            pts.append((x, y))

        # vsk.stroke(2)
        # vsk.geometry(MultiPoint(attractors).buffer(0.5))
        # vsk.geometry(MultiPoint(pts))
        # vsk.geometry(shape)
        # return
        # vsk.stroke(1)

        for g in voronoi_diagram(MultiPoint(pts)).geoms:
            g = g & shape
            g = g.buffer(-0.05)
            if not g.is_valid or g.is_empty:
                continue
            g = rotate(g, vsk.random(30))

            if self.renderer == 0:
                ty = (g.centroid.y - t) / (b - t)
                dd = vsk.random(3, 6)
                g = translate(g, 0, dd * ty)
            else:
                dx, dy = 0, 0
                for ax, ay in attractors:
                    ll = math.hypot(ax - g.centroid.x, ay - g.centroid.y)
                    dx += -(ax - g.centroid.x) * ll
                    dy += -(ay - g.centroid.x) * ll
                ll = math.hypot(dx, dy)
                dx, dy = dx / ll, dy / ll

                t = vsk.random(0.5, 1)
                g = translate(g, t * dx, t * dy)

            vsk.geometry(g)

        vsk.vpype("layout -m 2cm a5")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day25Sketch.display()
