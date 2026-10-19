from config import config

import random

repeat_notes_consequently = config["Repeat_notes_consequently"]
notes_ = config["Notes"]
previous = None


def generateNote():
  if(repeat_notes_consequently):
    return random.choice(notes_)

  else:
    global previous
          
    if previous and len(notes_) > 1:
      n_notes = [note for note in notes_ if note != previous]
      chosenNote = random.choice(n_notes)
    else:
      chosenNote = random.choice(notes_)

    previous = chosenNote
    return chosenNote
