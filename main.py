import urllib.request as urllib2 
from collections import Counter

# Training Data 
neg_train_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/train/Negative.txt'
neg_file = urllib2.urlopen(neg_train_data_url)
neg_train_tweets = []
for line in neg_file:
    neg_train_tweets.append(line.decode('utf-8'))


neu_train_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/train/Neutral.txt'
neu_file = urllib2.urlopen(neu_train_data_url)
neu_train_tweets = []
for line in neu_file:
    neu_train_tweets.append(line.decode('utf-8'))


pos_train_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/train/Positive.txt'
pos_file = urllib2.urlopen(pos_train_data_url)
pos_train_tweets = []
for line in pos_file:
    pos_train_tweets.append(line.decode('utf-8'))

# Testing Data
neg_test_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/test/Negative.txt'
neg_file = urllib2.urlopen(neg_test_data_url)
neg_test_tweets = []
for line in neg_file:
    neg_test_tweets.append(line.decode('utf-8'))


neu_test_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/test/Neutral.txt'
neu_file = urllib2.urlopen(neu_test_data_url)
neu_test_tweets = []
for line in neu_file:
    neu_test_tweets.append(line.decode('utf-8'))


pos_test_data_url = 'https://raw.githubusercontent.com/jeniyat/CSE-5521-SP21/master/HW/HW2/Data/test/Positive.txt'
pos_file = urllib2.urlopen(pos_test_data_url)
pos_test_tweets = []
for line in pos_file:
    pos_test_tweets.append(line.decode('utf-8'))



num_pos_examples = len(pos_train_tweets)
num_neg_examples = len(neg_train_tweets)
num_neu_examples = len(neu_train_tweets)
total_num_examples = num_neg_examples + num_neu_examples + num_pos_examples

pos_class_prob = num_pos_examples/total_num_examples # 30.6%
neg_class_prob = num_neg_examples/total_num_examples # 28.8%
neu_class_prob = num_neu_examples/total_num_examples # 40.5%


vocab_all = Counter()
vocab_positive = Counter()
vocab_negative = Counter()
vocab_neutral = Counter()

total_num_of_neg_words= 0
total_num_of_pos_words= 0
total_num_of_neu_words= 0

for sent in neg_train_tweets:
    word_list = sent.split()
    for word in word_list:
        # word = word.lower()
        vocab_all[word]+=1
        total_num_of_neg_words+=1
        vocab_negative[word]+=1

for sent in pos_train_tweets:
    word_list = sent.split()
    for word in word_list:
        # word = word.lower()
        vocab_all[word]+=1
        total_num_of_pos_words+=1
        vocab_positive[word]+=1

for sent in neu_train_tweets:
    word_list = sent.split()
    for word in word_list:
        # word = word.lower()
        vocab_all[word]+=1
        total_num_of_neu_words+=1
        vocab_neutral[word]+=1

print("vocab_all: ",vocab_all)
vocab_size = len(vocab_all)
print("vocab_size: ",vocab_size)

# (Try α = 1, 0.5, 2, 10).
# alpha = 1 ---> 0.8735483870967742
# alpha = 0.5 ---> 0.8722580645161291
# alpha = 2 ---> 0.8761290322580645
# alpha = 10 ---> 0.8696774193548387

alpha = 10

def find_pos_prob_sent(list_words):
  pos_prob_sent = pos_class_prob

  for word in list_words:
    if word in vocab_positive:
      numerator = vocab_positive[word]+alpha
    else:
      numerator = alpha

    denominator = total_num_of_pos_words + alpha*vocab_size
    word_prob = numerator / denominator

    pos_prob_sent = pos_prob_sent*word_prob 

  return pos_prob_sent

def find_neg_prob_sent(list_words):
  neg_prob_sent = neg_class_prob

  for word in list_words:
    if word in vocab_negative:
      numerator = vocab_negative[word]+alpha
    else:
      numerator = alpha

    denominator = total_num_of_neg_words + alpha*vocab_size
    word_prob = numerator / denominator

    neg_prob_sent = neg_prob_sent*word_prob 

  return neg_prob_sent

