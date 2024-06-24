from calcul_tools import *

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


def init_figure(xmin, xmax, ymin, ymax, width=10, height=10):
    fig = figure(figsize=(width, height))
    ax = fig.add_subplot(111, aspect='equal')
    ax.xmin = xmin
    ax.xmax = xmax
    ax.ymin = ymin
    ax.ymax = ymax
    clear(ax)
    return ax


def clear(ax):
    pause(0.001)
    cla()
    ax.set_xlim(ax.xmin, ax.xmax)
    ax.set_ylim(ax.ymin, ax.ymax)


def draw_arrow(x, y, θ, L, col='darkblue', w=1):
    plot2D(tran2H(x, y) @ rot2H(θ) @ arrow2H(L), col, w)


def draw_boat_and_vector(x, col='darkblue', r=0.1, w=2):
    """ Draw a boat with his speed vector """
    mx, my, v, θ = list(x[0:4, 0])
    M = r * array([[-1, 5, 7, 7, 5, -1, -1, -1], [-2, -2, -1, 1, 2, 2, -2, -2]])
    M = add1(M)
    draw_arrow(mx, my, θ, norm(v), 'red')
    plot2D(tran2H(mx, my) @ rot2H(θ) @ M, col, w)


def draw_field_around_c(ax, f, xmin, xmax, ymin, ymax, a, c):
    """ Draw field with the parameter c """
    Mx = arange(xmin, xmax, a)
    My = arange(ymin, ymax, a)
    X1, X2 = meshgrid(Mx, My)
    VX, VY = f(X1, X2, c)
    R = sqrt(VX ** 2 + VY ** 2)
    quiver(Mx, My, VX / R, VY / R)


def draw_field_around_c_new(ax, f, xmin, xmax, ymin, ymax, a, c, D, k, r):
    """ Draw field with the parameter c """
    Mx = arange(xmin, xmax, a)
    My = arange(ymin, ymax, a)
    X1, X2 = meshgrid(Mx, My)
    VX, VY = f(X1, X2, c, D, k, r)
    R = sqrt(VX ** 2 + VY ** 2)
    quiver(Mx, My, VX / R, VY / R)


def draw_circle(ax, center_x, center_y, radius, color):
    circle = plt.Circle((center_x, center_y), radius, fill=False, color=color)
    ax.add_artist(circle)


def draw_disk(ax, c, r, col, alph=0.7, w=1):
    # draw_disk(ax,array([[1],[2]]),0.5,"blue")
    e = Ellipse(xy=c, width=2 * r, height=2 * r, angle=0, linewidth=w)
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    e.set_alpha(alph)  # transparency
    e.set_facecolor(col)