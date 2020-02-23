# Twitter analysis on the weekend of 23 Feb 2020

The solution was developed using GCP and is described in the following diagram;

![Solution Architecture](https://raw.githubusercontent.com/ctorpy/Twitter/master/solution%20architecture.png)

A VM running a python script (twitter_listener) was used to watch for a list of hash tags and publish the results to pub/sub. 
A DataFlow job was created to take the stream data from pub/sub to a plain text file in GCS every 5 minutes. Everything 
downstream from DataFlow is a batch process.

A cloud function was used o extract text analyics data from the raw tweets (data_cleaning).The Python library nltk 
was used to extract the enlish words from the tweet and remove stop words like the,is ,etc.

A word cloud for #techology is presented below;

![Solution Architecture](https://raw.githubusercontent.com/ctorpy/Twitter/master/technology_word_cloud.png)

A word cloud for #blockchain is presented below;

![Solution Architecture](https://raw.githubusercontent.com/ctorpy/Twitter/master/blockchain_word_cloud.png)

The following chart presented the top 20 most common words in the tweets broken down by hash tag;

![Solution Architecture](https://raw.githubusercontent.com/ctorpy/Twitter/master/word_count.png)

It can be seen form the chart above that airdrop is a technology that is commonly used in relation 
to tweets about #blockchain . The fact that #technology tweets were by far the most common but under 
represented compared to #blockchai suggests during the sample period there may have been a significant 
development.