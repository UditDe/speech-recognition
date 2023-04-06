import pyaudio as pyAd
import wave as wv


###
FRAMES_PER_BUFFER = 3200
FORMAT = pyAd.paInt16
CHANNELS = 1
RATE = 16000

# creating a pyaudio object
P = pyAd.PyAudio()

# creating an audio stream
stream = P.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

print("Start Recording")

seconds = 10
frames = []

# starting the record

for i in range(0, int(RATE/FRAMES_PER_BUFFER * seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

stream.stop_stream()
stream.close()
P.terminate()

# saving the record

obj = wv.open("output.wav", "wb")
obj.setnchannels(CHANNELS)
obj.setsampwidth(P.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b"".join(frames))
obj.close()
