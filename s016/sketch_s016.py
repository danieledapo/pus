# My entry for WCC: Kandinsky
#
# This is a monochrome sketch "loosely inspired" by "Trente" and in general by
# Kandisky's black and white pieces.
#
# I tried to focus on having a good enough balance between black and white using
# only 2 triangles, circles and lines.
#
# I didn't have much time this week for coding nor plotting, but hopefully I'll
# be plotting during the stream :D.
#


import math
import random
import vsketch

from shapely.geometry import *
from shapely.affinity import *


def unit(x, y):
    l = math.hypot(x, y)
    dx, dy = x / l, y / l
    return dx, dy


class S016Sketch(vsketch.SketchClass):
    padding = vsketch.Param(2)
    maxr = vsketch.Param(1.2)
    linemargin = vsketch.Param(1)
    tripadding = vsketch.Param(0)

    def viewbox(self):
        return box(self.padding, self.padding, 15 - self.padding, 21 - self.padding)

    def randp(self, margin=0, box=None):
        if box is None:
            l, t, r, b = self.viewbox().bounds
        else:
            l, t, r, b = box.bounds
        x = self.vsk.random(l + margin, r - margin)
        y = self.vsk.random(t + margin, b - margin)
        return (x, y)

    def randtri(self, q: Polygon, boundary: MultiLineString):
        tris = None
        for minarea, maxa, fill in [(7, 30, False), (32, 8, True)]:
            for _ in range(3000):
                x0, y0 = self.randp(margin=self.tripadding, box=q)
                x1, y1 = self.randp(margin=self.tripadding, box=q)
                l = math.hypot(x0 - x1, y0 - y1)

                a = math.atan2(y1 - y0, x1 - x0)
                a += random.choice([1, -1]) * math.radians(self.vsk.random(10, maxa))
                x2, y2 = x0 + l * math.cos(a), y0 + l * math.sin(a)

                tri = Polygon([(x0, y0), (x1, y1), (x2, y2)])

                if not q.contains(tri):
                    continue

                if tri.area < q.area / minarea:
                    continue

                # if tri.distance(boundary) < 0.5:
                #     continue

                if fill:
                    self.vsk.fill(1)
                else:
                    lr = LineString([(x0, y0), (x2, y2)])
                    dx, dy = unit(x2 - x1, y2 - y1)
                    for ii in range(random.randrange(2, 6)):
                        off = 0.1 * (ii + 1)
                        tri |= translate(lr, dx * off, dy * off)

                tris = tri if tris is None else tri | tris

                self.vsk.strokeWeight(2)
                self.vsk.geometry(tri)
                self.vsk.strokeWeight(1)
                self.vsk.noFill()
                break
        return tris

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a5", landscape=False)
        vsk.scale("cm")
        vsk.penWidth("0.2mm")

        ox = self.padding + self.linemargin * vsk.random(1, 5)
        if vsk.random(1) > 0.5:
            ox = 15 - ox

        oy = self.padding + self.linemargin * vsk.random(1, 5)
        if vsk.random(1) > 0.5:
            oy = 21 - oy

        frame = [
            [(self.padding, oy), (15 - self.padding, oy)],
            [(ox, self.padding), (ox, 21 - self.padding)],
        ]

        frame = MultiLineString(frame)
        # debug view
        vsk.strokeWeight(2)
        # vsk.geometry(frame)
        vsk.strokeWeight(1)

        quads = [
            box(self.padding, self.padding, ox, oy),
            box(ox, self.padding, 15 - self.padding, oy),
            box(self.padding, oy, ox, 21 - self.padding),
            box(ox, oy, 15 - self.padding, 21 - self.padding),
        ]
        quads.sort(key=lambda b: b.area, reverse=True)

        tris = self.randtri(quads[0] | quads[1], frame)

        hasp = False
        for _ in range(1000):
            fx, fy = self.randp(margin=self.maxr, box=quads[0])
            fr = vsk.random(1, self.maxr)

            point = Point(fx, fy).buffer(fr)

            if point.distance(frame) < 1:
                continue

            if tris and point.distance(tris) < 1.5:
                continue

            vsk.fill(1)
            vsk.geometry(point)
            vsk.noFill()
            hasp = True
            break

        decs = Point()
        if vsk.random(1) > 0.0:
            q = quads[-1]
            l, t, r, b = q.bounds
            w, h = r - l, b - t
            c = self.viewbox().centroid

            ox = l if abs(l - c.x) < abs(r - c.x) else r
            oy = t if abs(t - c.y) < abs(b - c.y) else b

            divx, divy = 1, 1
            ar = w / h
            if abs(ar - 1) > 0.3:
                for _ in range(3):
                    if ar < 1:
                        divy += 1
                    else:
                        divx += 1
                    ar = (w / divx) / (h / divy)
                    if abs(ar - 1) < 0.3:
                        break

            x0, y0 = l + w / divx / 2, t + h / divy / 2
            fill = random.choice([True, False])
            for j in range(divy):
                for i in range(divx):
                    x = x0 + i / divx * w
                    y = y0 + j / divy * h
                    rad = min(w / divx, h / divy) * 0.35

                    if not hasp:
                        if fill:
                            vsk.fill(1)
                        else:
                            vsk.noFill()
                        decs |= Point(x, y).buffer(rad)
                        vsk.circle(x, y, radius=rad)
                    else:
                        if fill:
                            for i in range(3):
                                decs |= Point(x, y).buffer(rad)
                                vsk.circle(x, y, radius=rad)
                                rad -= 0.1
                        else:
                            rad -= 0.1 * 4
                            for i in range(3):
                                decs |= Point(x, y).buffer(rad)
                                vsk.circle(x, y, radius=rad)
                                rad += 0.1
                    fill = not fill
            vsk.noFill()

        drawn = decs.buffer(1, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre)
        if hasp:
            drawn |= point.buffer(
                0.5, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.bevel
            )
        if tris:
            drawn |= tris.buffer(
                0.5, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.bevel
            )

        boxes = [quads[1], quads[2], quads[0] | quads[1], quads[0] | quads[2]]
        for q in boxes:
            l, t, r, b = q.bounds
            w, h = r - l, b - t

            lines = []

            if vsk.random(1) > 0.25:
                y = h * vsk.random(0.1, 0.3)
                s = 1
                if vsk.random(1) > 0.5:
                    y = b - y
                    s = -1
                else:
                    y += t

                pad = 0.1
                x0, x1 = l + w * pad, r - w * pad

                for i in range(10):
                    yy = y + 0.3 * s * i
                    if yy < t + h * 0.1 or yy > t + h * 0.9:
                        break
                    lines.append([(x0, yy), (x1, yy)])

            if vsk.random(1) > 0.25:
                x = w * vsk.random(0.1, 0.3)
                s = 1
                if vsk.random(1) > 0.5:
                    x = r - x
                    s = -1
                else:
                    x += l

                pad = 0.1
                y0, y1 = t + h * pad, b - h * pad

                for i in range(10):
                    xx = x + 0.3 * s * i
                    if xx < l + w * 0.1 or xx > l + w * 0.9:
                        break
                    lines.append([(xx, y0), (xx, y1)])

            lines = MultiLineString(lines) - drawn
            drawn |= lines.buffer(1)
            vsk.geometry(lines)

        vsk.vpype("layout -m 2cm a5")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("color black linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    S016Sketch.display()
