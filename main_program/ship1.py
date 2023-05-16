class Ship1(Ship):

    # initialize ship attributes
    def __init__(self, xp):
        # x, y represent initial position
        self.x, self.y ,self.speed, self.direction = xp
        self.image = self.load_image("./image/870056.png")