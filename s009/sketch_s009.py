from random import choices
import vsketch

import math
import numpy as np

from shapely.geometry import *
from shapely.affinity import *


class Day25Sketch(vsketch.SketchClass):
    n = vsketch.Param(100)
    base = vsketch.Param("circle", choices=["circle", "line"])

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")

        vsk.noiseDetail(2)
        if self.base == "line":
            freq = vsk.random(1.5, 4)
            xs = np.arange(0, 10, 0.1)
            ys = vsk.noise(xs / 10 * freq) * 20
            subj = LineString(zip(xs, ys))
        elif self.base == "circle":
            phase = vsk.random(1)
            freq = vsk.random(1, 2)

            subj = []
            for a in np.arange(0, 360, 0.5):
                a = math.radians(a)
                x, y = math.cos(a), math.sin(a)
                rr = vsk.noise(x * freq + phase, y * freq + phase) * 10
                subj.append((rr * x, rr * y))
            subj = Polygon(subj)

        vsk.geometry(subj)
        for i in range(self.n):
            subj = scale(subj, 0.9 ** (i / self.n), 1)
            subj = translate(subj, 0, 0.1)
            vsk.geometry(subj)

            l, _, r, _ = subj.bounds
            if r - l < 0.05:
                break

        vsk.vpype("layout -m 2cm a5")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day25Sketch.display()
