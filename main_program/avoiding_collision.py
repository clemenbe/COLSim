from calcul_tools import *
from draw import *


def Jφ0(p):
    """ Jacobian Matrix of φ0 """
    p1, p2 = p.flatten()
    return array([[-3 * p1 ** 2 - p2 ** 2 + 1, -2 * p1 * p2 - 1],
                  [-2 * p1 * p2 + 1, -3 * p2 ** 2 - p2 ** 2 + 1]])

def dφ(x):
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
    dφ1, dφ2 = dφ(x)
    x, y, v, θ = x.flatten()
    φ1, φ2 = φ(x, y, c)
    u1 = 0
    u2 = -sawtooth(θ - arctan2(φ2, φ1)) - (φ2 * dφ1 - φ1 * dφ2) / ((φ1 ** 2) + (φ2 ** 2))
    return array([[u1], [u2]])


def f(x,u):
    x,u  = x.flatten(), u.flatten()
    v,θ = x[2],x[3]
    return array([[v*cos(θ)],[v*sin(θ)],[u[0]],[u[1]]])



''' Left lower zone '''
xp = array([[-2.5,-5,1.5,1]]).T      #x,y,v,θ of the boat
xq = array([[2,0,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right lower zone '''
# xp = array([[5,-6,1.5,2]]).T      #x,y,v,θ of the boat
# xq = array([[0,0,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Left upper zone '''
# xp = array([[-1,2,1.5,5]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right upper zone '''
# xp = array([[3,3,1.5,4]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Opposite direction '''
# xp = array([[-1, 3, 1.5, 4.75]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2, 0.25, 1.75]]).T    #x,y,v,θ of the obstacle boat

# xp = array([[3, 3, 1.5, 4.75]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2, 0.25, 1.75]]).T    #x,y,v,θ of the obstacle boat



k = 0.5     # constant to determine the repulsion force of the field
r = 2       # DCPA
D = array([[r, 0],
          [0, r]])

dt = 0.05   # step of the simulation
s = 9       # size of  the simulation figure
Ɛ = 2       # radius added to the dangerous zone
#TODO : remplace Ɛ by two variables, one for the manoeuvring area and one for the
ax = init_figure(-s,s,-s,s)
px0, py0 = -2.5, -5
Lx = [px0]
Ly = [py0]



for t in arange(0, 50, dt):
    clear(ax)

    qx, qy, qv, qθ = xq.flatten()   # obstacle boat
    px, py, pv, pθ = xp.flatten()   # boat

    c = array([[qx], [qy]])         # coordinates of the circle representing the obstacle zone to avoid

    # Instructions
    vhat = array([[1], [1]])        # desired acceleration and angular speed
    phat = array([[7.5], [8]])      # coordinates for the final destination of the boat
    qhat = array([[-2.5], [8]])     # coordinates for the final destination of the obstacle boat

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

    else :
        # Control commande to reach the final destination if there is no risk of collision
        wp = vhat - 2 * (array([[px], [py]]) - phat)
        vbar_p = norm(wp)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])
        up = array([[0], [10 * arctan(tan(0.5 * (thetabar_p - pθ)))]])

    # Control commande to reach the final destination of the obstacle
    wq = vhat - 2 * (array([[qx], [qy]]) - qhat)
    vbar_q = norm(wq)
    thetabar_q = arctan2(wq[1, 0], wq[0, 0])
    uq = array([[0], [10 * arctan(tan(0.5 * (thetabar_q - qθ)))]])

    # Euler integration method
    xp = xp + dt * f(xp, up)
    xq = xq + dt * f(xq, uq)
    print('xp=', xp)
    print('xq=', xq)

    ''' Display '''
    draw_boat_and_vector(xp)                                # display of the boat
    draw_boat_and_vector(xq)                                # display of the obstacle boat
    draw_circle(ax, c[0,0], c[1,0], r, 'red')               # DCPA zone to avoid related to the obstacle boat
    draw_circle(ax, c[0,0], c[1,0], r+Ɛ, 'magenta')         # DCPA zone extended for safety : manoeuvring area
    draw_circle(ax, px, py, r, 'red')                       # DCPA zone to avoid related to the boat

    # Final destination of the boat and the obstacle boat
    draw_disk(ax, phat, 0.2, 'green')
    draw_disk(ax, qhat, 0.2, 'blue')

    # Display of paths
    ax.plot([px0, phat[0, 0]], [py0, phat[1, 0]], linestyle='dotted', color='purple')   # initial path
    Lx.append(px)
    Ly.append(py)
    for x, y in zip(Lx, Ly):
        draw_disk(ax, array([[x], [y]]), 0.08, 'green')                                 # corrected path to avoid collision






