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
        if (xA <= x <= xB or xB <= x <= xA) and (xC <= x <= xD or xD <= x <= xC):
            print("The AB and CD segments cross at point ({}, {})".format(x, y))
            return True
        else:
            print("AB and CD segments do not cross")
            return False
    else:
        print("The AB and CD segments are parallel, they do not cross")
        return True