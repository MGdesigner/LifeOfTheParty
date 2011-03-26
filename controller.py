import serial
import facebook
import re
import urllib
import time
import os
from time import sleep


access_token = '201793946507565%7Cd202ecd7aef8dbce66e1e6e0-100002268818038%7CiHYYQSxjEu1_O2cltKLULG-7jL8' # LifeOf TheParty
event_id = '130842913653732'  # Hackathon
imageLocation = 'capture.jpg'
quiet = True

ser = serial.Serial('/dev/ttyACM0', 9600)
#co2 = serial.Serial('/dev/ttyUSB0',115200)
graph = facebook.GraphAPI(access_token)

tAVG=0
hAVG=0
cAVG=0

def readData():
  global tAVG
  global hAVG
  global cAVG
  for count in range(10):
	  ser.write('t')
	  ser.read(3)
	  b=ser.read()
	  a=ser.read()
	  temp=(((ord(a)<<8))*0.018)+32
	  temp=temp
	  ser.read()
	  ser.write('f')
	  ser.read(5)
	  time.sleep(.2)
	  ser.write('r')
	  ser.read(4)
	  a=ser.read()
	  relHumid=(ord(a)<<8)/100
	  ser.read()
	  ser.write('d')
	  ser.read(5)
	  time.sleep(.2)
	  ser.write('c')
	  cohtwo=0
	  ser.read(4)
	  #for i in range(2):
	  tmp=ser.read()
	  cohtwo= ord(tmp)<<8	
	  ser.read()
	  ser.write('e')
	  ser.read(5)
	  time.sleep(.2)
	  tAVG+=temp
	  hAVG+=relHumid
	  cAVG+=cohtwo
  tAVG=tAVG/10
  hAVG=hAVG/10
  cAVG=cAVG/10



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
  

# Wait for 'ready'
while 1:
  postMessage = ser.readline()
  if postMessage.find('ready'):
    break


print 'Ready'
sleep(0.5)

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

  ser.write('i')  # Guest count

  #print ser.readline()

  numGuests = ser.readline().rstrip()
  strTime = time.asctime(time.localtime(time.time()))

  postMessage = 'People: '+ numGuests +', and my current temperature is: '+ str(sum(tempArray) / len(tempArray)) + '. Bro.'
  print postMessage

  postStatus(postMessage)
  
  #Every 30 seconds
  print "Met: "+ str(metronome)
  if (metronome % 8 == 0):
    print "Met hit"
    postPicture()
  likeage = countLikes()
  updateLikeMeter(likeage)
  #readData()
  
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

