import urllib.request as urllib2 

neg_train_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/train/Negative.txt'
neg_file = urllib2.urlopen(neg_train_data_url)
neg_tweets = []
for line in neg_file:
    neg_tweets.append(line.decode('utf-8'))


neu_train_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/train/Neutral.txt'
neu_file = urllib2.urlopen(neu_train_data_url)
neu_tweets = []
for line in neu_file:
    neu_tweets.append(line.decode('utf-8'))


pos_train_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/train/Positive.txt'
pos_file = urllib2.urlopen(pos_train_data_url)
pos_tweets = []
for line in pos_file:
    pos_tweets.append(line.decode('utf-8'))

print(neg_tweets[0])
print(neu_tweets[0])
print(pos_tweets[0])
