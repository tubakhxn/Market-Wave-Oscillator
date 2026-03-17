import numpy as np

# Color gradient utilities for smooth transitions

def get_color_gradient(start_color, end_color, n_layers):
    """
    Generate a list of colors forming a gradient between start_color and end_color.
    Colors are in RGB tuple format (0-1 floats).
    """
    start = np.array(start_color)
    end = np.array(end_color)
    return [tuple(start + (end - start) * i / (n_layers - 1)) for i in range(n_layers)]


def get_glow_colors(base_color, n_glow, alpha_max=0.25):
    """
    Generate a list of RGBA colors for glow effect, fading outwards.
    """
    base = np.array(base_color)
    return [tuple(base) + (alpha_max * (1 - i / n_glow),) for i in range(n_glow)]
