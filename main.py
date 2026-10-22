from collections import Counter, deque
from math import ceil

from config import config
from util.notes.noteGenerator import generateNote
from util.sound.listen_for import listen_for_note
from util.sound.listen_for import create_input_stream
from util.display_status import display_status
from util.notes.get_note_variations import get_note_variations


if __name__ == "__main__":
  current_note = generateNote()
  played_notes = set()
  suggested_note = None
  detected_note = None
  average_cents = None
  correct_duration = 0.0
  correct_note_history = deque()
  listen_duration = config["NOTE_LISTEN_DURATION"]
  correct_note_duration = config["NOTE_CORRECT_DURATION"]
  correctness_threshold = config["NOTE_CORRECTNESS_THRESHOLD"]
  acceptable_cents = config["Acceptable_point_margin"]
  required_samples = max(1, ceil(correct_note_duration / listen_duration))

  with create_input_stream() as stream:
    while True:
      display_status(
        current_note,
        played_notes,
        detected_note,
        average_cents,
        suggested_note,
        correct_duration,
        correct_note_duration,
      )

      result = listen_for_note(stream)
      if result is None:
        detected_note = None
        average_cents = None
        correct_note_history.append(None)
        if len(correct_note_history) > required_samples:
          correct_note_history.popleft()
        correct_duration = min(
          len(correct_note_history) * listen_duration,
          correct_note_duration,
        )
        continue

      detected_note, average_cents = result
      note_name = detected_note.rstrip("0123456789")

      if suggested_note is not None:
        if (note_name == suggested_note
            and abs(average_cents) <= acceptable_cents):
          current_note = suggested_note
          played_notes = set()
          suggested_note = None
          correct_duration = 0.0
          correct_note_history.clear()
        continue

      is_correct_note = (
        note_name == current_note
        and abs(average_cents) <= acceptable_cents
      )
      correct_note_history.append(
        detected_note if is_correct_note else None
      )
      if len(correct_note_history) > required_samples:
        correct_note_history.popleft()

      correct_duration = min(
        len(correct_note_history) * listen_duration,
        correct_note_duration,
      )
      if len(correct_note_history) < required_samples:
        continue

      variation_counts = Counter(
        variation for variation in correct_note_history
        if variation is not None
      )
      if not variation_counts:
        continue

      variation, count = variation_counts.most_common(1)[0]
      if count / len(correct_note_history) < correctness_threshold:
        continue

      played_notes.add(variation)
      correct_duration = 0.0
      correct_note_history.clear()

      current_variations = set(get_note_variations(current_note))
      if current_variations and played_notes == current_variations:
        suggested_note = generateNote()