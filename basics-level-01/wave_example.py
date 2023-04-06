import wave

###### Reading the data from that .wav file #######
obj = wave.open("samplemusic.wav", "rb")

print("number of channels", obj.getnchannels())
print("sample width", obj.getsampwidth())
print("frame rate", obj.getframerate())
print("number of frames", obj.getnframes())
print("parameteres", obj.getparams())

timeOfAudio =  obj.getnframes() / obj.getframerate()
print("\n ", timeOfAudio)

frames = obj.readframes(-1) #doing this we get all the frames
print(type(frames), type(frames[0]))
print(len(frames)) #this is exactly doubled of number of frame as sample width is 2
print(len(frames) / obj.getsampwidth())

obj.close()


##### Writing the data / Coping the data to another file #####
new_object = wave.open("newSampleMusic.wav", "wb")

new_object.setnchannels(obj.getnchannels())
new_object.setsampwidth(obj.getsampwidth())
new_object.setframerate(obj.getframerate())
new_object.writeframes(frames)

new_object.close()

