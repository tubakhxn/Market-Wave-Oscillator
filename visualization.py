import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils.color_utils import get_color_gradient, get_glow_colors
from wave_layers import generate_wave_layers

class VolatilitySurfaceVisualizer:
    def __init__(self, n_layers=20, n_points=400, glow_lines=6):
        self.n_layers = n_layers
        self.n_points = n_points
        self.glow_lines = glow_lines
        self.x = np.linspace(0, 2 * np.pi, n_points)
        self.layers = generate_wave_layers(
            n_layers, self.x,
            amp_range=(0.2, 1.0),
            freq_range=(1.0, 3.0),
            phase_range=(0, 2 * np.pi),
            v_offset_range=(-1.5, 1.5)
        )
        # Color gradient: blue to magenta
        self.colors = get_color_gradient((0.1, 0.5, 1.0), (1.0, 0.2, 0.8), n_layers)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_facecolor('#181c20')
        self.fig.patch.set_facecolor('#181c20')
        self.ax.set_xlim(self.x[0], self.x[-1])
        self.ax.set_ylim(-2.5, 2.5)
        self.ax.axis('off')
        self.ax.set_title('Volatility Surface Wave', color='w', fontsize=20, pad=20)
        self.lines = [self.ax.plot([], [], lw=2.5, color=self.colors[i], alpha=0.85)[0] for i in range(n_layers)]
        # For glow effect, store extra line handles per layer
        self.glow_handles = [
            [self.ax.plot([], [], lw=6 + 2 * g, color=self.colors[i], alpha=0.08)[0] for g in range(glow_lines)]
            for i in range(n_layers)
        ]

    def init(self):
        for line in self.lines:
            line.set_data([], [])
        for glow_group in self.glow_handles:
            for glow in glow_group:
                glow.set_data([], [])
        return self.lines + [g for group in self.glow_handles for g in group]

    def animate(self, frame):
        t = frame * 0.04
        cam_offset = 0.15 * np.sin(0.2 * t)  # Camera illusion
        cam_scale = 1.0 + 0.03 * np.sin(0.13 * t)
        for i, layer in enumerate(self.layers):
            y = layer.get_y(t) * cam_scale + cam_offset
            # Main line
            self.lines[i].set_data(self.x, y)
            self.lines[i].set_alpha(0.85 * (0.5 + 0.5 * (i + 1) / self.n_layers))
            self.lines[i].set_linewidth(2.5 + 1.5 * (i / self.n_layers))
            # Glow lines
            for g, glow in enumerate(self.glow_handles[i]):
                glow.set_data(self.x, y)
                glow.set_alpha(0.08 * (1 - g / self.glow_lines))
                glow.set_linewidth(6 + 2 * g + 2 * (i / self.n_layers))
        return self.lines + [g for group in self.glow_handles for g in group]

    def show(self):
        anim = FuncAnimation(
            self.fig, self.animate, init_func=self.init,
            frames=100000, interval=33, blit=True
        )
        plt.show()
