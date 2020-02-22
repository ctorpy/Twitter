# coding: utf-8

#extract words from tweet

import os
import json
import re
from nltk.corpus import stopwords,words
import nltk
from nltk.stem import PorterStemmer
from google.cloud import storage
from datetime import datetime


nltk.download('stopwords')
nltk.download('words')
hashtags=['kubernetes','cloudnative','developers','technology','spark','blockchain']
pstem = PorterStemmer()

def process_text(data):
	corpus=[]
	for this_line in data.splitlines():
		dict_data=json.loads(this_line)
		text=dict_data['text'] 
		hash_tag='None'
		#get the hash tag out
		for this_tag in hashtags:
			if this_tag in text:
				hash_tag=this_tag
				break
		#get the words in tweet    
		text = re.sub("[^a-zA-Z]", ' ',text)
		text = text.lower()
		text = text.split()
		text = [pstem.stem(word) for word in text if not word in set(stopwords.words('english'))]
		text=list(filter(lambda x: x in words.words(),text))
		if hash_tag != 'None':
			corpus.append({'tag':hash_tag,'words':text})
	return corpus   

def bucket_listener(data, context):
	print('Event ID: {}'.format(context.event_id))
	print('Event type: {}'.format(context.event_type))
	print('Bucket: {}'.format(data['bucket']))
	print('File: {}'.format(data['name']))
	print('Metageneration: {}'.format(data['metageneration']))
	print('Created: {}'.format(data['timeCreated']))
	print('Updated: {}'.format(data['updated']))

	if data['name'].startswith('raw/raw_tweet'):
		#read data from GCS
		text=read_from_gcs(data['name'])
		#extract words from tweet
		corpus=process_text(text)
		#write to GCS
		write_to_gcs(corpus)


def read_from_gcs(blob_name):
	storage_client = storage.Client()
	bucket = storage_client.get_bucket('twitter_dl')
	blob = bucket.blob(blob_name)
	text=blob.download_as_string()
	return text


def write_to_gcs(data):
	#persist cleaned dtaa to GCS
	now = datetime.now()
	blob_name = 'clean/words-{}'.format(now.strftime("%Y-%m-%d %H:%M:%S"))
	storage_client = storage.Client()
	bucket = storage_client.get_bucket('twitter_dl')
	blob = bucket.blob(blob_name)
	blob.upload_from_string(str(data))
	print('Written cleaned data to GCS - {}'.format(blob_name))
	
	
