import serial
import facebook
import re
import urllib
import time, math
import os
import numpy as np
import mlpy
import random
import alsaaudio, time, audioop

from time import sleep


access_token = '201793946507565%7Cd202ecd7aef8dbce66e1e6e0-100002268818038%7CiHYYQSxjEu1_O2cltKLULG-7jL8' # LifeOf TheParty
event_id = '130842913653732'  # Hackathon
imageLocation = 'capture.jpg'
quiet = True

ser = serial.Serial('/dev/ttyACM1', 9600)
co2 = serial.Serial('/dev/ttyUSB0', 115200)
meter = serial.Serial('/dev/ttyACM0', 9600)
sandwich = serial.Serial('/dev/ttyUSB2', 9600)

graph = facebook.GraphAPI(access_token)

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(2)
inp.setrate(100)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

tAVG=0
hAVG=0
cAVG=0

def readEnvironment():
  global tAVG
  global hAVG
  global cAVG
  for count in range(10):
	  co2.write('t')
	  co2.read(3)
	  b=co2.read()
	  a=co2.read()
	  temp=(((ord(a)<<8))*0.018)+32
	  temp=temp
	  co2.read()
	  co2.write('f')
	  co2.read(5)
	  #time.sleep(.01)
	  co2.write('r')
	  co2.read(4)
	  a=co2.read()
	  relHumid=(ord(a)<<8)/100
	  co2.read()
	  co2.write('d')
	  co2.read(5)
	  #time.sleep(.01)
	  co2.write('c')
	  cohtwo=0
	  co2.read(4)
	  #for i in range(2):
	  tmp=co2.read()
	  cohtwo= ord(tmp)<<8	
	  co2.read()
	  co2.write('e')
	  co2.read(5)
	  #time.sleep(.01)
	  tAVG+=temp
	  hAVG+=relHumid
	  cAVG+=cohtwo
  tAVG=tAVG/10
  hAVG=hAVG/10
  cAVG=cAVG/100



def postStatus(postMessage):
  if (quiet == False):
    print graph.put_object("me", "feed", message=postMessage)
  return

def postPicture():
  if (quiet == False):
    print 'Taking picture'
    os.system('python ./camera.py')
    os.system("curl -F 'access_token="+ access_token +"' -F 'source=@"+ imageLocation +"' -F 'message="+ strTime +"' https://graph.facebook.com/me/photos")
  return

def countLikes():
  numLikes = 0
  eventFeed = graph.get_connections(event_id, 'feed')
  for i in eventFeed['data']:
    if (i.has_key('likes')):
      print i['likes']['count']
      numLikes += int(i['likes']['count'])
  likeage = float(numLikes) / float(len(eventFeed['data']))
  print "Num likes: "+ str(numLikes) +', num posts: '+ str(float(len(eventFeed['data'])))
  print "Average: "+ str(likeage)
  return likeage

def updateLikeMeter(likeage):
  ser.write('r')
  ser.readline()
  ser.write('t')
  ser.readline()
  ser.write('y')
  ser.readline()
  if (likeage <= 0.33):
    ser.write('e')
  elif (likeage <= 0.66):
    ser.write('e')
    ser.write('w')
    ser.readline()
  else:
    ser.write('q')
    ser.write('e')
    ser.write('w')
    ser.readline()
    ser.readline()
  ser.readline()
  print 'Updated like meter.'
  return
  

def pollSound():
  global inp
  samples = []
  for i in range(0, 20):
    # Read data from device
    l,data = inp.read()
    if l:
      # Return the maximum of the absolute value of all samples in a fragment.
      #print audioop.max(data, 2)
      sample = float(audioop.max(data, 2))
      samples.append(sample)
      print sample
      time.sleep(.05)
  average = 0
  if (len(samples)):
    average = float(sum(samples)/len(samples))
  print 'Took sound samples. Level: '+ str(average)
  return average


def updateSoundMeter(soundLevel):
  db = 10*math.log10(soundLevel)
  if db <= 27:
    meterLevel = 0
  elif db <= 31:
    meterLevel = 1
  else:
    meterLevel = 2
  print 'Updating sound meter from db: '+ str(db) +' to level: ['+ str(meterLevel) +']'
  meter.write(str(meterLevel*60 + 30))

  return db
  

last_id = None
def checkSandwich():
  global last_id
  posts = graph.get_connections('me', 'feed')['data']
  last_status = posts[0] 
  if last_status['message'].find('Make me a sandwich.') != -1 and last_status['id'] != last_id:
    message = "What? Make it yourself."
    graph.put_object(last_status['id'], "comments", message=message)
  elif last_status['message'].find('Sudo make me a sandwich.') != -1 and last_status['id'] != last_id:
    message = "Okay."
    graph.put_object(last_status['id'], "comments", message=message)
    sandwich.write('m')
    sleep(2)
    sandwich.write('n')
  last_id = last_status['id']
  


