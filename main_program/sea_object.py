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


class SeaObject:

    # x, y are positions, v is speed, theta is direction
    def __init__(self, x, y, v, theta):
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta

        destination_distance = 20 # the distance from initial position to destination
        self.phat = array([[self.x + destination_distance * cos(self.theta)], [self.y + destination_distance * sin(self.theta)]])

        self.privilege = 0
        self.r = 2 # collision avoidance radius for the object

    # Update the position of an object based on up controller
    def update(self, u, dt):
        x, y, v, theta = self.x, self.y, self.v, self.theta
        self.x += dt * v * cos(theta) 
        self.y += dt * v * sin(theta) 
        self.v = v + dt * u[0][0] 
        self.theta += dt * u[1][0]

    # return the object's x, y, speed and direction in a state vector
    def get_state_vector(self):
        return np.vstack((self.x, self.y, self.v, self.theta))
    
    # Move the object straight when there is no risk of collision
    # Called by move()
    def move_straight(self):
        vhat = array([[1], [1]])
        # Control commande to reach the final destination if there is no risk of collision
        wp = vhat - 2 * (array([[self.x], [self.y]]) - self.phat)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])

        up = array([[0], [10*arctan(tan(0.5*(thetabar_p - self.theta)))]])
        return up
    
    # Called by move(), when there is risk of collision
    def avoid_collision(self, obstacle, ax, Ɛ, s, r, k, rule_window):

        # get display color in the rules for each object
        color = self.get_color()

        px, py, pv, ptheta = self.get_state_vector().flatten()
        qx, qy, qv, qtheta = obstacle.get_state_vector().flatten()
        
        scalar_pdt = geo_scalar_prod(qv, pv, qtheta, ptheta)

        c = array([[qx],
                [qy]])
        D = array([[r, 0],
                [0, r]])


        # different cases of collision avoidance
        if dist(array([[qx], [qy]]), array([[px], [py]])) < r + Ɛ:
            if scalar_pdt >= 0:
                print('------------------Boats with close directions------------------')
                # Tests to find where the boat is compared with the obstacle
                if py > qy + Ɛ:
                    # The boat is in the front zone of the obstacle
                    print('------------------Front zone------------------')
                    φ = φrep

                    rule_window.apply_rule("finish overtaking the obstacle", color)
                    
                elif (py < qy + Ɛ) and (px < qx):
                    # The boat is in the left lower zone compared with the obstacle
                    print('------------------Left lower zone------------------')
                    φ = φcw

                    rule_window.apply_rule("overtaking the obstacle on the left side", color)

                else:
                    # The boat is in the right lower zone compared with the obstacle
                    print('------------------Right lower zone------------------')
                    φ = φccw

                    rule_window.apply_rule("overtaking the obstacle on the right side", color)

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

                    rule_window.apply_rule("red to red rule to avoid the collision", color)

                elif (py > qy - Ɛ) and (px > qx) and (scalar_pdt < abs(qv * pv) * cos(2.5)):
                    # The boat is in the front zone of the obstacle
                    print('------------------Right front zone (align)------------------')
                    up = array([[0], [0]])

                    rule_window.apply_rule("red to red rule to avoid the collision", color)

                elif py > qy - Ɛ and px > qx and scalar_pdt > abs(qv * pv) * cos(2.5):
                    # The boat is in the front zone of the obstacle
                    print('------------------Right front zone------------------')
                    φ = φccw
                    # Boat
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    print('up = ', up)
                    draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, k, r)

                    rule_window.apply_rule("red to red rule to avoid the collision", color)

                else:
                    # The boat is in the right lower zone compared with the obstacle
                    print('------------------Lower zone------------------')
                    φ = φrep
                    # Boat
                    up = control(array([[px], [py], [pv], [ptheta]]), φ, c, D, k, r)
                    print('up = ', up)
                    draw_field_around_c_new(ax, φ, -s, s, -s, s, 0.51, c, D, k, r)

                    rule_window.apply_rule("finish overtaking the obstacle", color)

        return up


    
    # Moves the object every iteration
    def move(self, sea_objects, ax, Ɛ, s, r, k, dt, rule_window):
        #up = array([[0], [0]])

        in_collision = False

        # Check risks of collision with every other object
        for other_object in sea_objects:

            if self != other_object:
                # when distance is smaller than collision radius
                if dist(array([[other_object.x], [other_object.y]]), array([[self.x], [self.y]])) < max(self.r, other_object.r) + Ɛ:
                    # object with smaller privilege avoids collision
                    if self.privilege <= other_object.privilege:
                        up = self.avoid_collision(other_object, ax, Ɛ, s, max(self.r, other_object.r), k, rule_window)
                        in_collision = True

        # If there is no need to avoid collision
        if not in_collision:
            up = self.move_straight()
            
        # Update position
        self.update(up, dt)

