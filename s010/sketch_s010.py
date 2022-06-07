import math
import vsketch

import numpy as np

from shapely.geometry import *


class Field:
    def __init__(self, charges: list[tuple[float, float, float]], resolution=200):
        self.resolution = resolution
        self.charges = charges

        self.grid = []
        for y in range(resolution + 1):
            row = []
            for x in range(resolution + 1):
                u, v = x / resolution, y / resolution

                dx, dy = 0, 0
                for cx, cy, cv in charges:
                    ll = math.hypot(cx - u, cy - v) or 1
                    dx += (cx - u) * cv / (ll * ll)
                    dy += (cy - v) * cv / (ll * ll)
                l = math.hypot(dx, dy) or 1
                dx, dy = dx / l, dy / l
                row.append((dx, dy))

            self.grid.append(row)

    def get(self, u: float, v: float) -> tuple[float, float]:
        assert 0 <= u <= 1, u
        assert 0 <= v <= 1, v
        x, y = int(u * self.resolution), int(v * self.resolution)
        return self.grid[y][x]


class S011Sketch(vsketch.SketchClass):
    step = vsketch.Param(1.0, 0.001)
    maxlen = vsketch.Param(50, 1)
    charges_min_dist = vsketch.Param(1.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")

        charges = [
            (0.45, 0.5, -100),
            (0.55, 0.5, +100),
            # (0.45, 0.50, +100),
            # (0.55, 0.50, +100),
            # (0.50, 0.35, -100),
            # (0.50, 0.65, -10),
        ]

        ncharges = int(vsk.random(1, 3)) * 2
        charges = []
        while len(charges) != ncharges:
            x, y = vsk.random(0.1, 0.9), vsk.random(0.1, 0.9)

            if (
                charges
                and min((math.hypot(x - xx, y - yy) for xx, yy, _ in charges))
                < self.charges_min_dist / 18
            ):
                continue

            v = vsk.random(1, 20) * 5 * (1 if len(charges) % 2 == 0 else -1)
            charges.append((x, y, v))

        field = Field(charges, resolution=400)

        # vsk.stroke(2)
        # for y in np.arange(0, 18, 0.2):
        #     for x in np.arange(0, 13, 0.2):
        #         dx, dy = field.get(x / 13, y / 18)
        #         vsk.point(x, y)
        #         vsk.line(x, y, x + dx * 0.2, y + dy * 0.2)

        # for cx, cy, _ in charges:
        #     vsk.circle(cx * 13, cy * 18, 1)
        # vsk.stroke(1)
        vsk.fill(1)

        existing = Point(-100, -100).buffer(0.1)

        for y0 in np.arange(0, 18, self.step):
            for x0 in np.arange(0, 13, self.step):
                l = [(x0, y0)]
                while len(l) < self.maxlen:
                    x, y = l[-1]
                    dx, dy = field.get(x / 13, y / 18)
                    x, y = x + dx * 0.1, y + dy * 0.1

                    if 0 <= x <= 13 and 0 <= y <= 18:
                        l.append((x, y))
                        continue
                    break

                # vsk.polygon(l)
                if len(l) < 2:
                    continue

                l = LineString(l).buffer(0.01) - existing
                if not l.is_valid or l.is_empty:
                    continue
                vsk.geometry(l)
                existing |= l.buffer(
                    0.2, join_style=JOIN_STYLE.mitre, cap_style=CAP_STYLE.flat
                )

        vsk.vpype("squiggles")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S011Sketch.display()