# [temp, hum, co2, db]
def classifyParty(observList):
	toxtr=list()
	toytr = list()
	#temp humidity co2 dB
	#10 samples for chill party
	print observList
	for i in range(10):
		tempxtr=list()
		tempxtr=[72+random.triangular(-2, 3),10+random.triangular(-2,3), 63+random.triangular(-50,50), 27+random.triangular(-2,2)]
		toxtr.append(tempxtr)
		toytr.append(1)
	#10 samples for hopping party
	for i in range(10):
		tempxtr=list()
		tempxtr=[77+random.triangular(-2, 2), 16+random.triangular(-5,5), 65+random.triangular(-50,50), 30+random.triangular(-2,2)]
		toxtr.append(tempxtr)
		toytr.append(2)
	
	#10 samples for insane party
	for i in range(10):
		tempxtr=list()
		tempxtr=[83+random.triangular(-3, 5), 26+random.triangular(-7,7), 95+random.triangular(-50,50), 35+random.triangular(-2,2)]
		toxtr.append(tempxtr)
		toytr.append(3)
	xtr = np.array(toxtr)
	ytr = np.array(toytr)
	knn = mlpy.Knn(k=1)
	knn.compute(xtr, ytr)
	xts = np.array(observList)
	return knn.predict(xts)


  

# Wait for 'ready'
while 1:
  postMessage = ser.readline()
  if postMessage.find('ready'):
    break


print 'Ready'
sleep(0.5)

sandwich.write('n')

metronome = 0
while 1:
  ser.write('u')
  postMessage = ser.readline()
  print postMessage

  #postMessage = ser.readline()
  print '[ '+ postMessage +' ]'
  ser.write('i')
  print ser.readline()


  # Take five measurements
  tempArray = []
  for i in range(0, 5):
    ser.write('u')
    postMessage = ser.readline()
    tempArray.append( float(postMessage.rstrip()) )
    
    print 'T: '+ postMessage
    time.sleep(0.1)
  print 'Finished temp readings.'
  averageTemp = sum(tempArray) / len(tempArray)

  ser.write('i')  # Guest count

  #print ser.readline()

  numGuests = ser.readline().rstrip()
  strTime = time.asctime(time.localtime(time.time()))

  postMessage = 'People: '+ numGuests +', and my current temperature is: '+ str(averageTemp) + '. Bro.'
  print postMessage

  postStatus(postMessage)
  
  #Every 30 seconds
  if (metronome % 6 == 0):
    postPicture()

  likeage = countLikes()
  soundLevel = pollSound()
  updateLikeMeter(likeage)
  soundLevel = updateSoundMeter(soundLevel)
  readEnvironment()
  partyTier = classifyParty([averageTemp, hAVG, cAVG, soundLevel])
  checkSandwich()
  
  print 'Party tier: '+ str(partyTier)
  
  metronome += 1
  sleep(2)




"""
fields = [('access_token', access_token), ('message', time.asctime(time.localtime(time.time()))),
    ('source', (pycurl.FORM_FILE, imageLocation))]

c = pycurl.Curl()
c.setopt(c.URL, 'https://graph.facebook.com/3780/photos')
c.setopt(c.HTTPPOST, fields)
c.perform()
c.close()
"""


"""
params = { 'access_token': access_token, 'source': imageLocation, 'message': time.asctime(time.localtime(time.time())) }
c = pycurl.Curl()
c.setopt(c.POST, 1)
c.setopt(c.URL, 'https://graph.facebook.com/me/photos') #?'+ urllib.urlencode(params))
#c.setopt(c.HTTPPOST, params)
c.setopt(c.VERBOSE, 1)
c.perform()
c.close()
"""


#App ID
# 201793946507565
#API Key
# bc13c86480dc16eac6b87eb63b5346aa
#App Secret
# ba53a4704f3dd2b046cd090087891424
#Code
# d202ecd7aef8dbce66e1e6e0-100002268818038%7CXY9AjPPlixPigHgWyvIUY71rRTk

#https://graph.facebook.com/oauth/access_token?type=client_cred&client_id=201793946507565&client_secret=ba53a4704f3dd2b046cd090087891424

# https://www.facebook.com/dialog/oauth?client_id=201793946507565&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token
# https://www.facebook.com/dialog/oauth?client_id=201793946507565&redirect_uri=http://www.facebook.com/&scope=manage_pages&response_type=token

# https://www.facebook.com/dialog/oauth?client_id=201793946507565&redirect_uri=http://www.facebook.com/&scope=publish_stream,read_stream,create_event,rsvp_event,sms,offline_access,publish_checkins


#print graph.put_object("me", "feed", message=postMessage)



"""
curl -F 'access_token=201793946507565%7C2.Xybx_4SNhmSbdKjYs3tnQg__.3600.1301115600-100002268818038%7CFclNdwBHAL2qXugnR9sfs7GcAPg' \
     -F 'source=@capture.jpg' \
     -F 'message=Howdy' \
     https://graph.facebook.com/me/photos
"""





#ser = serial.Serial('/dev/usbmon0', 9600)
#while 1:
#     ser.readline()




#ser = serial.Serial('/dev/tty.usbserial', 9600)
#ser.write('5')

