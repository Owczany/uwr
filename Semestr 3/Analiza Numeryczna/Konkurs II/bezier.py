import tkinter as tk
import json
import numpy as np
from math import comb
from PIL import Image
import io

# CONSTS
DOT_SIZE = 5

# Klasa punkt
class Point:
    def __init__(self, x, y, weight, canvas_point):
        self.x = x
        self.y = y
        self.weight = weight
        self.canvas_point = canvas_point

    def to_dict(self):
        return {"x": self.x, "y": self.y, "weight": self.weight}


class Curve:
    def __init__(self, next=None):
        self.points = []
        self.last_points = []
        self.curve = None
        self.next = next

    def copy(self):
        """Tworzy nową instancję Curve, kopiując punkty i inne parametry."""
        new_curve = Curve(self.next)
        new_curve.points = [Point(p.x, p.y, p.weight, None) for p in self.points]
        new_curve.last_points = [Point(p.x, p.y, p.weight, None) for p in self.last_points]
        return new_curve

    def to_dict(self):
        return {"points": [p.to_dict() for p in self.points]}


class App:
    def __init__(self, root):
        self.root = root
        self.animations = []
        self.curves_number = 1
        self.curve = Curve()
        self.curve.next = self.curve
        self.event_history = []

        # Stan zapamiętania dla animacji
        self.saved_state = None

        # Pobranie rozmiaru ekranu
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Ustawienia okna
        self.root.title("Aplikacja Animacji")
        self.root.minsize(800, 500)
        self.root.maxsize(screen_width, screen_height)
        self.root.attributes('-fullscreen', True)

        # Dolny pasek przycisków
        self.bottom_frame = tk.Frame(root, height=100, bg="grey")
        self.bottom_frame.pack(side="bottom", fill="both", expand=False)
        self.bottom_frame.pack_propagate(False)

        # Tworzenie canvasu
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Przycisk cofnięcia
        tk.Button(self.bottom_frame, text="Cofnij", command=self.remove_last_point).pack(side="left", padx=10, pady=10)

        # Przycisk przywracania
        tk.Button(self.bottom_frame, text="Przywróć", command=self.returnn).pack(side="left", padx=10, pady=10)

        # Przycisk dodania nowej krzywej
        tk.Button(self.bottom_frame, text="Dodaj Nową Krzywą", command=self.create_new_curve).pack(side="left", padx=10, pady=10)

        # Przycisk zmiany krzywej
        tk.Button(self.bottom_frame, text="Zmień Krzywą", command=self.change_curve).pack(side="left", padx=10, pady=10)

        # Przycisk zapisywania animacji
        tk.Button(self.bottom_frame, text="Zapisz Animację", command=self.save_animation).pack(side="left", padx=10, pady=10)

        # Przycisk odtwarzania animacji
        tk.Button(self.bottom_frame, text="Odtwórz Animację", command=self.animate).pack(side="left", padx=10, pady=10)

        # Przycisk eksportowania animacji
        tk.Button(self.bottom_frame, text="Eksportuj Animację", command=self.export_animation).pack(side="left", padx=10, pady=10)

        # Przycisk eksportowania animacji
        tk.Button(self.bottom_frame, text="Importuj Animację", command=self.import_animation).pack(side="left", padx=10, pady=10)

        # Ustawienie focusu na canvasie
        self.canvas.focus_set()
        self.canvas.bind("<FocusOut>", self.ensure_focus)

        # Zdarzenia dla canvasu
        self.canvas.bind("<Button-1>", self.create_or_drag_point)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Return>", self.remove_all_points)
        self.canvas.bind("<BackSpace>", self.remove_last_point)
        self.canvas.bind("<Control-BackSpace>", self.remove_all_points)
        self.canvas.bind("<Command-BackSpace>", self.remove_all_points)
        self.canvas.bind("<Control-c>", self.change_curve)
        self.canvas.bind("<Command-c>", self.change_curve)
        self.canvas.bind("<Control-z>", self.returnn)
        self.canvas.bind("<Command-z>", self.returnn)
        self.canvas.bind("<Control-n>", self.create_new_curve)
        self.canvas.bind("<Command-n>", self.create_new_curve)
        self.canvas.bind("<Control-s>", self.save_canvas_as_image)
        self.canvas.bind("<Command-s>", self.save_canvas_as_image)
        self.canvas.bind("<Control-e>", self.save_animation)
        self.canvas.bind("<Command-e>", self.save_animation)
        self.canvas.bind("<Control-r>", self.animate)
        self.canvas.bind("<Command-r>", self.animate)

    # Zmień edytowaną krzywą
    def change_curve(self, event=None):
        self.hide_points()
        self.curve = self.curve.next
        self.show_points()
        self.draw_curve()

    # Stwórz nową krzywą
    def create_new_curve(self, event=None):
        self.hide_points()
        new_curve = Curve(self.curve.next)
        self.curve.next = new_curve
        self.curve = new_curve
        self.curves_number += 1

    # Stwórz lub przeciągnij
    def create_or_drag_point(self, event):
        closest = self.canvas.find_overlapping(event.x - DOT_SIZE, event.y - DOT_SIZE, event.x + DOT_SIZE, event.y + DOT_SIZE)
        if closest:
            for point in self.curve.points:
                if point.canvas_point in closest:
                    self.dragging_point = point
                    self.canvas.itemconfig(self.dragging_point.canvas_point, fill='blue')
                    return
        self.create_point(event)

    # Stwórz punkt
    def create_point(self, event):
        x, y = event.x, event.y
        point = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")
        self.curve.points.append(Point(x, y, 1, point))
        self.draw_curve()

    # Importownaie animacji
    def import_animation(self):
        """Importuje animację z pliku JSON."""
        try:
            with open("animation.json", "r", encoding="utf-8") as f:
                animation_data = json.load(f)

            self.animations = []  # Reset animacji

            for frame_data in animation_data:
                curves = frame_data["curves"]
                curves_number = frame_data["number_of_curves"]

                # Odtwarzamy powiązane krzywe
                first_curve = None
                previous_curve = None
                for curve_data in curves:
                    curve = Curve()
                    for point_data in curve_data["points"]:
                        curve.points.append(Point(
                            x=point_data["x"],
                            y=point_data["y"],
                            weight=point_data["weight"],
                            canvas_point=None  # Canvas nie jest potrzebny podczas importu
                        ))
                    if previous_curve:
                        previous_curve.next = curve
                    else:
                        first_curve = curve
                    previous_curve = curve

                # Zamykamy cykl krzywych
                if previous_curve:
                    previous_curve.next = first_curve

                # Dodajemy klatkę do animacji
                self.animations.append({
                    "curve": first_curve,
                    "curves_number": curves_number,
                })
            
            print("Animacja została zaimportowana z pliku animation.json")
        except FileNotFoundError:
            print("Nie znaleziono pliku animation.json")
        except json.JSONDecodeError:
            print("Błąd podczas odczytu pliku animation.json")


    def drag(self, event):
        if self.dragging_point:
            self.dragging_point.x = event.x
            self.dragging_point.y = event.y
            self.canvas.coords(self.dragging_point.canvas_point, event.x - 5, event.y - 5, event.x + 5, event.y + 5)
            self.draw_curve()

    def stop_drag(self, event):
        if hasattr(self, 'dragging_point') and self.dragging_point:
            self.canvas.itemconfig(self.dragging_point.canvas_point, fill='black')
            self.dragging_point = None

    def save_canvas_as_image(self, event=None, filename="canvas_image.png"):
        ps_filename = "canvas_image.ps"
        self.canvas.postscript(file=ps_filename, colormode='color')
        with Image.open(ps_filename) as img:
            img.save(filename, "PNG")
        print(f"Canvas zapisany jako {filename}")

    def ensure_focus(self, event):
        self.canvas.focus_set()

    def remove_last_point(self, event=None):
        if self.curve.points:
            point = self.curve.points.pop()
            self.curve.last_points.append(point)
            self.canvas.delete(point.canvas_point)
        self.draw_curve()

    def returnn(self, event=None):
        if self.curve.last_points:
            point = self.curve.last_points.pop()
            new_point = self.canvas.create_oval(point.x-5, point.y-5, point.x+5, point.y+5, fill="black")
            self.curve.points.append(Point(point.x, point.y, point.weight, new_point))
        self.draw_curve()

    def remove_all_points(self, event=None):
        while self.curve.points:
            point = self.curve.points.pop()
            self.curve.last_points.append(point)
            self.canvas.delete(point.canvas_point)

    def hide_points(self):
        for point in self.curve.points:
            self.canvas.delete(point.canvas_point)

    def show_points(self):
        for point in self.curve.points:
            point.canvas_point = self.canvas.create_oval(point.x-5, point.y-5, point.x+5, point.y+5, fill="black")

    def draw_curve(self, event=None):
        if self.curve.curve:
            self.canvas.delete(self.curve.curve)
            self.curve.curve = None
        if len(self.curve.points) < 2:
            return
        t_values = np.linspace(0, 1, 1000)
        curve = [Bezier.bezier_point(t, points=self.curve.points) for t in t_values]
        self.curve.curve = self.canvas.create_line(curve, smooth=False, fill="red", width=2)

    def save_animation(self, event=None):
        animation_frame = {
            "curve": self.curve.copy(),
            "curves_number": self.curves_number,
        }
        self.animations.append(animation_frame)
        print("Dodano klatkę animacji")

    def export_animation(self):
        """Eksportuje animację do pliku JSON."""
        if not self.animations:
            print("Brak animacji do eksportu.")
            return

        animation_data = []
        for frame in self.animations:
            curves = []
            curve = frame["curve"]
            for _ in range(frame["curves_number"]):
                curves.append(curve.to_dict())  # Dodanie danych każdej krzywej do listy
                curve = curve.next  # Przechodzimy do kolejnej krzywej w cyklu
            
            frame_data = {
                "curves": curves,  # Lista wszystkich krzywych
                "number_of_curves": frame["curves_number"],  # Liczba krzywych
            }
            animation_data.append(frame_data)

        # Zapis do pliku JSON
        try:
            with open("animation.json", "w", encoding="utf-8") as f:
                json.dump(animation_data, f, indent=4, ensure_ascii=False)
            print("Animacja została wyeksportowana do pliku animation.json")
        except Exception as e:
            print(f"Wystąpił błąd podczas eksportu animacji: {e}")



    def save_current_state(self):
        """Zapisuje obecny stan krzywych i punktów."""
        self.saved_state = {
            "curves": [],
            "curves_number": self.curves_number,
        }
        current_curve = self.curve
        for _ in range(self.curves_number):
            self.saved_state["curves"].append(current_curve.copy())
            current_curve = current_curve.next

    def restore_saved_state(self):
        """Przywraca ostatni zapisany stan krzywych i punktów."""
        if self.saved_state:
            self.curves_number = self.saved_state["curves_number"]
            saved_curves = self.saved_state["curves"]

            # Odtwórz listę krzywych
            previous_curve = None
            first_curve = None
            for saved_curve in saved_curves:
                curve = saved_curve.copy()
                if previous_curve:
                    previous_curve.next = curve
                else:
                    first_curve = curve
                previous_curve = curve
            previous_curve.next = first_curve  # Zamyka pętlę krzywych
            self.curve = first_curve

            # Usuń wszystko z canvasu i narysuj krzywe od nowa
            self.canvas.delete("all")
            self.show_points()
            for _ in range(self.curves_number):
                self.draw_curve()
                self.curve = self.curve.next

    def animate(self, event=None):
        if not self.animations:
            print("Brak klatek animacji do odtworzenia.")
            return

        self.save_current_state()

        def play_frame(index):
            if index == len(self.animations):
                self.restore_saved_state()
                return
            frame = self.animations[index]
            self.curve = frame["curve"]
            self.curves_number = frame["curves_number"]
            self.canvas.delete("all")
            for _ in range(self.curves_number):
                self.draw_curve()
                self.curve = self.curve.next
            self.root.after(500, lambda: play_frame(index + 1))

        play_frame(0)

class Bezier:
    @staticmethod
    def bernstein(i, n, t):
        return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

    @staticmethod
    def bezier_point(t, points):
        n = len(points) - 1
        x, y = 0, 0
        for i, point in enumerate(points):
            x += Bezier.bernstein(i, n, t) * point.x
            y += Bezier.bernstein(i, n, t) * point.y
        return (x, y)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
