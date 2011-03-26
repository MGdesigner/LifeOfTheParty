import serial
import facebook
import re
import urllib
import time
import os
from time import sleep


access_token = '201793946507565%7C2.GvNfZZBc6rRObaf2oGWadg__.3600.1301122800-100002268818038%7CZieF2kcaynYqHsPhWbNxo1OMigg' # LifeOf TheParty
imageLocation = 'capture.jpg'
quiet = True

ser = serial.Serial('/dev/ttyACM0', 9600)
graph = facebook.GraphAPI(access_token)




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



while 1:
  postMessage = ser.readline()
  if postMessage.find('ready'):
    break

#print ser.readline()

print 'Ready'
sleep(1)

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
  postPicture()
  
  
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
# 2.QNdUhbDIwYxUy5G_C6lCiQ__.3600.1301104800-698432281|zy_pFQGxrfnde0B08jIWTvZiMLI



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

