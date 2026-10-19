import numpy as np

def get_dominant_frequency(samples, sample_rate):
  signal = samples.flatten()

  windowed_signal = signal * np.hanning(len(signal))

  fft_spectrum = np.abs(np.fft.rfft(windowed_signal))

  frequencies = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate)

  peak_index = np.argmax(fft_spectrum)

  dominant_freq = frequencies[peak_index]
  return dominant_freq