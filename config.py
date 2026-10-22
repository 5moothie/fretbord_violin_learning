from util.notes.notes import notes


config = {
  # violyn settings
  "Positions": [1],
  "Acceptable_point_margin": 25,

  # note settings
  "Notes": notes,
  "Repeat_notes_consequently": False,

  # actionable audio settings
  "Min_sound_volume": 0.01,

  # Technical audio settings
  "SAMPLE_RATE": 44100,
  "BLOCK_SIZE": 4096,

  "NOTE_LISTEN_DURATION": .1,
  "NOTE_CORRECT_DURATION": .5,
  "NOTE_CORRECTNESS_THRESHOLD": .7,
}