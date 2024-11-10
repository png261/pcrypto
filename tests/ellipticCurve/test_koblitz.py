from pcrypto.ellipticCurve import Koblitz
import random
from pcrypto.ellipticCurve.domain import CurveDomainParamter


def test_pipline():
    message = "Hello, Elliptic Curve Cryptography! " * 10
    curve_name = random.choice(CurveDomainParamter.list())
    encoded_points, scale_factor = Koblitz.encode(
        message=message, curve_name=curve_name
    )
    decoded_message = Koblitz.decode(encoded_points, scale_factor)
    assert decoded_message == message
