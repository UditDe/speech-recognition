import sys
from api_communication import *

filename = sys.argv[1]

audio_url = upload(filename)
save_transcript(audio_url, filename)

# print("Our data => \n", data)
# print("Error => \n", error)
