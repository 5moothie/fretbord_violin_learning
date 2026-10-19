from config import config
from util.notes.noteGenerator import generateNote
import msvcrt

if __name__ == '__main__':
  while(True):
    print(generateNote())
    print("Space to continue, q to quit")

    c = msvcrt.getch().decode('utf-8')

    match c:
      case " ":
        continue
      case "q":
        break
      case _:
        print("Space to continue, q to quit")
