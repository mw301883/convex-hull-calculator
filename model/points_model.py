class PointsModel:
    def __init__(self):
        self.points = []

    def add_point(self, x, y):
        self.points.append((round(x, 2), round(y, 2)))

    def get_points(self):
        return self.points
