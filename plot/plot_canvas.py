from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

class PlotCanvas:
    def __init__(self, model):
        self.model = model
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.highlighted_index = None
        self._setup_plot()

    def _setup_plot(self):
        self.ax.set_title("Kliknij, aby dodać punkty")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)

        self.ax.xaxis.set_major_locator(MultipleLocator(5))
        self.ax.yaxis.set_major_locator(MultipleLocator(5))

        self.ax.grid(True, linestyle="--", linewidth=0.5, color="#ccc")

    def draw_points(self):
        self.ax.cla()
        self._setup_plot()

        points = self.model.get_points()
        if points:
            xs, ys = zip(*points)
            colors = ["blue"] * len(points)
            sizes = [40] * len(points)

            if self.highlighted_index is not None and 0 <= self.highlighted_index < len(points):
                colors[self.highlighted_index] = "red"
                sizes[self.highlighted_index] = 100

            self.ax.scatter(xs, ys, color=colors, s=sizes)

        self.figure.canvas.draw()

    def highlight_point(self, index):
        self.highlighted_index = index
        self.draw_points()

    def highlight_specific_point(self, point, color="yellow"):
        self.draw_points()

        if hasattr(self.model, 'last_hull') and self.model.last_hull:
            hull = self.model.last_hull
            if len(hull) >= 2:
                xs, ys = zip(*(hull + [hull[0]]))
                self.ax.plot(xs, ys, color='red', linewidth=2)

        self.ax.plot(point[0], point[1], 'o', color=color, markersize=10)
        self.figure.canvas.draw()

    def remove_highlight(self):
        self.highlighted_index = None
        self.draw_points()

    def draw_hull(self, hull_points):
        self.draw_points()
        if len(hull_points) < 2:
            return
        xs, ys = zip(*(hull_points + [hull_points[0]]))
        self.ax.plot(xs, ys, color='red', linewidth=2)
        self.figure.canvas.draw()

