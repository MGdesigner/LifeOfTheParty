import facebook
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write('0')
access_token = '201793946507565%7Cd202ecd7aef8dbce66e1e6e0-100002268818038%7CiHYYQSxjEu1_O2cltKLULG-7jL8' # LifeOf TheParty
event_id = '130842913653732'  # Hackathon
graph = facebook.GraphAPI(access_token)
while 1:
  posts = graph.get_connections(event_id, 'feed')['data']
  last_status = posts[0]['message']
  if last_status.find('Make me a sandwich.') != -1:
    message = "What? Make it yourself."
    graph.put_object(last_status['id'], "comments", message)
  elif last_status.find('Sudo make me a sandwich.') != -1:
    message = "Okay."
    graph.put_object(last_status['id'], "comments", message)
    ser.write('180')
  sleep(5)