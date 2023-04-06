import wave
import matplotlib.pyplot as plt
import numpy as np

audio_sample = wave.open("samplemusic.wav", "rb")

sample_frequency = audio_sample.getframerate()
sample_number = audio_sample.getnframes()
signal_wave = audio_sample.readframes(-1)

audio_sample.close()

sample_audio_time = sample_number / sample_frequency;
print(sample_audio_time)

signal_array = np.frombuffer(signal_wave, dtype=np.int16)

times = np.linspace(0, sample_audio_time, num=sample_number)

plt.figure(figsize=(15,5))
plt.plot(times, signal_array)
plt.title("Audio Signal")
plt.ylabel("Signal Wave")
plt.xlabel("Time (sec)")
plt.xlim(0, sample_audio_time)
plt.show()
