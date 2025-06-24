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

    def gift_wrapping(self):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # współliniowe
            return 1 if val > 0 else 2  # zgodnie lub przeciwnie do ruchu wskazówek zegara

        points = list(set(self.points))  # usunięcie duplikatów
        n = len(points)
        if n == 0:
            return [], "brak punktów"
        if n == 1:
            return [points[0]], "punkt"
        if n == 2:
            return points, "odcinek"

        hull = []
        l = min(range(n), key=lambda i: (points[i][0], points[i][1]))
        p = l
        while True:
            hull.append(points[p])
            q = (p + 1) % n
            for i in range(n):
                if orientation(points[p], points[i], points[q]) == 2:
                    q = i
            p = q
            if p == l:
                break

        if len(hull) == 2:
            return hull, "odcinek"
        elif len(hull) == 3:
            return hull, "trójkąt"
        elif len(hull) == 4:
            return hull, "czworokąt"
        else:
            return hull, f"{len(hull)}-kąt"
