from calcul_tools import *
from draw import *

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


# def add1(M):
#     M = array(M)
#     return vstack((M, ones(M.shape[1])))
#
# def plot2D(M, col='black', w=1):
#     plot(M[0, :], M[1, :], col, linewidth=w)
#
# def tran2H(x, y):
#     return array([[1, 0, x], [0, 1, y], [0, 0, 1]])
#
#
# def rot2H(a):
#     return array([[cos(a), -sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1]])
#
# def arrow2H(L):
#     e = 0.2
#     return add1(L * array([[0, 1, 1 - e, 1, 1 - e], [0, 0, -e, 0, e]]))
#
# def sawtooth(x):
#     return (x + pi) % (2 * pi) - pi  # or equivalently   2*arctan(tan(x/2))
#
#
# def geo_scalar_prod(u,v, θu, θv):
#     return u*v*cos(θu-θv)
#
# def dist(a,b):
#     xa, ya = a[0:2].flatten()
#     xb, yb = b[0:2].flatten()
#     return sqrt((xb-xa)**2 + (yb-ya)**2)
#
#
# def init_figure(xmin, xmax, ymin, ymax):
#     fig = figure()
#     ax = fig.add_subplot(111, aspect='equal')
#     ax.xmin = xmin
#     ax.xmax = xmax
#     ax.ymin = ymin
#     ax.ymax = ymax
#     clear(ax)
#     return ax
#
#
# def clear(ax):
#     pause(0.001)
#     cla()
#     ax.set_xlim(ax.xmin, ax.xmax)
#     ax.set_ylim(ax.ymin, ax.ymax)
#
# def draw_arrow(x, y, θ, L, col='darkblue', w=1):
#     plot2D(tran2H(x, y) @ rot2H(θ) @ arrow2H(L), col, w)
#
# def draw_boat_and_vector(x, col='darkblue', r=0.1, w=2):
#     """ Draw a boat with his speed vector """
#     mx, my, v, θ = list(x[0:4, 0])
#     M = r * array([[-1, 5, 7, 7, 5, -1, -1, -1], [-2, -2, -1, 1, 2, 2, -2, -2]])
#     M = add1(M)
#     draw_arrow(mx, my, θ, norm(v), 'red')
#     plot2D(tran2H(mx, my) @ rot2H(θ) @ M, col, w)
#
#
# def draw_field_around_c(ax, f, xmin, xmax, ymin, ymax, a, c):
#     """ Draw field with the parameter c """
#     Mx = arange(xmin, xmax, a)
#     My = arange(ymin, ymax, a)
#     X1, X2 = meshgrid(Mx, My)
#     VX, VY = f(X1, X2, c)
#     R = sqrt(VX ** 2 + VY ** 2)
#     quiver(Mx, My, VX / R, VY / R)
#
#
# def draw_circle(ax, center_x, center_y, radius, color):
#     circle = plt.Circle((center_x, center_y), radius, fill=False, color=color)
#     ax.add_artist(circle)


def Jφ0(p):
    """ Jacobian Matrix of φ0 """
    p1, p2 = p.flatten()
    return array([[-3 * p1 ** 2 - p2 ** 2 + 1, -2 * p1 * p2 - 1],
                  [-2 * p1 * p2 + 1, -3 * p2 ** 2 - p2 ** 2 + 1]])


def dφ(x, c):
    p1, p2, v, θ = x.flatten()
    z = inv(D) @ array([[p1 - c[0,0]], [p2 - c[1,0]]])
    dv = D @ Jφ0(z) @ inv(D) @ array([[cos(θ)], [sin(θ)]])
    return dv.flatten()

def φ0(p1, p2):
    return -(p1 ** 3 + p2 ** 2 * p1 - p1 + p2), -(p2 ** 3 + p1 ** 2 * p2 - p1 - p2)


def φcw(p1, p2, c):
    """ Clockwise vector field """
    Z = D@array([[1, 0], [0, -1]])
    Z_1 = inv(Z)
    z1 = Z_1[0, 0] * (p1 - c[0,0]) + Z_1[0, 1] * (p2 - c[1,0])
    z2 = Z_1[1, 0] * (p1 - c[0,0]) + Z_1[1, 1] * (p2 - c[1,0])
    w1, w2 = φ0(z1, z2)
    v1 = Z[0, 0] * w1 + Z[0, 1] * w2
    v2 = Z[1, 0] * w1 + Z[1, 1] * w2
    return v1, v2


def φccw(p1, p2, c):
    """ Counterclockwise vector field """
    D_1 = inv(D)
    z1 = D_1[0, 0] * (p1 - c[0,0]) + D_1[0, 1] * (p2 - c[1,0])
    z2 = D_1[1, 0] * (p1 - c[0,0]) + D_1[1, 1] * (p2 - c[1,0])
    w1, w2 = φ0(z1, z2)
    v1 = D[0, 0] * w1 + D[0, 1] * w2
    v2 = D[1, 0] * w1 + D[1, 1] * w2
    return v1, v2


def φrep(p1, p2, c):
    """ Vector field repulsing to a circle of radius r and center c"""
    a = k*((p1-c[0,0])**2 + (p2-c[1,0])**2 - r**2)*(p1-c[0,0])
    b = k*((p1-c[0,0])**2 + (p2-c[1,0])**2)**(3/2)
    φ1 = a/b
    c = ((p1 - c[0, 0]) ** 2 + (p2 - c[1, 0]) ** 2 - r ** 2) * (p2 - c[1, 0])
    φ2 = c/b
    return φ1, φ2


def control(x, φ, c):
    dφ1, dφ2 = dφ(x, c)
    x, y, v, θ = x.flatten()
    φ1, φ2 = φ(x, y, c)
    u1 = 0
    u2 = -sawtooth(θ - arctan2(φ2, φ1)) - (φ2 * dφ1 - φ1 * dφ2) / ((φ1 ** 2) + (φ2 ** 2))
    return array([[u1], [u2]])


