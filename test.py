import os
import audiere

def findSong(directory, file):
  fileList = os.listdir(directory)
  return [f for f in fileList if f.find(file) > -1]

tesss = audiere.get_devices()
print tesss
d = audiere.open_device()

#get request

ash = "nevergoingtogiveyouup"
song = findSong('/music', ash)
l = d.open_file('/music'+ash+'.mp3')
l.repeating = 1
l.play()

