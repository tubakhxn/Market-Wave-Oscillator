import sys
import subprocess
import importlib
from pathlib import Path

def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_requirements(requirements_path):
    with open(requirements_path) as f:
        for line in f:
            pkg = line.strip().split('==')[0].split('>=')[0]
            if pkg:
                install_and_import(pkg)

if __name__ == "__main__":
    req_path = Path(__file__).parent / "requirements.txt"
    check_requirements(req_path)

    from wave_generator import WaveGenerator
    from visualization import MarketWaveVisualizer

    # Adjustable parameters
    freqs = [0.08, 0.18, 0.37]
    amps = [1.0, 0.7, 0.3]
    noise_level = 0.13
    sample_rate = 60
    window = 300
    fps = 60
    trail_decay = 0.97
    glow_layers = 6

    wave_gen = WaveGenerator(freqs=freqs, amps=amps, noise_level=noise_level, sample_rate=sample_rate)
    vis = MarketWaveVisualizer(wave_gen, window=window, fps=fps, trail_decay=trail_decay, glow_layers=glow_layers)
    vis.animate()
