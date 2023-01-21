class Punkt2D:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def odl(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5


class Punkt3d(Punkt2D):
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y)
        self.z = z
    
    def odl(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5
