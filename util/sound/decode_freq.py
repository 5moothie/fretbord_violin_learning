from config import config

import sounddevice as sd

SAMPLE_RATE = config["SAMPLE_RATE"]
BLOCK_SIZE = config["BLOCK_SIZE"]

def listen():
  print("Listening")