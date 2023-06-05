from boat import Boat

class Whale(Boat):

    def __init__(self, x, y, v, theta):
        super().__init__(x, y, v, theta)  # call the superclass's constructor
        self.privilege = 500