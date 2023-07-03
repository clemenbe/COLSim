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

# Called by move(), when there is risk of collision
def avoid_collision(boat, obstacle, ax, Ɛ, s, r, k, rule_window):

    # get display color for each instance
    color = boat.get_color()

    px, py, pv, ptheta = boat.get_state_vector().flatten()
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


class Boat:

    # v is speed, theta is direction
    def __init__(self, x, y, v, theta):
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta
        # 10 is the distance from initial position to destination
        self.phat = array([[self.x + 20 * cos(self.theta)], [self.y + 20 * sin(self.theta)]])
        self.privilege = 0
        self.r = 2
        self.in_collision = False

    # Update the position of a ship based on up controller
    def update(self, u, dt):
        x, y, v, theta = self.x, self.y, self.v, self.theta
        self.x += dt * v * cos(theta) 
        self.y += dt * v * sin(theta) 
        self.v = v + dt * u[0][0] 
        self.theta += dt * u[1][0]

    # Draw circle around boat
    def draw(self, ax, r, Ɛ):
        draw_boat_and_vector(self.get_state_vector())           # Display of the boat
        draw_circle(ax, self.x, self.y, self.r, 'red')               # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, self.r + Ɛ, 'magenta')       # DCPA zone extended for safety : manoeuvring area
        draw_disk(ax, self.phat, 0.2, 'green')                  # Display of the final destination

    def get_state_vector(self):
        return np.vstack((self.x, self.y, self.v, self.theta))
    
    # get the color displayed on the rules
    def get_color(self):
        return "green"

    # Move the ship straightly when there is no risk of collision
    # Called by move()
    def move_straight(self):
        vhat = array([[1], [1]])
        # Control commande to reach the final destination if there is no risk of collision
        wp = vhat - 2 * (array([[self.x], [self.y]]) - self.phat)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])

        up = array([[0], [10*arctan(tan(0.5*(thetabar_p - self.theta)))]])
        return up

    
    # Moves the ship every iteration
    def move(self, boats, ax, Ɛ, s, r, k, dt, rule_window):
        #up = array([[0], [0]])
        print('priviliege', self.privilege)

        in_collision = False

        # Check risks of collision
        for other_boat in boats:
            # If the boat has not been checked before
            if self != other_boat:
                # Avoid collision
                if dist(array([[other_boat.x], [other_boat.y]]), array([[self.x], [self.y]])) < max(self.r, other_boat.r) + Ɛ:
                    # Avoid collision depending on privilege
                    if self.privilege <= other_boat.privilege:
                        up = avoid_collision(self, other_boat, ax, Ɛ, s, max(self.r, other_boat.r), k, rule_window)
                        # Update position
                        self.update(up, dt)
                        print('ship')
                        in_collision = True


        # If no collision
        if not in_collision:
            up = self.move_straight()
            # Update position
            self.update(up, dt)



                    
    