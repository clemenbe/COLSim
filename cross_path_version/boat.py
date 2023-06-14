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
        self.crossed = False

    # Update the position of a ship based on up controller
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

    # Draw the boat and his circles
    def draw_seg(self, ax, r, Ɛ, future_state_boat, future_state_obstacle):
        draw_boat_and_vector(self.get_state_vector())       # Display of the boat and his speed vector
        draw_circle(ax, self.x, self.y, r, 'red')           # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, r + Ɛ, 'magenta')   # DCPA zone extended for safety : manoeuvring area
        draw_disk(ax, self.phat, 0.2, 'green')              # Final position to reach

        # xa_boat, ya_boat, va_boat, thetaa_boat = future_state_boat[0].flatten()
        # xb_boat, yb_boat, vb_boat, thetab_boat = future_state_boat[1].flatten()
        # xc_obstacle, yc_obstacle, vc_obstacle, thetac_obstacle = future_state_obstacle[0].flatten()
        # xd_obstacle, yd_obstacle, vd_obstacle, thetad_obstacle = future_state_obstacle[1].flatten()
        # # Coordinates of the boat+DCPA
        # xA = xa_boat + cos(thetaa_boat) * r
        # yA = ya_boat + sin(thetaa_boat) * r
        # xB = xb_boat + cos(thetab_boat) * r
        # yB = yb_boat + sin(thetab_boat) * r
        # # xA = xa_boat
        # # yA = ya_boat
        # # xB = xb_boat
        # # yB = yb_boat
        # # Coordinates of the obstacle+DCPA
        # xC = xc_obstacle - cos(thetac_obstacle) * r
        # yC = yc_obstacle - sin(thetac_obstacle) * r
        # xD = xd_obstacle - cos(thetad_obstacle) * r
        # yD = yd_obstacle - sin(thetad_obstacle) * r
        # # xC = xc_obstacle
        # # yC = yc_obstacle
        # # xD = xd_obstacle
        # # yD = yd_obstacle
        # plt.plot([xA, xB], [yA, yB], 'y-')
        # plt.plot([xC, xD], [yC, yD], 'b-')
        # # plt.plot([2.1, 2.7], [2.5, 3.4], 'g-')
        # # plt.plot([-0.2, -0.39], [-1.4, -0.9], 'g-')


    def get_state_vector(self):
        return np.vstack((self.x, self.y, self.v, self.theta))


    
    # Function called by move(), when there is risk of collision
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


    # Move the ship straightly to the desired position when there is no risk of collision
    # Called by move()
    def move_straight(self):
        vhat = array([[1], [1]])
        # Control commande to reach the final destination if there is no risk of collision
        wp = vhat - 2 * (array([[self.x], [self.y]]) - self.phat)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])

        up = array([[0], [10*arctan(tan(0.5*(thetabar_p - self.theta)))]])
        return up

    def move_straight_segment(self, x, y, theta):
        vhat = array([[1], [1]])
        # Control commande to reach the final destination if there is no risk of collision
        wp = vhat - 2 * (array([[x], [y]]) - self.phat)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])

        up = array([[0], [10 * arctan(tan(0.5 * (thetabar_p - theta)))]])
        return up


    def get_future_state(self, dt):
        future_state = []
        temp = (self.x, self.y, self.v, self.theta)

        for t in range(2):
            u = self.move_straight()
            self.update(u, dt)
            x_boat = self.get_state_vector()
            future_state.append(x_boat)

        self.x, self.y, self.v, self.theta = temp
        return future_state

    # def get_future_state(self, dt):
    #     future_state = []
    #     x, y, v, theta = self.x, self.y, self.v, self.theta
    #
    #     for _ in range(2):
    #         u = self.move_straight_segment(self, x, y, theta)
    #         x_boat = f(x, y, v, theta, u, dt)
    #         future_state.append(x_boat)
    #         x, y, v, theta = x_boat.flatten()
    #
    #     # self.x, self.y, self.v, self.theta = temp
    #     return future_state


    # Moves the ship every iteration
    def move(self, boats, checked_boats, ax, Ɛ, s, r, k, dt):
        #up = array([[0], [0]])
        in_collision = False
        # res = [np.vstack((0,0,0,0)), np.vstack((0,0,0,0))]
        # res_ = [np.vstack((0, 0, 0, 0)), np.vstack((0, 0, 0, 0))]


        # Check risks of collision
        for other_boat in boats:
            # If the boat has not been checked before
            if self != other_boat and other_boat not in checked_boats:

                # # Predict future
                # future_state_other = other_boat.get_future_state(2)
                #
                # future_state_boat = self.get_future_state(2)
                # print('future_state_boat =', future_state_boat)
                # print('future_state_other =', future_state_other)
                #
                # cross_path = check_cross_path(future_state_boat, future_state_other, r)

                # cross_path = check_vector_intersection(self.v, self.theta, other_boat.v, other_boat.theta)


                # Avoid collision
                if dist(array([[other_boat.x], [other_boat.y]]), array([[self.x], [self.y]])) < r + Ɛ:

                    if not self.crossed:

                        cross_path = check_vector_intersection(self.x, self.y, self.v, self.theta, other_boat.x,
                                                               other_boat.y, other_boat.v, other_boat.theta)

                        if not cross_path :
                            # res = future_state_boat
                            # res_ = future_state_other
                            self.crossed = True
                            print('safe')
                            continue

                        else:
                            print('Risk of collision')
                            self.crossed = True
                            up = self.avoid_collision(other_boat, ax, Ɛ, s, r, k)
                            in_collision = True

                    # # Predict future moves
                    # future_state_boat = self.get_future_state(2)
                    # future_state_other = other_boat.get_future_state(2)
                    # print('future_state_boat', future_state_boat)
                    # print('future_state_other', future_state_other)
                    #
                    # cross_path = check_cross_path(future_state_boat, future_state_other, r)
                    
                    # When there is no danger of collision

                    else :
                        print('Risk of collision')
                        up = self.avoid_collision(other_boat, ax, Ɛ, s, r, k)
                        in_collision = True


                    # res = future_state_boat
                    # res_ = future_state_other

            # else:
            #     self.crossed = False


        # If no collision
        if not in_collision:
            up = self.move_straight()

        # Update position
        self.update(up, dt)

        # Add checked boat
        checked_boats.add(self)

        # return (res, res_)




                    
