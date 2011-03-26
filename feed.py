import os
import time
import facebook
import simplejson as json
import pyglet
#from dateutil.parser import *
#from dateutil.tz import *
#from datetime import *

access_token = '201793946507565%7Cd202ecd7aef8dbce66e1e6e0-100002268818038%7CiHYYQSxjEu1_O2cltKLULG-7jL8' # LifeOf TheParty
event_id = '130842913653732'  # Hackathon

last_song = None


def findSong(directory, file):
	fileList = os.listdir(directory)
	return [f for f in fileList if f.find(file) > -1]

pyglet.resource.path = ['.','./music']
pyglet.resource.reindex()

player = None
songs_to_queue = []
last_played = None


play = None

def new_song():
  global last_played
  graph = facebook.GraphAPI(access_token)
  global player
  global play
  player = pyglet.media.ManagedSoundPlayer()

  posts = graph.get_connections(event_id, 'feed')['data']
  postTotal = len(posts)-1
  temp = 0
  posted_time = time.strptime(posts[temp]['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
  while temp != postTotal:
    if posted_time >= last_played:
      temp = temp + 1
  while temp >= 0:
    if posted_time > last_played and str(posts[temp]['message']).find('Play ') != -1:
      music = posts[temp]['message'].replace('Play ','')
      song = findSong('music/' , music)
      print str(song)
      play = pyglet.resource.media(str(song[0]))
      player.queue(play)
      #pyglet.clock.schedule_once(new_song_load,play.duration)
			pyglet.clock.schedule_once(new_song_load,20)
      last_played = posted_time
    else:
      temp = temp - 1;
  #pyglet.clock.schedule_once(new_song_load,20)
  player.play()
  #else:
  #player.stop()

def new_song_load(dt):
  global last_song
  if player != None:
    player.stop()
  new_song()

new_song()
pyglet.app.run()
