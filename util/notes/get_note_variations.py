from config import config
from util.notes.notes import notes_positions

def get_note_variations(note):
  variations = set()
  position_names = {
    1: "first",
  }
  for position in config["Positions"]:
    position_name = position_names.get(position, str(position))
    position_notes = notes_positions.get(f"{position_name}_position", {})
    variations.update(position_notes.get(note, set()))
  return sorted(variations)