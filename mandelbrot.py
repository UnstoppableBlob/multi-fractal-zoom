import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import matplotlib.colors as mcolors

def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def julia(c, z, max_iter):
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def draw_image(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return (r1, r2, np.array([[mandelbrot(complex(r, i), max_iter) for r in r1] for i in r2]))

def draw_julia_image(xmin, xmax, ymin, ymax, width, height, max_iter, c):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return (r1, r2, np.array([[julia(c, complex(r, i), max_iter) for r in r1] for i in r2]))

class FractalGUI:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Fractal Selection')
        self.fractal_options = ['Mandelbrot', 'Julia (c=-0.8+0.156i)', 'Julia (c=0.355+0.355i)', 'Julia (c=-0.70176-0.3842i)']
        self.fractal_choice = self.fractal_options[0]

        self.rax = plt.axes([0.025, 0.5, 0.50, 0.25])
        self.radio = RadioButtons(self.rax, self.fractal_options)
        self.radio.on_clicked(self.update_fractal)

        self.draw_button_ax = plt.axes([0.025, 0.4, 0.15, 0.075])
        self.draw_button = Button(self.draw_button_ax, 'Draw Fractal')
        self.draw_button.on_clicked(self.draw_fractal)


        self.fig.canvas.manager.set_window_title('Fractal Selection')
        self.fig.canvas.manager.resize(800, 600)  # set the window size
        plt.show()

    def update_fractal(self, label):
        self.fractal_choice = label

    def draw_fractal(self, event):
        if self.fractal_choice == 'Mandelbrot':
            self.draw_mandelbrot()
        elif self.fractal_choice.startswith('Julia'):
            self.draw_julia()

    def draw_mandelbrot(self):
        center_x, center_y = -0.743643887037151, 0.13182590420533
        zoom_factor = 1.5
        num_frames = 30

        plt.clf()

        for i in range(num_frames):
            zoom_width = zoom_factor / (2 ** i)
            zoom_height = zoom_width * (3 / 4)

            xmin, xmax = center_x - zoom_width, center_x + zoom_width
            ymin, ymax = center_y - zoom_height, center_y + zoom_height

            x, y, d = draw_image(xmin, xmax, ymin, ymax, 1000, 1000, 256 + i * 10)

            plt.clf()
            plt.imshow(d, extent=(xmin, xmax, ymin, ymax), cmap='plasma', norm=mcolors.PowerNorm(gamma=0.6))
            plt.title(f"Mandelbrot Set (Zoom Level {i + 1})")
            plt.colorbar(label="Iteration Count")
            plt.draw()
            plt.pause(0.1)
            plt.clf()

    def draw_julia(self):
        center_x, center_y = 0, 0
        zoom_factor = 1.5
        num_frames = 30
        c = 0
        if self.fractal_choice == 'Julia (c=-0.8+0.156i)':
            c = -0.8 + 0.156j
        elif self.fractal_choice == 'Julia (c=0.355+0.355i)':
            c = 0.355 + 0.355j
        elif self.fractal_choice == 'Julia (c=-0.70176-0.3842i)':
            c = -0.70176 - 0.3842j
        else:
            print("Invalid fractal choice???")
            return

        plt.clf()

        for i in range(num_frames):
            zoom_width = zoom_factor / (2 ** i)
            zoom_height = zoom_width * (3 / 4)

            xmin, xmax = center_x - zoom_width, center_x + zoom_width
            ymin, ymax = center_y - zoom_height, center_y + zoom_height

            x, y, d = draw_julia_image(xmin, xmax, ymin, ymax, 1000, 1000, 256 + i * 10, c)

            plt.clf()
            plt.imshow(d, extent=(xmin, xmax, ymin, ymax), cmap='viridis', norm=mcolors.PowerNorm(gamma=0.6))
            plt.title(f"Julia Set with c = {c} (Zoom Level {i + 1})")
            plt.colorbar(label="Iteration Count")
            plt.draw()
            plt.pause(0.1)
            plt.clf()


FractalGUI()
