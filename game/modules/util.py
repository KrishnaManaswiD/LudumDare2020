""" toolbox of useful functions like math etc"""

import math


# returns distance between pointA and pointB
def distance(pointA = (0,0), pointB = (0,0)):
    return math.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)


# returns the point of intersection of the two circles
def circles_intersection(xA, yA, rA, xB, yB, rB):
    k = xA*xA - xB*xB +yA*yA -yB*yB -rA*rA + rB*rB
    c = 0.5* k / (yA - yB)
    m = (xA - xB) / (yB - yA)
    g = c - yA
    A = 1 + m*m
    B = 2*m*g - 2*xA
    C = xA*xA + g*g - rA*rA
    xI = 0.5 * (-B + math.sqrt(B*B - 4*A*C) ) / A
    yI = m*xI + c
    return [xI, yI]


# polygon intersection code from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Given three collinear points p, q, r, the function checks if point q lies on line segment 'pr'
def on_segment(p, q, r):
    if (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Colinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

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


# The main function that returns true if the line segment 'p1q1' and 'p2q2' intersect.
def do_intersect(p1, q1, p2, q2):
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


def is_inside_polygon(polygon, p):
    """
    returns True is p is inside the polygon
    polygon - set of vertices stored as a list of Points
    p - the test point
    """
    n = len(polygon)
    if n < 3:
        return False # polygon should have at least three vertices

    # create a point at the right most end of the screen
    end = Point(1000, p.y)
    intersections = 0 # counter for number of intersections
    i = 0
    while True:
        j = (i+1)%n
        # check if segment from p to end, intersects with polygon[i] to polygon[j]
        if do_intersect(polygon[i],polygon[j],p,end):
            # if p is collinear with polygon[i] to polygon[j], check if it lies on the segment
            if orientation(polygon[i], p, polygon[j]) == 0:
                return on_segment(polygon[i], p, polygon[j])

            intersections+=1
        i = j
        if i == 0:
            break
    # return True if count is even, else False
    return intersections&1