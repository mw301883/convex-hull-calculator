import matplotlib.pyplot as plt

class PlotCanvas:
    def __init__(self, model):
        self.model = model
        self.figure, self.ax = plt.subplots()
        self.ax.set_title("Kliknij aby dodać punkt")
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

    def draw_points(self):
        self.ax.clear()
        self.ax.set_title("Kliknij aby dodać punkt")
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

        points = self.model.get_points()
        if points:
            xs, ys = zip(*points)
            self.ax.plot(xs, ys, 'ro')

        self.figure.canvas.draw()
