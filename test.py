import os
import pyglet

def findSong(directory, file):
  fileList = os.listdir(directory)
  return [f for f in fileList if f.find(file) > -1]

ash = "never"
song = findSong('music/',ash)

pyglet.resource.path = ['.','./music']
pyglet.resource.reindex()

player = pyglet.media.ManagedSoundPlayer()

song = pyglet.resource.media(str(song[0]))

player.queue(song)
player.play()

