import os
import time
import facebook
import simplejson as json
import pyglet

access_token = '201793946507565%7Cd202ecd7aef8dbce66e1e6e0-100002268818038%7CiHYYQSxjEu1_O2cltKLULG-7jL8' # LifeOf TheParty
event_id = '130842913653732'  # Hackathon

global last_song

def findSong(directory, file):
	fileList = os.listdir(directory)
	return [f for f in fileList if f.find(file) > -1]

pyglet.resource.path = ['.','./music']
pyglet.resource.reindex()

player = None


def new_song():
	graph = facebook.GraphAPI(access_token)
	
	penis = graph.get_connections(event_id, 'feed')['data']
	
	shit = str(penis[0]['message'])
	if shit != last_song:
	  last_song = shit
	  if shit.find('Play ') != -1:
		  music = shit.replace('Play ','')
		  song = findSong('music/' , music)
	    print str(song)
	  global player
	  player = pyglet.media.ManagedSoundPlayer()
	  play = pyglet.resource.media(str(song[0]))
	  player.queue(play)
	  pyglet.clock.schedule_once(new_song_load,play.duration)
	  #pyglet.clock.schedule_once(new_song_load,20)
	  player.play()
	else:
	  player.stop()

def new_song_load(dt):
	global player
	if player != None:
		player.stop()
	new_song()

new_song()
pyglet.app.run()
