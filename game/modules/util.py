import math
import pyglet

def distance(point_a=(0, 0), point_b=(0, 0)):
    """
    Returns the distance between the two specified points
    :param point_a: One of the points.
    :type point_a: Tuple
    :param point_b: The other point.
    :type point_b: Tuple
    :return: distance between the points
    """
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


# returns the point of intersection of the two circles
def circles_intersection(x_a, y_a, r_a, x_b, y_b, r_b):
    """
    Returns the point of intersection of two circkes
    :param x_a: x coordinate of the center of first circle
    :param y_a: y coordinate of the center of first circle
    :param r_a: radius of first circle
    :param x_b: x coordinate of the center of second circle
    :param y_b: y coordinate of the center of second circle
    :param r_b: radius of second circle
    :return: Array of coordinates of one of the intersection points
    """
    k = x_a*x_a - x_b*x_b + y_a*y_a - y_b*y_b - r_a*r_a + r_b*r_b
    c = 0.5 * k / (y_a - y_b)
    m = (x_a - x_b) / (y_b - y_a)
    g = c - y_a

    aa = 1 + m*m
    bb = 2*m*g - 2*x_a
    cc = x_a*x_a + g*g - r_a*r_a
    xi = 0.5 * (-bb + math.sqrt(bb*bb - 4*aa*cc)) / aa
    yi = m*xi + c
    return [xi, yi]


# polygon intersection code from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

class Point:
    """
    Class that defines a point
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


def on_segment(p, q, r):
    """
    Given three collinear points p, q, r, the function checks if point q lies on line segment 'pr'
    :param p: Point p
    :type p: Point
    :param q: Point q
    :type q: Point
    :param r: Point r
    :type r: Point
    :return: True if points are collinear, else False
    """
    if (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)):
        return True
    return False


def orientation(p, q, r):
    """
    Returns the orientation of an ordered triplet of points (p, q, r).
    :param p: Point p
    :type p: Point
    :param q: Point q
    :type q: Point
    :param r: Point r
    :type r: Point
    :return: 0 if points are collinear, 1 if clockwise and 2 if counterclockwise
    """
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:
        # Clockwise orientation
        return 1
    elif val < 0:
        # Counterclockwise orientation
        return 2
    else:
        # Collinear orientation
        return 0


def do_intersect(p1, q1, p2, q2):
    """
    Checks if two line segments defined by the endpoints p1,q1 and p1,q2 intersect
    :param p1: One end of line segment 1
    :type p1: Point
    :param q1: Other end of line segment 1
    :type q1: Point
    :param p2: One end of line segment 2
    :type p2: Point
    :param q2: Other end of line segment 2
    :type q2: Point
    :return: True if the line segments intersect, else False
    """

    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if (o1 == 0) and on_segment(p1, p2, q1):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if (o2 == 0) and on_segment(p1, q2, q1):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if (o3 == 0) and on_segment(p2, p1, q2):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if (o4 == 0) and on_segment(p2, q1, q2):
        return True

    # If none of the cases
    return False


def is_inside_polygon(p, polygon):
    """
    Checks if a point p is inside a polygon
    :param p: the test point
    :param polygon: set of vertices stored as a list of Points
    :returns: True if p is inside the polygon, else False
    """
    n = len(polygon)
    if n < 3:
        return False     # polygon should have at least three vertices

    # create a point at the right most end of the screen
    end = Point(1000, p.y)
    intersections = 0    # counter for number of intersections
    i = 0
    while True:
        j = (i + 1) % n
        # check if segment from p to end, intersects with polygon[i] to polygon[j]
        if do_intersect(polygon[i], polygon[j], p, end):
            # if p is collinear with polygon[i] to polygon[j], check if it lies on the segment
            if orientation(polygon[i], p, polygon[j]) == 0:
                return on_segment(polygon[i], p, polygon[j])

            intersections += 1
        i = j
        if i == 0:
            break
    # return True if count is even, else False
    return intersections & 1


def get_gl_polygon(vertices):
    num_vertices = len(vertices) // 2
    indices = []
    for i in range(num_vertices-2):
        indices.extend([0,i+1,i+2])
    colours = []
    for i in range(num_vertices):
        colours.extend([0.3,0.0,0.3])
    polygon = pyglet.graphics.vertex_list_indexed(num_vertices, indices, ('v2i', vertices), ('c3f', colours))
    return polygon


def get_points(vertices):
    points = []
    for i in range(0, len(vertices), 2):
        points.append(Point(vertices[i], vertices[i+1]))
    return points
