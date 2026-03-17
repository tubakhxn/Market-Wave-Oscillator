import numpy as np

class WaveGenerator:
    def __init__(self, freqs=[0.1, 0.25, 0.5], amps=[1.0, 0.5, 0.25], noise_level=0.1, sample_rate=60):
        self.freqs = freqs
        self.amps = amps
        self.noise_level = noise_level
        self.sample_rate = sample_rate
        self.t = 0

    def next(self, n=1):
        t = np.arange(self.t, self.t + n) / self.sample_rate
        signal = np.zeros_like(t)
        for amp, freq in zip(self.amps, self.freqs):
            signal += amp * np.sin(2 * np.pi * freq * t)
        noise = np.random.normal(0, self.noise_level, size=t.shape)
        self.t += n
        result = signal + noise
        if n == 1:
            return float(result[0])
        return result

    def reset(self):
        self.t = 0
