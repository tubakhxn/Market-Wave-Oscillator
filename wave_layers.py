import numpy as np

class WaveLayer:
    def __init__(self, x, amplitude, frequency, phase, vertical_offset):
        self.x = x
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.vertical_offset = vertical_offset

    def get_y(self, t):
        # Sine wave with time-evolving phase
        return self.amplitude * np.sin(self.frequency * self.x + self.phase + t) + self.vertical_offset


def generate_wave_layers(n_layers, x, amp_range=(0.2, 1.0), freq_range=(1.0, 3.0), phase_range=(0, 2*np.pi), v_offset_range=(0, 1)):
    """
    Generate a list of WaveLayer objects with varying parameters.
    """
    amps = np.linspace(amp_range[0], amp_range[1], n_layers)
    freqs = np.linspace(freq_range[0], freq_range[1], n_layers)
    phases = np.linspace(phase_range[0], phase_range[1], n_layers)
    v_offsets = np.linspace(v_offset_range[0], v_offset_range[1], n_layers)
    layers = [WaveLayer(x, amps[i], freqs[i], phases[i], v_offsets[i]) for i in range(n_layers)]
    return layers
