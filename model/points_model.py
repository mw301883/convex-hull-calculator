class PointsModel:
    def __init__(self):
        self.points = []
        self.last_hull = []

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
        # Funkcja pomocnicza: określa orientację trzech punktów (p, q, r)
        # Zwraca:
        #   0 – punkty współliniowe
        #   1 – skręt w prawo (zgodnie z ruchem wskazówek zegara)
        #   2 – skręt w lewo (przeciwnie do ruchu wskazówek zegara)
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # współliniowe
            return 1 if val > 0 else 2  # zgodnie lub przeciwnie do ruchu wskazówek zegara

        def distance_sq(p, q):
            return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

        points = list(set(self.points))  # usunięcie duplikatów
        n = len(points)

        # Obsługa przypadków brzegowych
        if n == 0:
            return [], "brak punktów"
        if n == 1:
            return [points[0]], "punkt"
        if n == 2:
            return points, "odcinek"

        hull = []  # Lista przechowująca punkty otoczki

        # Znalezienie punktu o najmniejszej współrzędnej X (i Y w razie remisu) – zaczynamy od niego
        l = min(range(n), key=lambda i: (points[i][0], points[i][1]))
        p = l

        # Główna pętla algorytmu Gift Wrapping
        while True:
            hull.append(points[p])  # Dodaj aktualny punkt do otoczki
            q = (p + 1) % n  # Wstępnie przyjmujemy kolejny punkt jako następny w otoczce

            # Sprawdzenie wszystkich punktów, czy któryś z nich leży bardziej "na lewo"
            for i in range(n):
                orient = orientation(points[p], points[i], points[q])
                if orient == 2:  # skręt w lewo
                    q = i  # znaleziono lepszy punkt
                elif orient == 0:
                    # jeśli punkty współliniowe, wybierz punkt najdalej od p
                    if distance_sq(points[p], points[i]) > distance_sq(points[p], points[q]):
                        q = i  # wybieramy punkt najbardziej oddalony, żeby uniknąć punktów na prostej

            p = q  # przechodzimy do następnego punktu
            if p == l:  # jeśli wróciliśmy do punktu początkowego, kończymy
                break

        # Zapis ostatniej obliczonej otoczki w pamięci w celu jej szybkiego odtworzenia na wykresie
        self.last_hull = hull.copy()

        # Określenie typu figury na podstawie liczby punktów otoczki
        if len(hull) == 2:
            return hull, "odcinek"
        elif len(hull) == 3:
            return hull, "trójkąt"
        elif len(hull) == 4:
            return hull, "czworokąt"
        else:
            return hull, f"{len(hull)}-kąt"

