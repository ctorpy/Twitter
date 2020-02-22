#! /usr/bin/python
'''
Starts a listener for tweets containing a list of hash tags.
Publish tweets containing hash tag 
'''

# coding: utf-8
import datetime
import json
import time
import os


from google.cloud import pubsub_v1,logging
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import logging

#store all the certificcations in another privtae file
from twitter_cert import *


# Config pub/sub
publisher = pubsub_v1.PublisherClient()

# config pub/sub
project_id = "twitter-268909"
topic_name="cloud_tweets"
topic_path = publisher.topic_path(project_id, topic_name)

# Method to push messages to pubsub
def write_to_pubsub(tweet_data):
    try:
        if tweet_data["lang"] == "en":
            publisher.publish(topic_path, data=json.dumps({
                "text": tweet_data["text"],
                "user": tweet_data["user"],
                "posted_at": tweet_data["created_at"]
            }).encode("utf-8"), tweet_id=str(tweet_data["id"]).encode("utf-8"))
            logging.info('tweet published {}'.format(tweet_data['text']))    
            print('tweet published {}'.format(tweet_data['text']))    
    except Exception as e:
        raise

class TwritterListener(StreamListener):
    def on_data(self,data):
        try:
            j_data=json.loads(data)
            #print(j_data.keys())
            write_to_pubsub(j_data)
        except BaseException as ex:
            logging.error('Error publishing tweet - {}'.format(str(ex)))
        return True
    def on_error(self,status):
        logging.error('Error publishing tweet - {}'.format(str(status)))
 
#start the listener

listener=TwritterListener()
auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream=Stream(auth,listener)
logging.info('Starting listener')
stream.filter(track=['#kubernetes','#cloudnative','#developers','#technology','#spark','#blockchain'])