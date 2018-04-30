from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import re
from textblob import TextBlob
import json
from elasticsearch import Elasticsearch
from datetime import datetime

def get_tweet_sentiment(tweet):
        analysis = TextBlob(tweet[0])
        einstance = Elasticsearch(['http://localhost:9200'])
	    print(tweet)
        if analysis.sentiment.polarity > 0:
             sentiment = 'positive'
        elif analysis.sentiment.polarity == 0:
            sentiment = 'neutral'
        else:
            sentiment = 'negative'
        latlong = tweet[1].split("@@@@")
	    doc = {
	        'text': tweet[0],
	        'sentiment' : sentiment,
	        'geo_point' : str(latlong[0]+","+latlong[1]),
	        'timestamp' : datetime.now(),
	         }
	einstance.index(index='homework-3',doc_type = 'tweet', body = doc)

TCP_IP = 'localhost'
TCP_PORT = 9001

# Pyspark
# create spark configuration
conf = SparkConf()
conf.setAppName('TwitterApp')
conf.setMaster('local[2]')
# create spark context with the above configuration
sc = SparkContext(conf=conf)

# create the Streaming Context from spark context with interval size 2 seconds
ssc = StreamingContext(sc, 4)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 900
dataStream = ssc.socketTextStream(TCP_IP, TCP_PORT)

######### your processing here ###################
dataStream.pprint()
tweetdata = dataStream.flatMap(lambda x: x.split("####"))
filtertweets = tweetdata.filter(lambda x: len(x.split('++++')) == 2)
tweettext = filtertweets.map(lambda x : x.split("++++"))
tweetsentiment = tweettext.map(lambda x : get_tweet_sentiment(x))
tweettext.pprint()
tweetsentiment.pprint()
#################################################

ssc.start()
ssc.awaitTermination()
