from util.notes.notes import notes

import numpy as np

def frequency_to_note(frequency):
  if frequency is None or frequency <= 0:
    return None

  midi_note = round(69 + 12 * np.log2(frequency / 440.0))

  note_name = notes[midi_note % 12]
  octave = midi_note // 12 - 1

  target_frequency = 440.0 * 2 ** ((midi_note - 69) / 12)
  cents = 1200 * np.log2(frequency / target_frequency)

  return f"{note_name}{octave}", cents