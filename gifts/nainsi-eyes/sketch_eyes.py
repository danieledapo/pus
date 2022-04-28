import vsketch
import math

from shapely.geometry import *
from shapely.ops import *
from shapely.affinity import *


class EyesSketch(vsketch.SketchClass):
    postcard = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        if self.postcard:
            vsk.size("a5", landscape=False)
            vsk.scale(0.71, 0.71)
        else:
            vsk.size("a4", landscape=False)

        vsk.scale("cm")

        vsk.penWidth("1.0mm")

        eye_height = 4
        pupil_height = 1.5
        reflection_height = 0.7
        padding = 2
        eyes_radius = eye_height + padding

        def draw_eyes(a=0):
            # vsk.circle(0, 0, eyes_radius, mode="radius")
            for dx in (-eyes_radius / 2, eyes_radius / 2):
                with vsk.pushMatrix():
                    vsk.translate(dx, 0)
                    # vsk.circle(0, 0, eye_height, mode="radius")
                    vsk.scale(0.5, 1.0)

                    eye = Point(0, 0).buffer(eye_height)
                    vsk.geometry(eye)

                    pupil = Point(0, 0).buffer(pupil_height)
                    pupil -= Point(
                        reflection_height * math.cos(-math.radians(40)),
                        reflection_height * math.sin(-math.radians(40)),
                    ).buffer(reflection_height)

                    pupil = translate(
                        pupil,
                        (eye_height - pupil_height) * math.cos(a),
                        (eye_height - pupil_height) * math.sin(a),
                    )

                    vsk.fill(1)
                    vsk.geometry(pupil)
                    vsk.noFill()

        boundary = LinearRing([(-8, -10), (-8, 10), (8, 10), (8, -10)])
        # vsk.geometry(boundary)
        circles = []
        for _ in range(3000):
            x, y = vsk.random(-8, 8), vsk.random(-10, 10)
            r = vsk.random(5, 10)
            r = min(r, boundary.distance(Point(x, y)))
            for c in circles:
                if c.contains(Point(x, y)):
                    break

                r = min(r, c.distance(Point(x, y)))
                if r < 0.5:
                    break
            else:
                circles.append(Point(x, y).buffer(r))

        for c in circles:
            l, t, r, b = c.bounds
            cx, cy = (l + r) / 2, (t + b) / 2
            with vsk.pushMatrix():
                vsk.translate(cx, cy)
                vsk.rotate(vsk.random(math.pi * 2))
                vsk.scale((r - l) / 2 / eyes_radius)
                draw_eyes(vsk.random(math.pi * 2))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    EyesSketch.display()
