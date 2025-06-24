import random
import sys
from tkinter import Entry
from tkinter import Label, Button, Frame, Canvas, Scrollbar, X, LEFT, RIGHT, VERTICAL
from tkinter import messagebox, Listbox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from model.points_model import PointsModel
from plot.plot_canvas import PlotCanvas


class MainWindow:
    MAX_POINTS = 30

    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator otoczki wypukłej - Michał Wieczorek, Kamil Grabowski, Olaf Wnęczak, Jakub Salamon")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#f8f8f8")
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        top_bar = Frame(self.root, bg="#f8f8f8")
        top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        title = Label(top_bar, text="Kalkulator otoczki wypukłej - Michał Wieczorek, Kamil Grabowski, Olaf Wnęczak, Jakub Salamon", font=("Arial", 16, "bold"), bg="#f8f8f8")
        title.pack(side=LEFT)

        btn_close = Button(top_bar, text="Zamknij", command=self.quit_program,
                           bg="#e74c3c", fg="white", relief="flat", font=("Arial", 10), padx=10, pady=4)
        btn_close.pack(side=RIGHT)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        left_panel = Frame(self.root, bg="#f8f8f8")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))

        left_panel.grid_rowconfigure(0, weight=0)
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_rowconfigure(2, weight=0)

        left_panel.grid_columnconfigure(0, weight=1)

        Label(left_panel, text="Lista punktów:", bg="#f8f8f8", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0,5))

        canvas_container = Frame(left_panel)
        canvas_container.grid(row=1, column=0, sticky="nsew")

        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)

        self.canvas_points = Canvas(canvas_container, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas_points.grid(row=0, column=0, sticky="nsew")

        scrollbar = Scrollbar(canvas_container, orient=VERTICAL, command=self.canvas_points.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas_points.configure(yscrollcommand=scrollbar.set)

        self.points_frame = Frame(self.canvas_points, bg="white")
        self.canvas_points.create_window((0, 0), window=self.points_frame, anchor="nw")
        self.points_frame.bind("<Configure>", lambda e: self.canvas_points.configure(scrollregion=self.canvas_points.bbox("all")))

        btn_container = Frame(left_panel, bg="#f8f8f8")
        btn_container.grid(row=2, column=0, pady=10, sticky="ew")

        entry_frame = Frame(left_panel, bg="#f8f8f8")
        entry_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        Label(entry_frame, text="X:", bg="#f8f8f8", font=("Arial", 10)).pack(side=LEFT, padx=(0,5))
        self.entry_x = Entry(entry_frame, width=7)
        self.entry_x.pack(side=LEFT, padx=(0, 10))

        Label(entry_frame, text="Y:", bg="#f8f8f8", font=("Arial", 10)).pack(side=LEFT, padx=(0,5))
        self.entry_y = Entry(entry_frame, width=7)
        self.entry_y.pack(side=LEFT, padx=(0, 10))

        btn_add_point = Button(entry_frame, text="Dodaj punkt", command=self.add_point_from_entry,
                               bg="#1abc9c", fg="white", relief="flat", font=("Arial", 10), padx=10, pady=2)
        btn_add_point.pack(side=LEFT)

        Button(btn_container, text="Wyczyść", command=self.clear_all_points,
               bg="#3498db", fg="white", relief="flat", font=("Arial", 10), padx=10, pady=4).pack(side=LEFT, padx=5)

        self.btn_convex_hull = Button(btn_container, text="Oblicz otoczkę", command=self.compute_convex_hull,
                                      bg="#2ecc71", fg="white", relief="flat", font=("Arial", 10), padx=10, pady=4)
        self.btn_convex_hull.pack(side=LEFT, padx=5)

        Button(btn_container, text="Losuj punkty", command=self.randomize_points,
               bg="#f39c12", fg="white", relief="flat", font=("Arial", 10), padx=10, pady=4).pack(side=LEFT, padx=5)

        # po utworzeniu left_panel:
        points_frame = Frame(left_panel, bg="#f8f8f8")
        points_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        # Wiersz z otoczką i typem figury
        hull_row = Frame(points_frame, bg="#f8f8f8")
        Label(points_frame, text="Punkty otoczki:", font=("Arial", 11, "bold"), bg="#f8f8f8", anchor="w").grid(row=0, column=0, sticky="w", pady=(0,5))
        hull_row.grid(row=1, column=0, sticky="nsew")

        self.hull_points_listbox = Listbox(hull_row, font=("Arial", 11), width=30, height=30, fg="red")
        self.hull_points_listbox.pack(side=LEFT)

        self.hull_type_label = Label(hull_row, text="Typ figury: brak", font=("Arial", 11, "bold"), bg="#f8f8f8",
                                     anchor="e", justify="right")
        self.hull_type_label.pack(side=RIGHT, padx=10)


        self.hull_computed = False

        self.model = PointsModel()

        self.plot = PlotCanvas(self.model)

        self.canvas_widget = FigureCanvasTkAgg(self.plot.figure, master=self.root)
        self.canvas_widget.get_tk_widget().grid(row=1, column=1, sticky="nsew", padx=(0,10), pady=(0,10))
        self.canvas_widget.mpl_connect("button_press_event", self.on_click)

        self.update_point_list()

    def on_click(self, event):
        if event.inaxes != self.plot.ax:
            return

        if len(self.model.get_points()) >= self.MAX_POINTS:
            messagebox.showwarning("Limit punktów", f"Można dodać maksymalnie {self.MAX_POINTS} punktów.")
            return

        self.model.add_point(event.xdata, event.ydata)
        self.plot.draw_points()
        self.update_point_list()

    def update_point_list(self):
        for widget in self.points_frame.winfo_children():
            widget.destroy()

        points = self.model.get_points()
        if not points:
            Label(self.points_frame, text="Brak punktów", bg="white", anchor="w", font=("Arial", 10)).pack(anchor="w", padx=10, pady=5)
            return

        for idx, (x, y) in enumerate(points):
            point_str = f"({x:.2f}, {y:.2f})"
            point_row = Frame(self.points_frame, bg="white")
            point_row.pack(fill=X, anchor="w", pady=2, padx=5)

            Label(point_row, text=point_str, width=20, anchor="w", bg="white", font=("Arial", 10)).pack(side=LEFT, padx=5)

            btn_delete = Button(point_row, text="Usuń", command=lambda i=idx: self.delete_point(i),
                                bg="#d9534f", fg="white", relief="flat", font=("Arial", 9), padx=6, pady=2)
            btn_delete.pack(side=RIGHT, padx=5)

            btn_delete.bind("<Enter>", lambda e, i=idx: self.plot.highlight_point(i))
            btn_delete.bind("<Leave>", lambda e: self.plot.remove_highlight())

    def quit_program(self):
        self.root.destroy()
        sys.exit(0)

    def delete_point(self, index):
        self.model.remove_point(index)
        self.plot.draw_points()
        self.update_point_list()

    def clear_all_points(self):
        self.model.clear()
        self.plot.draw_points()
        self.update_point_list()

    def randomize_points(self):
        self.model.clear()
        num_points = random.randint(1, self.MAX_POINTS)
        for _ in range(num_points):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            self.model.add_point(x, y)
        self.plot.draw_points()
        self.update_point_list()

    def add_point_from_entry(self):
        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawne liczby dla X i Y.")
            return

        if not (0 <= x <= 100 and 0 <= y <= 100):
            messagebox.showwarning("Zakres wartości", "Współrzędne X i Y muszą być w zakresie od 0 do 100.")
            return

        if len(self.model.get_points()) >= self.MAX_POINTS:
            messagebox.showwarning("Limit punktów", f"Można dodać maksymalnie {self.MAX_POINTS} punktów.")
            return

        self.model.add_point(x, y)
        self.plot.draw_points()
        self.update_point_list()

        self.entry_x.delete(0, 'end')
        self.entry_y.delete(0, 'end')

    def compute_convex_hull(self):
        hull, shape_type = self.model.gift_wrapping()
        if not hull:
            return

        # Zaokrąglenie
        rounded_hull = [(round(x, 2), round(y, 2)) for x, y in hull]
        rounded_all = [(round(x, 2), round(y, 2)) for x, y in self.model.get_points()]

        # Wypełnienie prawego listboxa punktami otoczki
        self.hull_points_listbox.delete(0, 'end')
        for pt in rounded_hull:
            self.hull_points_listbox.insert('end', f"({pt[0]}, {pt[1]})")

        # Rysowanie otoczki
        self.plot.draw_hull(rounded_hull)

        self.hull_type_label.config(text=f"Typ figury: {shape_type}")

    def remove_convex_hull(self):
        self.hull_computed = False

        self.btn_convex_hull.config(text="Oblicz otoczkę", command=self.compute_convex_hull,
                                    bg="#2ecc71")
        self.plot.draw_points()
