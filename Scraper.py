import json 
import tweepy
import socket
import re
import urllib
import requests


ACCESS_TOKEN = '981471745038221313-j9UmatXOCZD4PscAovZUafVZm6NEkRZ'
ACCESS_SECRET = 'xTEV0hsVUwWwhKY2NBCkCLeMfjd3lCNZhyqK9h7Ewseer'
CONSUMER_KEY = 'axjZxAPBIuiqVXIlzEvBTywPD'
CONSUMER_SECRET = 'XX6ovjitLFuwAfGhqvTfdW0KyWBYPQ1Zq5tDEr07lR8UgiVabK'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


hashtag = '#Trump'

TCP_IP = 'localhost'
TCP_PORT = 9001

# create sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
	if status.user.location is not None:
		#print(status.user.location)
		URL = "https://maps.googleapis.com/maps/api/geocode/json?address="+status.user.location+"&key=AIzaSyB7xo2wIfBf0HzsVdTfkq0kCRn9EQSc1y8"  # Add Key
		res = requests.get(url = URL)
		jsondata = res.json()
		if len(jsondata['results']) == 0:		
			return
		if len(jsondata['results'][0]['address_components']) > 0:
			for i in jsondata['results'][0]['address_components']:
				if i['long_name'] == 'United States':
					print(jsondata['results'][0]['geometry']['location'])
					lat= "++++" + str(jsondata['results'][0]['geometry']['location']['lat'])
					lng= "@@@@" + str(jsondata['results'][0]['geometry']['location']['lng']) 
					sendtext = str(self.clean(status.text) + lat + lng + "####") + "\n"
					print(sendtext)
			       		conn.send(sendtext.encode('utf-8'))
    
    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)
    
    def clean(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())
myStream.filter(track=[hashtag])


