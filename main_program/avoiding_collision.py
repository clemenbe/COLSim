from calcul_tools import *
from draw import *
import math


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
DCPA = 2       # DCPA
D = array([[DCPA, 0],
          [0, DCPA]])
Ɛ = 2       # radius added to the dangerous zone
r = 2


# call from simulation.py
# simulation is the current simulation
# colliding_ships and non_colliding_ships are vectors that contains ship objects
def avoid_collision(simulation, colliding_ships, non_colliding_ships, vhat = array([[1], [1]]), phat = array([[7.5], [8]]), qhat = array([[-2.5], [8]]), rhat = array([[-7.5], [-8]])):
    dt = simulation.dt
    r = simulation.collision_radius

    while colliding_ships != []:
        

    # here is how you can access ships in collision

        #for pair_index, shippair in enumerate(colliding_ships):
        #ship1_index, ship2_index = shippair
        ship1_index, ship2_index = colliding_ships[0]
        # get the ships object by index access
        ship1 = simulation.ships[ship1_index]
        ship2 = simulation.ships[ship2_index]
        # depents on which one you see as obstacle
        px = ship1.x
        py = ship1.y
        qx = ship2.x
        qy = ship2.y
        pv = ship1.speed
        qv = ship2.speed
        pθ = math.radians(ship1.direction)
        qθ = math.radians(ship2.direction)
        xp = array([[px], [py], [pv], [pθ]])
        xq = array([[qx], [qy], [qv], [qθ]])

        c = array([[qx], [qy]])         # coordinates of the circle representing the obstacle zone to avoid
        scalar_pdt = geo_scalar_prod(qv, pv, qθ, pθ)

        if dist(xp, xq) < r :

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


            else :
                print('------------------Boats in opposite directions------------------')
                # Tests to find where the boat is compared with the obstacle
                if (py > qy - Ɛ):
                    # The boat is in the front zone of the obstacle
                    print('------------------Left front zone------------------')
                    φ = φccw
                    # Boat
                    up = control(xp, φ, c)
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
                else:
                    # The boat is in the right lower zone compared with the obstacle
                    print('------------------Lower zone------------------')
                    φ = φrep
                    # Boat
                    up = control(xp, φ, c)



            # Control commande to reach the final destination of the obstacle
            wq = vhat - 2 * (array([[qx], [qy]]) - qhat)
            thetabar_q = arctan2(wq[1, 0], wq[0, 0])
            uq = array([[0], [10 * arctan(tan(0.5 * (thetabar_q - qθ)))]])

            # Euler integration method
            print('up=', up)
            xp = xp + dt * f(xp, up)
            xq = xq + dt * f(xq, uq)
            print('xp=', xp)
            print('xq=', xq)

            px, py, pv, pθ = xp.flatten()
            qx, qy, qv, qθ = xq.flatten()

            simulation.ships[ship1_index].x = px
            simulation.ships[ship1_index].y = py
            simulation.ships[ship2_index].x = qx
            simulation.ships[ship2_index].y = qy
            simulation.ships[ship1_index].speed = pv
            simulation.ships[ship2_index].speed = qv
            simulation.ships[ship1_index].direction = math.degrees(pθ)
            simulation.ships[ship2_index].direction = math.degrees(qθ)

        # remove when out of collision
        else :
            colliding_ships.pop()


        # here is how you can access the rest of ships not in collision

        '''for other_ship_index in non_colliding_ships:
                other_ship = simulation.ships[other_ship_index]
                xr = other_ship.x
                yr = other_ship.y
                vr = other_ship.speed
                θr = other_ship.direction
                x = array([[xr], [yr], [vr], [θr]])

                # Control commande to reach the final destination
                w = vhat - 2 * (array([[xr], [yr]]) - rhat)
                thetabar = arctan2(w[1, 0], w[0, 0])
                u = array([[0], [10 * arctan(tan(0.5 * (thetabar - θr)))]])

                x = x + dt * f(x, u)

                simulation.ships[other_ship_index].x = xr
                simulation.ships[other_ship_index].y = yr
                simulation.ships[other_ship_index].speed = vr
                simulation.ships[other_ship_index].direction = θr

                # if ship becomes in collision with any other, put in colliding ships
                for i, ship in enumerate(simulation.ships):
                    if ship != other_ship and math.sqrt((ship.x - other_ship.x) ** 2 + (ship.y - other_ship.y) ** 2) <= r:
                        colliding_ships.append(i, other_ship_index)'''


        simulation.draw()




# TODO : ax ? px0 ? draw functions ?