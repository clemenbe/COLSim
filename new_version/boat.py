from calcul_tools import *
from draw import *
from potential_fields import *

def Jφ0(p):
    """ Jacobian Matrix of φ0 """
    p1, p2 = p.flatten()
    return array([[-3 * p1 ** 2 - p2 ** 2 + 1, -2 * p1 * p2 - 1],
                  [-2 * p1 * p2 + 1, -3 * p2 ** 2 - p2 ** 2 + 1]])

def dφ(x, c, D):
    p1, p2, v, θ = x.flatten()
    z = inv(D) @ array([[p1 - c[0,0]], [p2 - c[1,0]]])
    dv = D @ Jφ0(z) @ inv(D) @ array([[cos(θ)], [sin(θ)]])
    return dv.flatten()


def control(x, φ, c, D, k, r):
    dφ1, dφ2 = dφ(x, c, D)
    x, y, v, θ = x.flatten()
    φ1, φ2 = φ(x, y, c, D, k, r)
    u1 = 0
    u2 = -sawtooth(θ - arctan2(φ2, φ1)) - (φ2 * dφ1 - φ1 * dφ2) / ((φ1 ** 2) + (φ2 ** 2))
    return array([[u1], [u2]])


class Boat:

    # v is speed, theta is direction
    def __init__(self, x, y, v, theta):
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta
        # 10 is the distance from initial position to destination
        self.phat = array([[self.x + 10 * cos(self.theta)], [self.y + 10 * sin(self.theta)]])

    # update the position of a ship based on up controller
    def update(self, u, dt):
        x, y, v, theta = self.x, self.y, self.v, self.theta
        self.x += dt * v * cos(theta)
        self.y += dt * v * sin(theta)
        self.v = v + dt * u[0][0]
        self.theta += dt * u[1][0]

    # draw circle around boat
    def draw(self, ax, r, Ɛ):
        draw_boat_and_vector(self.get_state_vector())  # display of the 
        draw_circle(ax, self.x, self.y, r, 'red')  # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, r + Ɛ, 'magenta')  # DCPA zone extended for safety : manoeuvring area
        draw_disk(ax, self.phat, 0.2, 'green')

    def get_state_vector(self):
        return np.vstack((self.x, self.y, self.v, self.theta))
    
    # called by move(), when there is risk of collision
    def avoid_collision(self, obstacle, ax, Ɛ, s, r, k):
        px, py, pv, ptheta = self.get_state_vector().flatten()
        qx, qy, qv, qtheta = obstacle.get_state_vector().flatten()
        
        scalar_pdt = geo_scalar_prod(qv, pv, qtheta, ptheta)

        c = array([[qx],
                [qy]])
        D = array([[r, 0],
                [0, r]])

        if dist(array([[qx], [qy]]), array([[px], [py]])) < r + Ɛ:
            if scalar_pdt >= 0:
                print('------------------Boats with close directions------------------')
                # Tests to find where the boat is compared with the obstacle
                if py > qy + Ɛ:
                    # The boat is in the front zone of the obstacle
                    print('------------------Front zone------------------')
                    φ = φrep
                elif (py < qy + Ɛ) and (px < qx):
                    # The boat is in the left lower zone compared with the obstacle
                    print('------------------Left lower zone------------------')
                    φ = φcw
                else:
                    # The boat is in the right lower zone compared with the obstacle
                    print('------------------Right lower zone------------------')
                    φ = φccw
                up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                print('up = ',up)
                draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, k, r)
            else:
                print('------------------Boats in opposite directions------------------')
                # Tests to find where the boat is compared with the obstacle
                if (py > qy - Ɛ):
                    # The boat is in the front zone of the obstacle
                    print('------------------Left front zone------------------')
                    φ = φccw
                    # Boat
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    print('up = ', up)
                    draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, k, r)
                elif (py > qy - Ɛ) and (px > qx) and (scalar_pdt < abs(qv * pv) * cos(2.5)):
                    # The boat is in the front zone of the obstacle
                    print('------------------Right front zone (align)------------------')
                    up = array([[0], [0]])
                elif py > qy - Ɛ and px > qx and scalar_pdt > abs(qv * pv) * cos(2.5):
                    # The boat is in the front zone of the obstacle
                    print('------------------Right front zone------------------')
                    φ = φccw
                    # Boat
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    print('up = ', up)
                    draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, k, r)

                else:
                    # The boat is in the right lower zone compared with the obstacle
                    print('------------------Lower zone------------------')
                    φ = φrep
                    # Boat
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    print('up = ', up)
                    draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, k, r)

        return up


    # move the ship straightly when there is no risk of collision
    # called by move()
    def move_straight(self):
        vhat = array([[1], [1]])
        # Control commande to reach the final destination if there is no risk of collision
        wp = vhat - 2 * (array([[self.x], [self.y]]) - self.phat)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])
        print(f'thetabar_p: {thetabar_p}, type: {type(thetabar_p)}')
        print(f'self.theta: {self.theta}, type: {type(self.theta)}')

        up = array([[0], [10*arctan(tan(0.5*(thetabar_p - self.theta)))]])
        return up

    
    # moves the ship every iteration
    def move(self, boats, checked_boats, ax, Ɛ, s, r, k, dt):
        #up = array([[0], [0]])
        in_collision = False

        # check risks of collision
        for other_boat in boats:
            # if the boat has not been checked before
            if self != other_boat and other_boat not in checked_boats:
                # avoid collision
                if dist(array([[other_boat.x], [other_boat.y]]), array([[self.x], [self.y]])) < r + Ɛ:
                    up = self.avoid_collision(other_boat, ax, Ɛ, s, r, k)
                    in_collision = True

        # if no collision
        if not in_collision:
            up = self.move_straight()

        # update position
        self.update(up, dt)

        # add checked boat
        checked_boats.add(self)

                    
    