class PointsModel:
    def __init__(self):
        self.points = []

    def add_point(self, x, y):
        self.points.append((x, y))

    def get_points(self):
        return self.points

    def remove_point(self, index):
        if 0 <= index < len(self.points):
            self.points.pop(index)

    def clear(self):
        self.points.clear()