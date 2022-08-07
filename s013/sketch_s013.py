# My entry for WCC: Origami
#
# I started trying to simulate folds "accurately", but eventually I gave up
# because it's quite hard :).
#
# However, the folding transformation should be mostly ok, the thing I haven't
# had time to figure out is which folds are physically possible and which are
# not, but it's fine.
#
# The two textures are meant to distinguish the two sides of the paper, but
# they're not enough to convey the sense of depth, oh well.
#
# The sketch is just a series of random folds on a rectangular sheet of paper
# and sometimes something interesting comes out, mostly paper planes and
# newspaper hats :).

import vsketch

import itertools
import random
import numpy as np

from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from shapely.validation import *


def fold(geo, a):
    geo = rotate(geo, -a, origin=(0, 0), use_radians=True)
    geo = scale(geo, 1, -1, origin=(0, 0))
    geo = rotate(geo, a, origin=(0, 0), use_radians=True)
    return roundShape(geo)


class S013Sketch(vsketch.SketchClass):
    n = vsketch.Param(8, 0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        polys = [(box(-6, -10, 6, 10), 0)]
        texture = [
            MultiLineString([[(x, -15), (x + 10, 15)] for x in np.arange(-15, 15, 0.3)])
        ]
        p = Point(0, 0).buffer(0.4).exterior & box(-100, -100, 100, 0)
        texture2 = [
            MultiLineString([[(-15, y), (15, y)] for y in np.arange(-15, 15, 0.1)])
        ]

        for _ in range(self.n):
            a = np.radians(random.randrange(0, 360, 5))
            x0, y0 = 15 * np.cos(a), 15 * np.sin(a)
            x1, y1 = -x0, -y0

            left, right = [], []
            ltexs, rtexs = [], []
            ltexs2, rtexs2 = [], []
            for (poly, ti), text, text2 in zip(polys, texture, texture2):
                parts = split(poly, LineString([(x0, y0), (x1, y1)]))

                for p in parts.geoms:
                    c = p.centroid
                    d = (c.x - x0) * (y1 - y0) - (c.y - y0) * (x1 - x0)
                    if d <= 0:
                        left.append((p, ti))
                        ltexs.append(text & p)
                        ltexs2.append(text2 & p)
                    else:
                        p = fold(p, a)
                        right.append((p, ti ^ 1))

                        rtexs.append(fold(text, a))
                        rtexs[-1] &= p

                        rtexs2.append(fold(text2, a))
                        rtexs2[-1] &= p

            if not left or not right:
                continue

            polys = list(itertools.chain(left, reversed(right)))
            texture = list(itertools.chain(ltexs, reversed(rtexs)))
            texture2 = list(itertools.chain(ltexs2, reversed(rtexs2)))

        drawn = Point()
        for (p, ti), t, t2 in zip(polys, texture, texture2):

            p -= drawn

            if not p.is_valid or p.is_empty:
                continue

            p = roundShape(p).buffer(0)
            drawn |= p

            vsk.geometry(p)
            tex = t if ti == 0 else t2
            tex &= p

            if hasattr(tex, "geoms"):
                tex = type(tex)(
                    [g for g in tex.geoms if not isinstance(g, (Point, MultiPoint))]
                )

            vsk.geometry(tex)

        vsk.vpype("layout -m 2cm a4")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


def roundShape(geo):
    if isinstance(geo, Point):
        if geo.is_empty:
            return Point()
        return Point(round(geo.x, 6), round(geo.y, 6))

    if isinstance(geo, (LineString, LinearRing)):
        ls = LineString([(round(x, 6), round(y, 6)) for x, y in geo.coords])
        return make_valid(ls)

    if isinstance(geo, Polygon):
        e = roundShape(geo.exterior)
        if len(e.coords) < 3:
            return e
        p = Polygon(e.coords, [roundShape(i).coords for i in geo.interiors])
        return p.buffer(0)

    if isinstance(geo, (MultiPolygon, MultiLineString, MultiPoint, GeometryCollection)):
        ps = []
        for p in geo.geoms:
            pp = roundShape(p)
            if hasattr(pp, "geoms"):
                ps.extend(pp.geoms)
            else:
                ps.append(pp)
        return make_valid(GeometryCollection(ps))

    print(type(geo))
    assert False


if __name__ == "__main__":
    S013Sketch.display()
