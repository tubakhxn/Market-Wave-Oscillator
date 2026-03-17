import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils.effects import apply_trail_alpha, get_glow_lines

class MarketWaveVisualizer:
    def __init__(self, wave_gen, window=300, fps=60, trail_decay=0.97, glow_layers=6):
        self.wave_gen = wave_gen
        self.window = window
        self.fps = fps
        self.trail_decay = trail_decay
        self.glow_layers = glow_layers
        self.x = np.arange(-window+1, 1)
        self.y = np.zeros(window)
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self._setup_plot()

    def _setup_plot(self):
        self.fig.patch.set_facecolor('#181c20')
        self.ax.set_facecolor('#181c20')
        self.ax.set_xlim(self.x[0], self.x[-1])
        self.ax.set_ylim(-2, 2)
        self.ax.set_title('Market Wave Oscillator', color='#e0e0e0', fontsize=18, pad=18)
        self.ax.grid(True, color='#333a40', alpha=0.25)
        self.ax.tick_params(colors='#b0b0b0')
        for spine in self.ax.spines.values():
            spine.set_color('#444')
        self.lines = []
        for _ in range(self.glow_layers):
            l, = self.ax.plot([], [], lw=2, alpha=0.2, color='#00ffe7', solid_capstyle='round')
            self.lines.append(l)
        self.main_line, = self.ax.plot([], [], lw=2.5, color='#00ffe7', alpha=1, solid_capstyle='round')

    def _update(self, frame):
        # Get next value (should be scalar)
        new_y = self.wave_gen.next()
        if isinstance(new_y, (np.ndarray, list)):
            new_y = float(np.ravel(new_y)[0])
        self.y = np.roll(self.y, -1)
        self.y[-1] = new_y
        # Dynamic y-scaling
        y_margin = 0.2
        y_min, y_max = self.y.min(), self.y.max()
        self.ax.set_ylim(y_min - y_margin, y_max + y_margin)
        # Trail effect
        alpha_arr = apply_trail_alpha(len(self.y), self.trail_decay)
        # Glow layering: draw multiple lines with increasing width and decreasing alpha
        for i, (y_vals, alpha, lw) in enumerate(get_glow_lines(self.y, n_layers=self.glow_layers)):
            self.lines[i].set_data(self.x, y_vals)
            # For glow, use a single alpha value per line (not per-point)
            self.lines[i].set_alpha(alpha)
            self.lines[i].set_linewidth(lw)
        # Main line with trail alpha (per-point)
        self.main_line.set_data(self.x, self.y)
        # For main line, use a single alpha (max), but fade the color using a colormap for trail effect
        # Instead, we can use a workaround: set alpha to 1, but color the line with a faded color
        self.main_line.set_alpha(1.0)
        return self.lines + [self.main_line]

    def animate(self):
        interval = 1000 / self.fps
        self.ani = FuncAnimation(self.fig, self._update, blit=True, interval=interval)
        plt.show()