def find_neu_prob_sent(list_words):
  neu_prob_sent = neu_class_prob

  for word in list_words:
    if word in vocab_neutral:
      numerator = vocab_neutral[word] + alpha
    else:
      numerator = alpha

    denominator =  total_num_of_neu_words + alpha*vocab_size
    word_prob = numerator / denominator

    neu_prob_sent = neu_prob_sent*word_prob

  return neu_prob_sent



prediction_list = []

for sent in pos_test_tweets:
    word_list = sent.split()
    prob = {}
    pos_prob = find_pos_prob_sent(word_list)
    neg_prob = find_neg_prob_sent(word_list)
    neu_prob = find_neu_prob_sent(word_list)

    actual = "+ve"

    prob[pos_prob] = "+ve"
    prob[neg_prob] = "-ve"
    prob[neu_prob] = "+/-ve"
    print(prob)

    prediction = prob[max(prob, key=float)]


    # if neg_prob > pos_prob:
    #     prediction = "-ve"
    # elif neu_prob > pos_prob:
    #     prediction = "+/-ve"
    # else:
    #     prediction = "+ve"

    pred = (sent, actual, prediction)
    prediction_list.append(pred)

    print("sent: ", sent)
    print("pos_prob: ", pos_prob)
    print("neg_prob: ", neg_prob)
    print("neu_prob: ", neu_prob)
    print("prediction: ", prediction)
    print("actual: ", actual)
    print("---------")

for sent in neg_test_tweets:
    word_list = sent.split()
    prob = {}
    pos_prob = find_pos_prob_sent(word_list)
    neg_prob = find_neg_prob_sent(word_list)
    neu_prob = find_neu_prob_sent(word_list)

    actual = "-ve"

    prob[pos_prob] = "+ve"
    prob[neg_prob] = "-ve"
    prob[neu_prob] = "+/-ve"
    print(prob)

    prediction = prob[max(prob, key=float)]

    # if pos_prob > neg_prob:
    #     prediction = "+ve"
    # elif neu_prob > neg_prob:
    #     prediction = "+/-ve"
    # else:
    #     prediction = "-ve"

    pred = (sent, actual, prediction)
    prediction_list.append(pred)

    print("sent: ", sent)
    print("pos_prob: ", pos_prob)
    print("neg_prob: ", neg_prob)
    print("neu_prob: ", neu_prob)
    print("prediction: ", prediction)
    print("actual: ", actual)
    print("---------")


for sent in neu_test_tweets:
    word_list = sent.split()
    prob = {}
    pos_prob = find_pos_prob_sent(word_list)
    neg_prob = find_neg_prob_sent(word_list)
    neu_prob = find_neu_prob_sent(word_list)

    actual = "+/-ve"
    
    prob[pos_prob] = "+ve"
    prob[neg_prob] = "-ve"
    prob[neu_prob] = "+/-ve"
    print(prob)

    prediction = prob[max(prob, key=float)]
    # if pos_prob > neg_prob:
    #     prediction = "+ve"
    # elif neg_prob > neu_prob:
    #     prediction = "-ve"
    # else:
    #     prediction = "+/-ve"

    pred = (sent, actual, prediction)
    prediction_list.append(pred)

    print("sent: ", sent)
    print("pos_prob: ", pos_prob)
    print("neg_prob: ", neg_prob)
    print("neu_prob: ", neu_prob)
    print("prediction: ", prediction)
    print("actual: ", actual)
    print("---------")

correct = 0
total_test_case = 0
for pred in prediction_list:
  (sent, actual, prediction) = pred
  if actual == prediction:
    correct+=1
  total_test_case +=1


accuracy = correct/ total_test_case

print("accuracy: ",accuracy)
