import vsketch
import math


class S012Sketch(vsketch.SketchClass):
    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")

        ccs = [
            (0, vsk.random(1, 10), math.radians(vsk.random(360))),
            (0, vsk.random(1, 10), math.radians(vsk.random(360))),
        ]
        ll = []
        for _ in range(360):
            x, y = 0, 0
            for i in range(len(ccs)):
                a, r, da = ccs[i]
                x, y = x + r * math.cos(a), y + r * math.sin(a)
                ccs[i] = (a + da, r, da)
            ll.append((x, y))

        vsk.polygon(ll)

        vsk.vpype("layout -m 2cm a5")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S012Sketch.display()
