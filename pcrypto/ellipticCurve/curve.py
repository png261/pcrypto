from __future__ import annotations
import pcrypto.ellipticCurve.point as point
from typing import Tuple


class Curve(object):
    def __init__(
        self,
        p: int,
        a: int,
        b: int,
        g: Tuple[int, int],
        n: int,
        h: int,
        name="undefined",
    ):
        self.name = name
        self.p = p
        self.a = a
        self.b = b
        self.g = point.Point(self, g[0], g[1])
        self.n = n
        self.h = h

    def is_singular(self) -> bool:
        return (4 * self.a**3 + 27 * self.b**2) % self.p == 0

    def on_curve(self, x, y) -> bool:
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def __eq__(self, other) -> bool:
        if not isinstance(other, Curve):
            return False
        return (
            self.p == other.p
            and self.a == other.a
            and self.b == other.b
            and self.n == other.n
            and self.h == other.h
        )

    def __ne__(self, other) -> point.Point:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return '"%s" => y^2 = x^3 + %dx + %d (mod %d)' % (
            self.name,
            self.a,
            self.b,
            self.p,
        )

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> str:
        return {
            "name": self.name,
            "p": str(self.p),
            "a": str(self.a),
            "b": str(self.b),
            "g": {"x": str(self.g.x), "y": str(self.g.y)},
            "n": str(self.n),
            "h": str(self.h),
            "is_singular": self.is_singular(),
        }
