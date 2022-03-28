import math
import vsketch

import numpy as np
from shapely.geometry import *


class S002Sketch(vsketch.SketchClass):
    n = vsketch.Param(200)
    buf = vsketch.Param(0.2)
    clip = vsketch.Param("none", choices=["none", "circle"])

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        pts = []
        for _ in range(self.n):
            x, y = (vsk.random(2, 14), vsk.random(2, 22))
            pts.append((x, y))

        if self.clip == "none":
            clip = box(0, 0, 28, 24)
        elif self.clip == "circle":
            clip = Point(8, 12).buffer(7)

        tris = []
        for cx, cy in pts:
            r = min([math.hypot(cx - x, cy - y) for x, y in pts if (x, y) != (cx, cy)])
            r = min(r, abs(16 - cx), abs(24 - cy))

            r = vsk.random(2, r)

            ad = vsk.random(math.pi)
            a = ad + vsk.random(0.25, 0.75) * math.pi

            p = (
                Polygon(
                    [
                        (cx + r * math.cos(ad), cy + r * math.sin(ad)),
                        (cx - r * math.cos(ad), cy - r * math.sin(ad)),
                        (cx + r * math.cos(a), cy + r * math.sin(a)),
                    ]
                )
                & clip
            )

            for t in tris:
                p -= t

            if not p.is_valid or p.is_empty:
                continue

            l, t, r, b = p.bounds
            steps = min(20, int((r - l) / 0.05))
            tex = MultiLineString(
                [[(x, -10), (x, 30)] for x in np.linspace(l, r, steps)]
            )

            tex_p = vsk.random(1)
            for g in [p] if isinstance(p, Polygon) else p.geoms:
                if g.area <= 0.1:
                    continue

                vsk.geometry(g)
                if tex_p > 0.6:
                    vsk.geometry(tex & g)

                tris.append(g.buffer(self.buf))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S002Sketch.display()
