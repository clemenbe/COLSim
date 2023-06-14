import matplotlib.pyplot as plt
from numpy import mean, pi, cos, sin, sinc, sqrt, tan, arctan, arctan2, tanh, arcsin, arccos, \
    exp, dot, array, log, inf, eye, zeros, ones, inf, size, \
    arange, reshape, vstack, hstack, diag, median, \
    sign, sum, meshgrid, cross, linspace, append, round, trace, rint
from matplotlib.pyplot import *
from matplotlib.cbook import flatten
from numpy.random import randn, rand
from numpy.linalg import inv, det, norm, eig, qr
from scipy.linalg import sqrtm, expm, logm, norm, block_diag

from scipy.signal import place_poles
from mpl_toolkits.mplot3d import Axes3D
from math import factorial
from matplotlib.patches import Ellipse, Rectangle, Circle, Wedge, Polygon, Arc
from matplotlib.collections import PatchCollection


def add1(M):
    M = array(M)
    return vstack((M, ones(M.shape[1])))

def plot2D(M, col='black', w=1):
    plot(M[0, :], M[1, :], col, linewidth=w)

def tran2H(x, y):
    return array([[1, 0, x], [0, 1, y], [0, 0, 1]])


def rot2H(a):
    return array([[cos(a), -sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1]])

def arrow2H(L):
    e = 0.2
    return add1(L * array([[0, 1, 1 - e, 1, 1 - e], [0, 0, -e, 0, e]]))

def sawtooth(x):
    return (x + pi) % (2 * pi) - pi  # or equivalently   2*arctan(tan(x/2))


def geo_scalar_prod(u,v, θu, θv):
    return u*v*cos(θu-θv)


def dist(a,b):
    xa, ya = a[0:2].flatten()
    xb, yb = b[0:2].flatten()
    return sqrt((xb-xa)**2 + (yb-ya)**2)


def f(x, y, v, theta, u, dt):
    x += dt * v * cos(theta)
    y += dt * v * sin(theta)
    v = v + dt * u[0][0]
    theta += dt * u[1][0]
    return np.vstack((x, y, v, theta))


def check_cross_path(future_state_boat, future_state_obstacle, r):
    xa_boat, ya_boat, va_boat, thetaa_boat = future_state_boat[0].flatten()
    xb_boat, yb_boat, vb_boat, thetab_boat = future_state_boat[1].flatten()
    xc_obstacle, yc_obstacle, vc_obstacle, thetac_obstacle = future_state_obstacle[0].flatten()
    xd_obstacle, yd_obstacle, vd_obstacle, thetad_obstacle = future_state_obstacle[1].flatten()
    # Coordinates of the boat+DCPA
    xA = xa_boat - cos(thetaa_boat) * r
    yA = ya_boat - sin(thetaa_boat) * r
    xB = xb_boat - cos(thetab_boat) * r
    yB = yb_boat - sin(thetab_boat) * r
    # Coordinates of the obstacle+DCPA
    xC = xc_obstacle - cos(thetac_obstacle) * r
    yC = yc_obstacle - sin(thetac_obstacle) * r
    xD = xd_obstacle - cos(thetad_obstacle) * r
    yD = yd_obstacle - sin(thetad_obstacle) * r

    # AB and CD segment slope calculation
    slope_AB = (yB - yA) / (xB - xA)
    slope_CD = (yD - yC) / (xD - xC)

    # Check if the segments intersect
    if slope_AB != slope_CD:
        # Segments are not parallel, they may cross

        # Calculation of intersection coordinates (x, y)
        x = (yC - yA + slope_AB * xA - slope_CD * xC) / (slope_AB - slope_CD)
        y = yA + slope_AB * (x - xA)

        # Check if the intersection is inside the segments
        if (xA <= x <= xB or xB <= x <= xA) and (xC <= x <= xD or xD <= x <= xC) and (yA <= y <= yB or yB <= y <= yA) and (yC <= y <= yD or yD <= y <= yC):
            print("The AB and CD segments cross at point ({}, {})".format(x, y))
            return True
        else:
            print("AB and CD segments do not cross")
            return False
    else:
        print("The AB and CD segments are parallel, they do not cross")
        return True



def check_vector_intersection_with_point(x_boat, y_boat, v_boat, theta_boat, x_obstacle, y_obtscle, v_obstacle):
    # Calculate the direction vectors
    v1 = np.array([v_boat * np.cos(theta_boat), v_boat * np.sin(theta_boat)])
    v2 = np.array([v_obstacle * np.cos(x_obstacle), v_obstacle * np.sin(y_obtscle)])

    # Calculate the determinant of the two vectors
    det = v1[0] * v2[1] - v1[1] * v2[0]

    if np.abs(det) < 1e-9:
        # The vectors are parallel or collinear
        return False
    else:
        # Calculate the intersection point
        t1 = (v2[1] * (x_boat - 0) - v2[0] * (y_boat - 0)) / det
        t2 = (v1[1] * (x_boat - 0) - v1[0] * (y_boat - 0)) / det

        # Check if the intersection point is within the range of both vectors
        if 0 <= t1 <= 1 and 0 <= t2 <= 1:
            return True
        else:
            return False


# def check_vector_intersection(v1, theta1, v2, theta2):
#     # Calculate the direction vectors
#     vector1 = np.array([v1 * np.cos(theta1), v1 * np.sin(theta1)])
#     vector2 = np.array([v2 * np.cos(theta2), v2 * np.sin(theta2)])
#
#     # Calculate the determinant of the two vectors
#     det = vector1[0] * vector2[1] - vector1[1] * vector2[0]
#
#     if np.abs(det) < 1e-9:
#         # The vectors are parallel or collinear
#         return False
#     else:
#         # return True
#         # Calculate the intersection point
#         t = (vector2[0] * (0 - vector1[1]) - vector2[1] * (0 - vector1[0])) / det
#         intersection = vector1 + t * vector2
#
#         # Check if the intersection point is within the norms of the vectors
#         if 0 <= t <= 1 and np.linalg.norm(intersection) <= v1 and np.linalg.norm(intersection) <= v2:
#             print('Cross')
#             return True
#         else:
#             return False

# def check_vector_intersection(v1, theta1, v2, theta2):
#     vector1 = np.array([v1 * np.cos(theta1), v1 * np.sin(theta1)])
#     vector2 = np.array([v2 * np.cos(theta2), v2 * np.sin(theta2)])
#
#     det = vector1[0] * vector2[1] - vector1[1] * vector2[0]
#
#     if np.abs(det) < 1e-6:  # Les vecteurs sont parallèles
#         return False
#
#     t = (vector2[0] * vector1[1] - vector2[1] * vector1[0]) / det
#
#     if 0 <= t <= 1:
#         intersection = vector1 + t * vector2
#         return True, intersection
#     else:
#         return False


def check_vector_intersection(mx, my, v1, theta1, nx, ny, v2, theta2):

    vector1 = np.array([v1 * np.cos(theta1), v1 * np.sin(theta1)])
    vector2 = np.array([v2 * np.cos(theta2), v2 * np.sin(theta2)])

    det = vector1[0] * vector2[1] - vector1[1] * vector2[0]

    if np.abs(det) < 1e-6:  # Les vecteurs sont parallèles
        return False

    t = ((my - ny) * vector2[0] - (mx - nx) * vector2[1]) / det
    u = ((my - ny) * vector1[0] - (mx - nx) * vector1[1]) / det

    if 0 <= t <= 1 and 0 <= u <= 1:
        intersection = np.array([mx, my]) + t * vector1
        return True, intersection
    else:
        return False

