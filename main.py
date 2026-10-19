from config import config
from util.notes.noteGenerator import generateNote

import msvcrt

from util.sound.listen_for import listen_for_note

if __name__ == '__main__':
  
  while(True):
    note = generateNote()
    print(f"Play {note}", end='\r')

    listen_for_note(note)