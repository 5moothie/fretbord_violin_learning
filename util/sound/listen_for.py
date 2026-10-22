from collections import Counter, defaultdict

from config import config
from util.sound.dominant_freq import get_fundamental_frequency_librosa
from util.notes.frequency_to_note import frequency_to_note

import numpy as np
import sounddevice as sd
import time

SAMPLE_RATE = config["SAMPLE_RATE"]
BLOCK_SIZE = config["BLOCK_SIZE"]
MIN_VOLUME = config["Min_sound_volume"]
LISTEN_DURATION = config["NOTE_LISTEN_DURATION"]

def create_input_stream():
  return sd.InputStream(
    channels=1,
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
  )


def listen_for_note(stream):
  detected_notes = []
  cents_by_note = defaultdict(list)

  end_time = time.monotonic() + LISTEN_DURATION
  while time.monotonic() < end_time:
    samples, _ = stream.read(BLOCK_SIZE)
    volume = np.sqrt(np.mean(samples**2))

    if volume < MIN_VOLUME:
      continue

    frequency = get_fundamental_frequency_librosa(samples, SAMPLE_RATE)
    converted_note = frequency_to_note(frequency)
    if converted_note is None:
      continue

    detected_note, cents = converted_note
    detected_notes.append(detected_note)
    cents_by_note[detected_note].append(float(cents))

  if not detected_notes:
    return None

  dominant_note = Counter(detected_notes).most_common(1)[0][0]
  average_cents = sum(cents_by_note[dominant_note]) / len(cents_by_note[dominant_note])
  result = dominant_note, average_cents

  return result
