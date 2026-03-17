from visualization import VolatilitySurfaceVisualizer

if __name__ == "__main__":
    visualizer = VolatilitySurfaceVisualizer(
        n_layers=24,  # visually rich
        n_points=500, # smooth
        glow_lines=7  # strong glow
    )
    visualizer.show()
