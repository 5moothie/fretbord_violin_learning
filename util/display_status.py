from util.notes.get_note_variations import get_note_variations

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
ERASE_LINE = "\033[2K"
CURSOR_UP = "\033[4A"

_static_signature = None
_has_output = False


def _format_pitch_bar(average_cents):
  width = 61
  centre = width // 2
  if average_cents is None:
    marker = centre
  else:
    cents = max(-50.0, min(50.0, average_cents))
    marker = round((cents + 50) / 100 * (width - 1))

  return marker


def _dynamic_lines(current_note, detected_note, average_cents, correct_duration,
                   correct_note_duration):
  if detected_note is None:
    playing_line = "Currently playing: -"
  else:
    playing_line = (
      f"Currently playing: {detected_note} "
      f"({average_cents:+.1f} cents)"
    )

  marker = _format_pitch_bar(average_cents)
  generic_note = (
    detected_note.rstrip("0123456789")
    if detected_note is not None
    else current_note
  )
  labels = [" "] * 61
  for position, label in ((0, "-50"), (15, "-25"), (30, generic_note),
                          (45, "+25"), (58, "+50")):
    labels[position:position + len(label)] = label
  pitch_line = "  " + "".join(labels)
  marker_line = f"  {' ' * marker}^"
  progress_line = (
    f"Correct duration: {correct_duration:.1f}/"
    f"{correct_note_duration:.1f} seconds"
  )
  return playing_line, pitch_line, marker_line, progress_line


def display_status(current_note, played_notes, detected_note, average_cents,
                   suggested_note=None, correct_duration=0.0,
                   correct_note_duration=1.0):
  global _static_signature, _has_output

  static_signature = (
    current_note,
    frozenset(played_notes),
    suggested_note,
  )
  if static_signature != _static_signature:
    print("\033[2J\033[H", end="")
    print(f"Play: {current_note}")
    print()
    print(f"{current_note} variations:")

    for variation in get_note_variations(current_note):
      colour = GREEN if variation in played_notes else RED
      status = "played" if variation in played_notes else "not played"
      print(f"  {colour}{variation}: {status}{RESET}")

    print()
    if suggested_note is not None:
      print(f"Next note: {suggested_note}")
    _static_signature = static_signature
    _has_output = False

  lines = _dynamic_lines(
    current_note,
    detected_note,
    average_cents,
    correct_duration,
    correct_note_duration,
  )
  if _has_output:
    print(CURSOR_UP, end="")

  for line in lines:
    print(ERASE_LINE + line)
  print(ERASE_LINE, end="", flush=True)
  _has_output = True
