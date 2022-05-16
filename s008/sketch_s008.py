import vsketch

import math

import numpy as np
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import *


class S008Sketch(vsketch.SketchClass):
    def flow(self, freq: float, thick: float, rounding: float) -> MultiLineString:
        vsk = self.vsk

        ampl = vsk.random(0.1, 0.3)

        counts = {}
        lines = []
        for y0 in np.arange(0, 18, thick):
            for x0 in np.arange(0, 15, thick):
                line = [(x0, y0)]
                for _ in range(100):
                    x, y = line[-1]
                    xt, yt = x / 15, y / 18
                    a = vsk.noise(xt * freq, yt * freq) * math.tau
                    a = math.radians(math.degrees(a) // rounding * rounding)
                    x += math.cos(a) * ampl
                    y += math.sin(a) * ampl

                    k = int(round(x * 10)), int(round(y * 10))
                    c = counts.get(k, 0)
                    if c < 2:
                        counts[k] = c + 1
                    else:
                        break

                    if 0 <= x <= 15 and 0 <= y <= 18:
                        line.append((x, y))
                    else:
                        break

                if len(line) > 1:
                    lines.append(line)

        return MultiLineString(lines)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")

        freq = vsk.random(7, 10)

        container = box(0, 0, 13, 18)
        subject = Point(6.5, 9).buffer(5)

        rounding = int(vsk.random(1, 9) * 10)

        lines1 = self.flow(freq, 0.60, rounding) & container
        lines2 = self.flow(freq, 0.25, rounding) & container

        vsk.geometry(container)
        vsk.geometry(lines1 - subject)
        vsk.geometry(lines2 & subject)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S008Sketch.display()
