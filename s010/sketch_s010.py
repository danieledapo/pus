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
    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")

        charges = [
            # (0.45, 0.55, -100),
            # (0.55, 0.45, +100),
            (0.45, 0.50, +100),
            (0.55, 0.50, +100),
            (0.50, 0.35, -100),
            (0.50, 0.65, -10),
        ]

        charges = []
        for i in range(int(vsk.random(2, 10))):
            x, y = vsk.random(0.1, 0.9), vsk.random(0.1, 0.9)
            v = vsk.random(1, 10) * 10 * (1 if i % 2 == 0 else -1)
            charges.append((x, y, v))

        print(len(charges))

        field = Field(charges, resolution=400)

        vsk.stroke(2)
        # for y in np.arange(0, 18, 0.2):
        #     for x in np.arange(0, 13, 0.2):
        #         dx, dy = field.get(x / 13, y / 18)
        #         vsk.point(x, y)
        #         vsk.line(x, y, x + dx * 0.2, y + dy * 0.2)

        # for cx, cy, _ in charges:
        #     vsk.circle(cx * 13, cy * 18, 1)
        vsk.stroke(1)

        counts = {}
        step = 0.5

        for y0 in np.arange(0, 18, step):
            for x0 in np.arange(0, 13, step):
                l = [(x0, y0)]
                while len(l) < 50:
                    x, y = l[-1]
                    dx, dy = field.get(x / 13, y / 18)
                    x, y = x + dx * 0.1, y + dy * 0.1

                    x, y = round(x, 2), round(y, 2)

                    if 0 <= x <= 13 and 0 <= y <= 18:
                        counts[(x, y)] = counts.get((x, y), 0) + 1
                        if counts[(x, y)] >= 2:
                            break
                        l.append((x, y))
                        continue
                    break

                vsk.polygon(l)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S011Sketch.display()
