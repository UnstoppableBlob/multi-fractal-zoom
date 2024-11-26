import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import matplotlib.colors as mcolors

# These are the functions to calculate the sets... I think they're correct

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

def burning_ship(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = complex(abs(z.real), abs(z.imag))**2 + c
    return max_iter

def multibrot(c, max_iter, d):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**d + c
    return max_iter

def tricorn(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = np.conj(z)**2 + c
    return max_iter

def celtic_mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z*z + c
    return max_iter

def draw_image(xmin, xmax, ymin, ymax, width, height, max_iter, fractal_func, *args):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return (r1, r2, np.array([[fractal_func(complex(r, i), max_iter, *args) for r in r1] for i in r2]))

class FractalGUI:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Fractal Selection')
        self.fractal_options = [
            'Mandelbrot',
            'Julia (c=-0.8+0.156i)',
            'Julia (c=0.355+0.355i)',
            'Julia (c=-0.70176-0.3842i)',
            'Burning Ship',
            'Multibrot (d=3)',
            'Multibrot (d=4)',
            'Tricorn',
            'Celtic Mandelbrot'
        ]
        self.fractal_choice = self.fractal_options[0]

        self.rax = plt.axes([0.025, 0.5, 0.50, 0.3])
        self.radio = RadioButtons(self.rax, self.fractal_options)
        self.radio.on_clicked(self.update_fractal)

        self.draw_button_ax = plt.axes([0.025, 0.4, 0.15, 0.075])
        self.draw_button = Button(self.draw_button_ax, 'Draw Fractal')
        self.draw_button.on_clicked(self.draw_fractal)

        mng = plt.get_current_fig_manager()
        mng.resize(800, 600)
        mng.window.resizable(False, False)

        plt.show()

    def update_fractal(self, label):
        self.fractal_choice = label

    def draw_fractal(self, event):
        if self.fractal_choice == 'Mandelbrot':
            self.draw_mandelbrot()
        elif self.fractal_choice.startswith('Julia'):
            self.draw_julia()
        elif self.fractal_choice == 'Burning Ship':
            self.draw_burning_ship()
        elif self.fractal_choice.startswith('Multibrot'):
            self.draw_multibrot()
        elif self.fractal_choice == 'Tricorn':
            self.draw_tricorn()
        elif self.fractal_choice == 'Celtic Mandelbrot':
            self.draw_celtic_mandelbrot()

    def draw_mandelbrot(self):
        self.animate_fractal(-0.53027761, -0.70669007, 1.5, mandelbrot, 'plasma')

    def draw_julia(self):
        c = 0
        if self.fractal_choice == 'Julia (c=-0.8+0.156i)':
            c = -0.8 + 0.156j
            self.animate_fractal(0, 0, 1.5, lambda z, max_iter: julia(c, z, max_iter), 'viridis')
        elif self.fractal_choice == 'Julia (c=0.355+0.355i)':
            c = 0.355 + 0.355j
            self.animate_fractal(0.024156, -0.179694, 1.5, lambda z, max_iter: julia(c, z, max_iter), 'viridis')
        elif self.fractal_choice == 'Julia (c=-0.70176-0.3842i)':
            c = -0.7102 - 0.3847j
            self.animate_fractal(0.130790, 0.182954, 1.5, lambda z, max_iter: julia(c, z, max_iter), 'viridis', 387) 

    def draw_burning_ship(self):
        # zoom into the largest ship
        self.animate_fractal(-1.7619, 0.028, 1.5, burning_ship, 'inferno')

    def draw_multibrot(self):
        d = 3 if self.fractal_choice == 'Multibrot (d=3)' else 4
        if d == 3:
            self.animate_fractal(-0.52615929, -0.07635728, 1.5, lambda c, max_iter: multibrot(c, max_iter, d), 'twilight', 387) 
        if d == 4:
            self.animate_fractal(-0.743643887037151, 0.13182590420533, 1.5, lambda c, max_iter: multibrot(c, max_iter, d), 'twilight') 

    def draw_tricorn(self):
        self.animate_fractal(-0.69318366, 0.13715734, 1.5, tricorn, 'twilight_shifted')

    def draw_celtic_mandelbrot(self):
        self.animate_fractal(-0.63933522, 0.25433522, 1.5, celtic_mandelbrot, 'cividis')

    def animate_fractal(self, center_x, center_y, zoom_factor, fractal_func, cmap, num_frames=387):
        plt.clf()

        for i in range(num_frames):
            zoom_width = zoom_factor / (1.033 ** i)  
            zoom_height = zoom_width * (3 / 4)

            xmin, xmax = center_x - zoom_width, center_x + zoom_width
            ymin, ymax = center_y - zoom_height, center_y + zoom_height

            x, y, d = draw_image(xmin, xmax, ymin, ymax, 1000, 1000, 256 + i * 10, fractal_func)

            plt.clf() # spamming this clears the buttons and stuff?

            plt.imshow(d, extent=(xmin, xmax, ymin, ymax), cmap=cmap, norm=mcolors.PowerNorm(gamma=0.6))
            plt.title(f"{self.fractal_choice} (Zoom Level {i + 1})")
            plt.colorbar(label="Iteration Count")
            plt.draw()
            plt.pause(0.1)
            plt.clf()


FractalGUI()
