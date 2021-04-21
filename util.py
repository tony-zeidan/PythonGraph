from math import radians, degrees, sin, cos, asin, acos, sqrt
from h3 import h3


def great_circle(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    try:
        return 6371 * (
            acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
        )
    except:
        print(lat1, lon1, lat2, lon2)


def dist_to_spherical(point1, point2):
    return h3.point_dist((point1.x, point1.y), (point2.x, point2.y))
