import numpy as np

def apply_trail_alpha(length, trail_decay=0.95, min_alpha=0.05):
    """
    Returns an array of alpha values for a trail effect.
    Newest point has alpha=1, oldest approaches min_alpha.
    """
    if length == 0:
        return np.array([])
    idx = np.arange(length)[::-1]
    alpha = trail_decay ** idx
    alpha = min_alpha + (1 - min_alpha) * alpha / alpha.max()
    return alpha

def get_glow_lines(y, n_layers=6, base_alpha=0.18, width_step=1.5):
    """
    Returns a list of (y, alpha, linewidth) for glow layering.
    """
    lines = []
    for i in range(n_layers):
        alpha = base_alpha * (1 - i / n_layers)
        lw = 2.5 + i * width_step
        lines.append((y, alpha, lw))
    return lines
