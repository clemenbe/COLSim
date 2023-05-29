from calcul_tools import *
from draw import *
from boat import Boat
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

def compute_destination(x, y, theta, distance):
    destination_x = x + distance * cos(theta)
    destination_y = y + distance * sin(theta)
    return array([[destination_x], [destination_y]])


class Simulation:
    def __init__(self, boatpairs, dt, k, r):
        self.boatpairs = boatpairs
        self.dt = dt
        self.k = k
        self.r = r

    def run(self, num_steps, ax, Ɛ, s):

        # instructions
        vhat = array([[1], [1]])
        
        # vector of variables to draw a pair of ships
        collision_variables = []
        for i in range(len(self.boatpairs)):
            boat, obstacle = self.boatpairs[i]
            phat = compute_destination(boat.x, boat.y, boat.theta, 10)  # here 10 is the desired travel distance for the boat
            qhat = compute_destination(obstacle.x, obstacle.y, obstacle.theta, 10)  # and 5 is the desired travel distance for the obstacle
            # ax, xp, xq, c, phat, qhat
            collision_variables.append([0, 0, 0, 0, phat, qhat])

        for _ in range(num_steps):

            for i, boatpair in enumerate(self.boatpairs):

                boat, obstacle = boatpair

                clear(ax)

                qx, qy, qv, qtheta = obstacle.get_state_vector().flatten()
                px, py, pv, ptheta = boat.get_state_vector().flatten()
                c = array([[qx],
                        [qy]])
                D = array([[self.r, 0],
                        [0, self.r]])

                # phat = array([[7.5], [8]])
                # qhat = array([[-2.5], [8]])

                scalar_pdt = geo_scalar_prod(qv, pv, qtheta, ptheta)

                if dist(array([[qx], [qy]]), array([[px], [py]])) < self.r + Ɛ:
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
                        up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, self.k, self.r)
                        print('up = ',up)
                        draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, self.k, self.r)
                    else:
                        print('------------------Boats in opposite directions------------------')
                        # Tests to find where the boat is compared with the obstacle
                        if (py > qy - Ɛ):
                            # The boat is in the front zone of the obstacle
                            print('------------------Left front zone------------------')
                            φ = φccw
                            # Boat
                            up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, self.k, self.r)
                            print('up = ', up)
                            draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, self.k, self.r)
                        elif (py > qy - Ɛ) and (px > qx) and (scalar_pdt < abs(qv * pv) * cos(2.5)):
                            # The boat is in the front zone of the obstacle
                            print('------------------Right front zone (align)------------------')
                            up = array([[0], [0]])
                        elif py > qy - Ɛ and px > qx and scalar_pdt > abs(qv * pv) * cos(2.5):
                            # The boat is in the front zone of the obstacle
                            print('------------------Right front zone------------------')
                            φ = φccw
                            # Boat
                            up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, self.k, self.r)
                            print('up = ', up)
                            draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, self.k, self.r)

                        else:
                            # The boat is in the right lower zone compared with the obstacle
                            print('------------------Lower zone------------------')
                            φ = φrep
                            # Boat
                            up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, self.k, self.r)
                            print('up = ', up)
                            draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, self.k, self.r)
                else:
                    # Control commande to reach the final destination if there is no risk of collision
                    wp = vhat - 2 * (array([[px], [py]]) - phat)
                    thetabar_p = arctan2(wp[1, 0], wp[0, 0])
                    up = array([[0], [10*arctan(tan(0.5*(thetabar_p - ptheta)))]])
                    print('up = ', up)

                # Control commande to reach the final destination of the obstacle
                wq = vhat - 2 * (array([[qx], [qy]]) - qhat)
                thetabar_q = arctan2(wq[1, 0], wq[0, 0])
                uq = array([[0], [10 * arctan(tan(0.5 * (thetabar_q - qtheta)))]])
                print('uq = ', uq)

                boat.update(up, self.dt)
                obstacle.update(uq, self.dt)
                xp = boat.get_state_vector()
                xq = obstacle.get_state_vector()

                # integrate all values into the vector
                collision_variables[i][0] = ax
                collision_variables[i][1] = xp
                collision_variables[i][2] = xq
                collision_variables[i][3] = c


            ''' Display '''
            for ax, xp, xq, c, phat, qhat in collision_variables:
                px, py, pv, ptheta = xp.flatten()
                draw_boat_and_vector(xp)  # display of the boat
                draw_boat_and_vector(xq)  # display of the obstacle boat
                draw_circle(ax, c[0, 0], c[1, 0], self.r, 'red')  # DCPA zone to avoid related to the obstacle boat
                draw_circle(ax, c[0, 0], c[1, 0], self.r + Ɛ, 'magenta')  # DCPA zone extended for safety : manoeuvring area
                draw_circle(ax, px, py, self.r, 'red')  # DCPA zone to avoid related to the boat

                # Final destination of the boat and the obstacle boat
                draw_disk(ax, phat, 0.2, 'green')
                draw_disk(ax, qhat, 0.2, 'blue')

            plt.xlim(-s, s)
            plt.ylim(-s, s)
            plt.pause(0.01)

        plt.show()
