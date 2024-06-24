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
    # fig = figure(figsize=(width, height))
    # ax = fig.add_subplot(111, aspect='equal')
    fig, ax = plt.subplots()
    plt.suptitle('Simulation', size='x-large')

    ax.xmin = xmin
    ax.xmax = xmax
    ax.ymin = ymin
    ax.ymax = ymax
    clear(ax)
    return fig, ax


def init_table2(data, legend, xmin, xmax, ymin, ymax, text_size=11, length=4, width=2):
    fig, ax = plt.subplots()
    plt.suptitle('Active rules of the sea', size='x-large')
    table = plt.table(cellText=data, loc='center')
    legend_table = plt.table(cellText=legend, loc='bottom')

    table.auto_set_font_size(False)
    table.set_fontsize(text_size)

    # Colouring of specific boxes
    cell_colors = []
    for row in range(len(data)):
        current_row = []
        for col in range(len(data[row])):
            if (row, col) == (0, 0):  # condition to color the box
                current_row.append('lightgray')
            else:
                current_row.append('white')
        cell_colors.append(current_row)

    for row in range(len(data)):
        for col in range(len(data[row])):
            table[row, col].set_facecolor(cell_colors[row][col])

    ax.xmin = xmin
    ax.xmax = xmax
    ax.ymin = ymin
    ax.ymax = ymax
    clear(ax)
    ax.axis('off')
    fig.tight_layout()
    return fig, ax, table

def init_table(rules, legend,fig,ax, text_size=11, length=4, width=2):
    #fig, ax = plt.subplots()
    # fig, ax = plt.subplots(figsize=(3, 0.5))
    plt.suptitle('Active rules of the sea', size='x-large')
    table = plt.table(cellText=rules, loc='center')
    legend_table = plt.table(cellText=legend, loc='bottom')

    # # Modification du style de la première colonne
    # first_column_cells = [table.get_celld()[row, 0] for row in range(len(data))]
    # for cell in first_column_cells:
    #     cell.set_width(length * 1.2)  # Double la largeur de la première colonne

    table.auto_set_font_size(False)
    table.set_fontsize(text_size)
    # table.scale(length, width)
    # table.scale(0.3, 0.3)
    # ax.xmin = xmin
    # ax.xmax = xmax
    # ax.ymin = ymin
    # ax.ymax = ymax
    # Colouring of specific boxes
    cell_colors = []
    for row in range(len(rules)):
        current_row = []
        for col in range(len(rules[row])):
            if (row, col) == (row, 0):  # Condition pour les cases à colorer
                current_row.append('lightgray')
            else:
                current_row.append('white')
        cell_colors.append(current_row)

    for row in range(len(rules)):
        for col in range(len(rules[row])):
            table[row, col].set_facecolor(cell_colors[row][col])

    ax.axis('off')
    fig.tight_layout()
    # plt.subplots_adjust(left=0.7, top=0.3)

    return table

def clear(ax):
    pause(0.001)
    ax.cla()
    ax.set_xlim(ax.xmin, ax.xmax)
    ax.set_ylim(ax.ymin, ax.ymax)


def draw_arrow(ax, x, y, θ, L, col='darkblue', w=1):
    plot2D(ax, tran2H(x, y) @ rot2H(θ) @ arrow2H(L), col, w)


def draw_boat_and_vector(ax, x, col='darkblue', r=0.1, w=2):
    """ Draw a boat with his speed vector """
    mx, my, v, θ = list(x[0:4, 0])
    M = r * array([[-1, 5, 7, 7, 5, -1, -1, -1], [-2, -2, -1, 1, 2, 2, -2, -2]])
    M = add1(M)
    draw_arrow(ax, mx, my, θ, norm(v), 'red')
    plot2D(ax, tran2H(mx, my) @ rot2H(θ) @ M, col, w)


def draw_field_around_c(ax, f, xmin, xmax, ymin, ymax, a, c):
    """ Draw field with the parameter c """
    Mx = arange(xmin, xmax, a)
    My = arange(ymin, ymax, a)
    X1, X2 = meshgrid(Mx, My)
    VX, VY = f(X1, X2, c)
    R = sqrt(VX ** 2 + VY ** 2)
    ax.quiver(Mx, My, VX / R, VY / R)


def draw_field_around_c_new(ax, f, xmin, xmax, ymin, ymax, a, c, D, k, r):
    """ Draw field with the parameter c """
    Mx = arange(xmin, xmax, a)
    My = arange(ymin, ymax, a)
    X1, X2 = meshgrid(Mx, My)
    VX, VY = f(X1, X2, c, D, k, r)
    R = sqrt(VX ** 2 + VY ** 2)
    ax.quiver(Mx, My, VX / R, VY / R)


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