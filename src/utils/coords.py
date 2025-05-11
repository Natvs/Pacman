class coords:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collides(self, x, y):
        return self.x == x and self.y == y