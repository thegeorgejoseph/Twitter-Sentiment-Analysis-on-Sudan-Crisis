import sys
import csv
import tweepy
import re 
import nltk
import string
from nltk.classify import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from nltk.corpus import stopwords
import nltk.classify.util


stopWords = []
 

def replaceTwoOrMore(s):
    
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end
 

def getStopWordList(stopWordListFileName):

    stopWords = []
    
    stopWords.append('URL')
 
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

st = open('StopWords.txt', 'r')
stopWords = getStopWordList('StopWords.txt')
 
#starting the function 
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        
        w = replaceTwoOrMore(w)
        
        w = w.strip('\'"?,.')
        
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end
 
#starting the function 
def featureExtraction():
    #Here I am reading the tweets one by one and process it
    inpTweets = csv.reader(open('TweetsDataSet_MaxEnt', 'rb'), delimiter=',', quotechar='|')
    tweets = []
  
    for rowTweet in inpTweets:
        sentiment = rowTweet[0]
        tweet = rowTweet[1]
        featureVector = getFeatureVector(tweet)
        tweets.append((featureVector, sentiment))
    
    return tweets 

tweets = featureExtraction()
#print tweets

#Classifier 
def get_words_in_tweets(tweets):
    all_words = []
    for (text, sentiment) in tweets:
        all_words.extend(text)
    return all_words

def get_word_features(wordlist):
    

    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    
   
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets)) 

def extract_features(tweet):
    settweet = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in settweet)
    return features




training_set = nltk.classify.apply_features(extract_features, tweets)
test_set = nltk.classify.apply_features(extract_features, tweets[:250])

#****** Naive Bayes Classifier******************************************

classifier = nltk.NaiveBayesClassifier.train(training_set)

# Accuracy
accuracy = nltk.classify.accuracy(classifier, training_set) 

#Printing the accuracy
print accuracy 

total = accuracy * 100 
print 'Naive Bayes Accuracy: %4.2f' % total 

# Accuracy Test Set
accuracyTestSet = nltk.classify.accuracy(classifier, test_set) 

#Printing the accuracy for the test set 
print accuracyTestSet 

totalTest = accuracyTestSet * 100 
print '\nNaive Bayes Accuracy with the Test Set: %4.2f' % totalTest 

print '\nInformative features'
print classifier.show_most_informative_features(n=15)
#**************************

var = ''
while(var!='exit'):
    input = raw_input('\nPlease write a sentence to be tested sentiment. If you type - exit- the program will exit \n')
    print '\n'
    if input == 'exit':
        print 'Exiting the program'
        var = 'exit'
        #break
    else:
        input = input.lower()
        input = input.split()
       
        print '\nNaive Bayes Classifier'
        print 'I think that the sentiment was ' + classifier.classify(extract_features(input)) + ' in that sentence.\n'

   
    
