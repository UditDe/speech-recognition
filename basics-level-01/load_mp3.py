from pydub import AudioSegment as ads

audio = ads.from_wav("output.wav")

audio = audio + 9  # this is how to increase the volume by 9dB
'''
audio = audio * 2  # repeate twice
'''

audio = audio.fade_in(2000)

audio.export("mashup.mp3", format="mp3")

audio2 = ads.from_mp3("mashup.mp3")

print("done")