def f(x,u):
    x,u  = x.flatten(), u.flatten()
    v,θ = x[2],x[3]
    return array([[v*cos(θ)],[v*sin(θ)],[u[0]],[u[1]]])


# TODO : plot initial traj and modifieed

''' Left lower zone '''
# xp = array([[-2.5,-3,1,1]]).T      #x,y,v,θ of the boat
# xq = array([[2,2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right lower zone '''
# xp = array([[5,-6,1.5,2]]).T      #x,y,v,θ of the boat
# xq = array([[0,0,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Left upper zone '''
# xp = array([[-1,2,1,5]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right upper zone '''
# xp = array([[3,3,1,4]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Opposite direction '''
# xp = array([[-1, 3, 1, 4.75]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2, 0.25, 1.75]]).T    #x,y,v,θ of the obstacle boat

xp = array([[400, 300, 2, -1.5]]).T      #x,y,v,θ of the boat
xq = array([[400, 400, 50, 0.8]]).T    #x,y,v,θ of the obstacle boat

# qx, qy = 2, 2
k = 0.5   # constant to determine the repulsion force of the field
r = 2   # DCPA
# c = array([[qx],
#           [qy]])
D = array([[r, 0],
          [0, r]])

dt = 0.05
s = 9
Ɛ = 2
#TODO : remplace Ɛ by two variables, one for the manoeuvring area and one for the
ax = init_figure(-s,s,-s,s)

# # draw_field(ax, φccw, -s, s, -s,  s, 0.51)
# draw_field_rep(ax, φrep, -s, s, -s,  s, 0.51, c)
# draw_circle(ax, c[0,0], c[1,0], r, 'magenta')
# pause(20)

if __name__ == '__main__':
    for t in arange(0, 50, dt):
        clear(ax)
        # xq = array([[1 + 0.1 * t], [1]])
        qx, qy, qv, qθ = xq.flatten()   # obstacle boat
        px, py, pv, pθ = xp.flatten()   # boat
        uq = array([[0], [0]])          # obstacle boat controler
        c = array([[qx],
                [qy]])               # coordinates of the circle representing the obstacle zone to avoid
        scalar_pdt = geo_scalar_prod(qv, pv, qθ, pθ)
        print('scalar_pdt=', geo_scalar_prod(qv, pv, qθ, pθ))

        # Test to check if the boat is close to the obstacle
        if dist(xq, xp) < r+Ɛ :
            # Test to see if the boat have a heading close to the obstacle
            # TODO : affine the precision of the application of the scalar product
            if scalar_pdt >= 0:
                print('------------------Boats with close directions------------------')
                # Tests to find where the boat is compared with the obstacle
                if (py > qy + Ɛ) :
                    # The boat is in the front zone of the obstacle
                    print('------------------Front zone------------------')
                    φ = φrep
                elif (py < qy + Ɛ) & (px < qx) :
                    # The boat is in the left lower zone compared with the obstacle
                    print('------------------Left lower zone------------------')
                    φ = φcw
                else :
                    # The boat is in the right lower zone compared with the obstacle
                    print('------------------Right lower zone------------------')
                    φ = φccw
                up = control(xp, φ, c)
                print('u=', up)
                draw_field_around_c(ax, φ, -s, s, -s, s, 0.51, c)

            else :
                print('------------------Boats in opposite directions------------------')
                # Tests to find where the boat is compared with the obstacle
                if (py > qy - Ɛ):
                    # The boat is in the front zone of the obstacle
                    print('------------------Left front zone------------------')
                    φ = φccw
                    # Boat
                    up = control(xp, φ, c)
                    draw_field_around_c(ax, φ, -s, s, -s, s, 0.51, c)
                elif (py > qy - Ɛ) & (px > qx) & (scalar_pdt < abs(qv*pv)*cos(2.5)):
                    # The boat is in the front zone of the obstacle
                    print('------------------Right front zone (align)------------------')
                    up = array([[0], [0]])
                elif (py > qy - Ɛ) & (px > qx) & (scalar_pdt > abs(qv*pv)*cos(2.5)):
                    # The boat is in the front zone of the obstacle
                    print('------------------Right front zone------------------')
                    φ = φccw
                    # Boat
                    up = control(xp, φ, c)
                    draw_field_around_c(ax, φ, -s, s, -s, s, 0.51, c)
                else:
                    # The boat is in the right lower zone compared with the obstacle
                    print('------------------Lower zone------------------')
                    φ = φrep
                    # Boat
                    up = control(xp, φ, c)
                    draw_field_around_c(ax, φ, -s, s, -s, s, 0.51, c)
                # # Boat
                # up = control(xp, φ, c)
                # print('up=', up)
                # draw_field_around_c(ax, φ, -s, s, -s, s, 0.51, c)
                # # Obstacle boat
                # # uq = control(xq, φ, array([[qx], [qy]]))
                # print('uq=', uq)
                # # draw_field_around_c(ax, φ, -s, s, -s, s, 0.51, array([[qx], [qy]]))


        else :
            up = array([[0], [0]])

        # Euler integration method
        xp = xp + dt * f(xp, up)
        xq = xq + dt * f(xq, uq)
        print('xp=', xp)
        print('xq=', xq)
        draw_boat_and_vector(xp)
        draw_boat_and_vector(xq)
        draw_circle(ax, c[0,0], c[1,0], r, 'red')               # DCPA zone to avoid
        draw_circle(ax, c[0,0], c[1,0], r+Ɛ, 'magenta')         # DCPA zone extended for safety : manoeuvring area

        draw_circle(ax, px, py, r, 'red')








