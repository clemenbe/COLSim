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




class Simulation:
    def __init__(self, boat, obstacle, dt, k, r):
        self.boat = boat
        self.obstacle = obstacle
        self.dt = dt
        self.k = k
        self.r = r


    def run(self, num_steps, ax, Ɛ, s):
        for _ in range(num_steps):
            clear(ax)

            qx, qy, qv, qtheta = self.obstacle.get_state_vector().flatten()
            px, py, pv, ptheta = self.boat.get_state_vector().flatten()
            c = array([[qx],
                       [qy]])
            D = array([[self.r, 0],
                       [0, self.r]])

            # Instructions
            vhat = array([[1], [1]])
            phat = array([[7.5], [8]])
            qhat = array([[-2.5], [8]])

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

            self.boat.update(up, self.dt)
            self.obstacle.update(uq, self.dt)
            xp = self.boat.get_state_vector()
            xq = self.obstacle.get_state_vector()

            ''' Display '''
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
