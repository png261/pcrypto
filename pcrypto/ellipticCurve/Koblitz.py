import multiprocessing
from typing import Tuple
from functools import partial

from pcrypto.ellipticCurve.point import Point
from pcrypto.utils import powermod, encodeString, decodeString
from pcrypto.ellipticCurve.domain import CurveDomainParamter
from pcrypto.ellipticCurve.curve import Curve


def getPointOnCurve(message_decimal: int, curve: Curve, scale_factor: int):
    for j in range(1, scale_factor - 1):
        x = (scale_factor * message_decimal + j) % curve.p
        s = (x**3 + curve.a * x + curve.b) % curve.p

        if s == powermod(s, (curve.p + 1) // 2, curve.p):
            y = powermod(s, (curve.p + 1) // 4, curve.p)

            if curve.on_curve(x, y):
                return Point(curve, x, y)

    raise ValueError("Could not find a valid point on the curve.")


def encodeChunk(
    message: str,
    curve_name: str = "secp521r1",
    scale_factor: int = 100,
    alphabet_size: int = 2**8,
) -> Tuple[Point]:
    curve = CurveDomainParamter.get(curve_name=curve_name)
    message_decimal = encodeString(message, alphabet_size)
    return getPointOnCurve(message_decimal, curve, scale_factor)


def encode(
    message: str,
    curve_name: str = "secp521r1",
    scale_factor: int = 100,
    chunk_size: int = 10,
    alphabet_size: int = 2**8,
) -> Tuple[Tuple[Point], int]:
    with multiprocessing.Pool() as pool:
        encoded_messages = pool.map(
            partial(
                encodeChunk,
                curve_name=curve_name,
                scale_factor=scale_factor,
                alphabet_size=alphabet_size,
            ),
            (message[i : i + chunk_size] for i in range(0, len(message), chunk_size)),
        )

    return encoded_messages, scale_factor


def decodeSinglePoint(
    encoded: Point,
    scale_factor: int = 100,
    alphabet_size: int = 2**8,
) -> str:
    return decodeString(encoded.x // scale_factor)


def decode(
    encoded_points: Tuple[Point],
    scale_factor: int = 100,
    alphabet_size: int = 2**8,
) -> str:
    with multiprocessing.Pool() as pool:
        characters = pool.starmap(
            partial(
                decodeSinglePoint,
                scale_factor=scale_factor,
                alphabet_size=alphabet_size,
            ),
            [(point,) for point in encoded_points],
        )

    return "".join(characters)
