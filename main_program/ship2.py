class Ship2(Ship):

    # initialize ship attributes
    def __init__(self, x, y, speed, direction):
        # x, y represent initial position
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.image = self.load_image("./image/870056.png")