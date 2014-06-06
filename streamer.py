from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sqlite3, json, os
import config

buffered_list = []
cursor = None
con = None

class stream_listener(StreamListener):  
    def __init__(self):
        self.connect_db()
        self.naughty_words = self.load_naughty_words()
        super(stream_listener, self)

    def load_naughty_words(self):
        try:
            if os.path.isfile(config.stream['naughty_file']):
                fo = open(config.stream['naughty_file'], 'r')
                words = fo.readlines()  
                word_list = []
                for word in words:
                    word_list.append(word.strip())
                return word_list
            return []
        except:
            print "Error reading naughty file"
            return []

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            self.write_tweet(tweet)
        except Exception as e:     
            print "Error processing Tweet:", e

    def on_error(self, status):
        print status

    def connect_db(self):
        self.con = sqlite3.connect(config.stream['db_file'])
        self.cursor = self.con.cursor()

    def write_tweet(self, tweet):
        t_id = tweet['id']
        t_text = tweet['text'] 
        for word in self.naughty_words:
            if str(word.lower) in str(t_text.encode('utf-8')).lower():
                return
        t_time = tweet['created_at']
        u_id = tweet['user']['id']
        u_name = tweet['user']['name']
        u_username = tweet['user']['screen_name']
        u_avatar = tweet['user']['profile_image_url_https']
        self.cursor.execute("INSERT INTO tweets VALUES(?,?,?,?,?,?,?)", [t_id,t_text,t_time,u_id,u_name,u_username,u_avatar])
        try:
            if tweet['entities'] is not None:   
                if tweet['entities']['media'] is not None and len(tweet['entities']['media']) > 0:
                    self.cursor.execute("INSERT INTO media VALUES(?,?,?,?,?,?)", [t_id,t_text,u_id,u_name,u_username,tweet['entities']['media'][0]['media_url']])
        except:
            print "Could not parse image."
        self.con.commit()        

    def write_tweets(self, tweets):
        for tweet in tweets:
            write_tweet(tweet)

def init_db():
    con = sqlite3.connect(config.stream['db_file'])
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tweets(
                tweet_id NUMBER,
                tweet_text TEXT,
                tweet_time TEXT,
                user_id NUMBER,
                user_name TEXT,
                user_username TEXT,
                user_avatar TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS media(
                tweet_id NUMBER,
                tweet_text TEXT,
                user_id NUMBER,
                user_name TEXT,
                user_username TEXT,
                url TEXT)""")
    con.commit()
    con.close()

def load_twitter_credentials():
    try:
        json_file = open("twitter_credentials.json", "r")
        json_data = json_file.read()
        credentials = json.loads(json_data)
        return credentials
    except Exception as e:
        print "Could not load Twitter credentials ffrom twitter_credentials.json."
        exit()

def start_streamer():
    init_db()
    t_creds = load_twitter_credentials()
    auth = OAuthHandler(t_creds['consumer_key'], t_creds['consumer_secret'])
    auth.set_access_token(t_creds['access_token'], t_creds['access_secret'])
    twitterStream = Stream(auth, stream_listener())
    twitterStream.filter(track=config.stream['terms'])
