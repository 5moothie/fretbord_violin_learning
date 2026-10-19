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
  pending_variation = None
  listen_duration = config["NOTE_LISTEN_DURATION"]
  correct_note_duration = config["NOTE_CORRECT_DURATION"]
  acceptable_cents = config["Acceptable_point_margin"]

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
        correct_duration = 0.0
        pending_variation = None
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
          pending_variation = None
        continue

      if (note_name != current_note
          or abs(average_cents) > acceptable_cents):
        correct_duration = 0.0
        pending_variation = None
        continue

      if pending_variation == detected_note:
        correct_duration += listen_duration
      else:
        pending_variation = detected_note
        correct_duration = listen_duration

      if correct_duration < correct_note_duration:
        continue

      played_notes.add(pending_variation)
      correct_duration = 0.0
      pending_variation = None

      current_variations = set(get_note_variations(current_note))
      if current_variations and played_notes == current_variations:
        suggested_note = generateNote()