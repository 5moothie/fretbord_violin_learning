import numpy as np

def get_dominant_frequency(samples, sample_rate):
  signal = samples.flatten()

  windowed_signal = signal * np.hanning(len(signal))

  fft_spectrum = np.abs(np.fft.rfft(windowed_signal))

  frequencies = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate)

  peak_index = np.argmax(fft_spectrum)

  dominant_freq = frequencies[peak_index]
  return dominant_freq

import numpy as np


def get_fundamental_frequency(samples, sample_rate):
    signal = np.asarray(samples, dtype=np.float64)

    # Convert stereo audio to mono if necessary.
    if signal.ndim > 1:
        signal = signal.mean(axis=-1)

    signal = signal.flatten()

    # Remove the DC offset.
    signal -= np.mean(signal)

    # Ignore silence.
    if np.sqrt(np.mean(signal ** 2)) < 1e-6:
        return None

    # Skip the zero-lag result and limit the lag to half the signal length.
    min_lag = 2
    max_lag = len(signal) // 2
    if min_lag >= max_lag:
        return None

    # Calculate the difference function.
    difference = np.zeros(max_lag + 1)

    for lag in range(1, max_lag + 1):
        delta = signal[:-lag] - signal[lag:]
        difference[lag] = np.dot(delta, delta)

    # Cumulative mean normalized difference function (YIN).
    cumulative = np.cumsum(difference[1:])

    cmnd = np.ones_like(difference)
    cmnd[1:] = (
        difference[1:] * np.arange(1, len(difference))
        / (cumulative + 1e-12)
    )

    # Find the first convincing period candidate.
    threshold = 0.15
    candidates = np.flatnonzero(
        cmnd[min_lag:max_lag + 1] < threshold
    )
    
    if len(candidates) > 0:
        lag = min_lag + candidates[0]

        # Follow the curve to its local minimum.
        while lag < max_lag and cmnd[lag + 1] < cmnd[lag]:
            lag += 1
    else:
        # Use the best candidate only if confidence is reasonable.
        lag = min_lag + np.argmin(cmnd[min_lag:max_lag + 1])
        if cmnd[lag] > 0.35:
            return None
        
    # Refine the period estimate for better frequency accuracy.
    if min_lag < lag < max_lag:
        left = cmnd[lag - 1]
        middle = cmnd[lag]
        right = cmnd[lag + 1]

        denominator = left - 2 * middle + right

        if abs(denominator) > 1e-12:
            lag = lag + 0.5 * (left - right) / denominator

    return sample_rate / lag