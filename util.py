from math import radians, degrees, sin, cos, asin, acos, sqrt
from h3 import h3
from shapely.geometry import Point

def great_circle(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calculates the spherical distance between two coordinates.
    
    :param lon1: Origin longitude
    :type lon1: float
    :param lat1: Origin latitude
    :type lat1: float
    :param lon2: Destination longitude
    :type lon2: float
    :param lat2: Destination latitude
    :type lat2: float
    :return: The spherical distance
    :rtype: float
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    try:
        return 6371 * (
            acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
        )
    except:
        print(lat1, lon1, lat2, lon2)


def dist_to_spherical(point1: Point, point2: Point) -> float:
    """Calculates spherical distance between two shapely points.
    
    :param point1: The origin
    :type point1: Point
    :param point2: The destination
    :type point2: Point
    :return: The spherical distance
    :rtype: float
    """
    return h3.point_dist((point1.x, point1.y), (point2.x, point2.y))
