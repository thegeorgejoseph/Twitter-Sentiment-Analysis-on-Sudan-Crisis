import sys
import tweepy
import re 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler



class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, maxnum, api=None):
        self.n = maxnum
        self.api = api

    def on_status(self, status):
        try:
            tweets = []
            name = status.author.screen_name
            textTwitter = status.text
            
            #Convert into lowercase
            Tweet = textTwitter.lower()
            
            #Convert www.* or https?://* to URL
            Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',Tweet)
            
            #Convert @username to User
            Tweet = re.sub('@[^\s]+','TWITTER_USER',Tweet)
            
            #Remove additional white spaces
            tweet = re.sub('[\s]+', ' ', Tweet)
            
            #Replace #word with word Handling hashtags
            Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)
            
            #trim
            Tweet = Tweet.strip('\'"')
            
            #Deleting happy and sad face emoticon from the tweet 
            a = ':)'
            b = ':('
            Tweet = Tweet.replace(a,'')
            Tweet = Tweet.replace(b,'')
            
            #Deleting the Twitter @username tag and reTweets
            tag = 'TWITTER_USER' 
            rt = 'rt'
            Tweet = Tweet.replace(tag,'')
            Tweet = Tweet.replace(rt,'')
            
            final_tweet = '|positive|, |%s| ' % (Tweet)

            f = open('YourFileHereName', 'r+')
            old = f.read()
            f.write(final_tweet+'\n')
            f.close()
        
            self.n = self.n+1
            if self.n < 3000: 
                return True
            else:
                print 'maxnum = '+str(self.n)
                return False
        
        except Exception as e:
            print (e)

    def on_error(self, status_code):
        
        return True 

    def on_timeout(self):
        
        return True 
        


class CustomStreamListenerNEG(tweepy.StreamListener):
    def __init__(self, maxnum, api=None):
        self.n = maxnum
        self.api = api

    def on_status(self, status):
        try:
            tweets = []
            name = status.author.screen_name
            textTwitter = status.text
            
            
            Tweet = textTwitter.lower()
            
            
            Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',Tweet)
            
            
            Tweet = re.sub('@[^\s]+','TWITTER_USER',Tweet)
            
            
            tweet = re.sub('[\s]+', ' ', Tweet)
            
            
            Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)
            
            
            Tweet = Tweet.strip('\'"')
            
             
            a = ':)'
            b = ':('
            Tweet = Tweet.replace(a,'')
            Tweet = Tweet.replace(b,'')
                        
            
            tag = 'TWITTER_USER' 
            rt = 'rt'
            Tweet = Tweet.replace(tag,'')
            Tweet = Tweet.replace(rt,'')
            
            final_tweet = '|negative|, |%s| ' % (Tweet)
            
            f = open('YourFileHereName', 'r+')
            old = f.read()
            f.write(final_tweet+'\n')
            f.close()
        
            self.n = self.n+1
            if self.n < 3000: 
                return True
            else:
                print 'maxnum = '+str(self.n)
                return False
        
        except Exception as e:
            print (e)

    def on_error(self, status_code):
        
        return True 

    def on_timeout(self):
        
        return True 

#initialize stopWords
stopWords = []
 
#starting the function
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end
 
#starting the function
def getStopWordList(stopWordListFileName):
#read the stopwords file and build a list
    stopWords = []
    stopWords.append('TWITTER_USER')
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
 
#starting the function
def getFeatureVector(tweet):
    
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end


def main():
    consumer_key="####"
    consumer_secret="####"
    access_token="####"
    access_token_secret="####"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 

    print "Establishing stream...\n"
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener(maxnum=0))
    
    setTerms = [':)']
    
    sapi.filter(None, setTerms, languages=["en"])
    

def mainNEG():
    consumer_key="####"
    consumer_secret="####"
    access_token="####"
    access_token_secret="####"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 
    
    
    NegTweets = tweepy.streaming.Stream(auth, CustomStreamListenerNEG(maxnum=0))
    setTermsNEG = [':(']
    
    NegTweets.filter(None, setTermsNEG, languages=["en"])
     
    
def Positive():
    fp = open('YourFileHereName', 'r')
    line = fp.readline()
    
    st = open('StopWords.txt', 'r')
    stopWords = getStopWordList('StopWords.txt')
    
    while line:
        featureVector = getFeatureVector(line)
        
        line = fp.readline()         
    
if __name__ == '__main__':
    try:
        main()
        mainNEG()
        Positive()
        
    except KeyboardInterrupt:
        print "Disconnecting from Twitter... ",
        print "Done"        
        
        
        
        
