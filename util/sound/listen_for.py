from config import config
from util.sound.dominant_freq import get_dominant_frequency

import numpy as np
import sounddevice as sd

SAMPLE_RATE = config["SAMPLE_RATE"]
BLOCK_SIZE = config["BLOCK_SIZE"]
MIN_VOLUME = config["Min_sound_volume"]

def listen_for_note(note):
  print("Listening")

  max_ = 0

  with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE) as stream:
    while True:
      samples, _ = stream.read(BLOCK_SIZE)
      volume = np.sqrt(np.mean(samples**2))

      if(volume < MIN_VOLUME):
        print(f"What the fuck, are you an acapella group? Play the fucking instrument! (louder)")
        continue

      print(get_dominant_frequency(samples, SAMPLE_RATE))

      


      
      
      
