# gttsExample.py
# quick example with the gtts engine.

import gtts
import os

tts = gtts.gTTS(text="hello there", lang="en")
tts.save("greeting.mp3")
os.system("gtts-cli 'hello' -|'en' -o greeting.mp3")