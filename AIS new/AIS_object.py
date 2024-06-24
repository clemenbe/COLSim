from draw import *

class LearningShip():

    def __init__(self, x, y, v, theta, df):
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta
        self.df = df
        self.index = 0
        self.privilege = 700


    def get_last_data(self, df, t, start_index=0):
        return


    # Moves the ship every iteration
    def move(self, boats, checked_boats, ax, t, dt):
        index_t_line = self.get_last_data(self.df, t)
        t_line = self.df.loc[index_t_line, 't']  # Time value corresponding to the current line
        # Check if the index time is inferior to the global time of the simu to update each boat state
        if t_line < t:
            self.v = self.df.loc[self.index, 'speedoverground']
            self.theta = self.df.loc[self.index, 'trueheading']
            self.index += 1
            print('--------------------------')
            print('index = ', self.index)
            print('self.x = ', self.x)
            print('self.y = ', self.y)
            print('self.v = ', self.v)
            print('self.theta = ', self.theta)
            self.x += dt * self.v * cos(self.theta)
            self.y += dt * self.v * sin(self.theta)

    def get_state_vector(self):
        return np.vstack((self.x, self.y, self.v, self.theta))

    # Draw circle around boat
    def draw(self, ax, r, Ɛ):
        draw_boat_and_vector(self.get_state_vector())  # display of the
        draw_circle(ax, self.x, self.y, r, 'red')  # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, r + Ɛ, 'magenta')  # DCPA zone extended for safety : manoeuvring area