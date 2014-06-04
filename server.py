from flask import Flask, render_template, jsonify 
import sqlite3, json
import config

app = Flask(__name__)
app.secret_key = config.web_server['secret_key']

class DatabaseManager():
    def __init__(self):
        self.connect()
        
    def connect(self):
        self.con = sqlite3.connect(config.stream['db_file'])
        self.con.row_factory = sqlite3.Row
        self.cursor = self.con.cursor()

    def get_recent_media(self, last_media_id):
        self.connect()
        res = self.cursor.execute("SELECT * FROM media WHERE tweet_id > ? ORDER BY tweet_id DESC LIMIT 20", [last_media_id]).fetchall()
        media = []
        for row in res:
            item = {}       
            item['url'] = row['url']
            item['tweet_id'] = row['tweet_id']
            item['tweet_text'] = row['tweet_text']
            item['user_username'] = row['user_username']
            media.append(item)
        return media 

    def get_recent_tweets(self, last_id):
        self.connect()
        res = self.cursor.execute("SELECT * FROM tweets WHERE tweet_id > ? ORDER BY tweet_id DESC LIMIT 20", [last_id]).fetchall()
        tweets = []
        for row in res:
            tweet = {}
            tweet['tweet_id'] = row['tweet_id']
            tweet['tweet_text'] = row['tweet_text'] 
            tweet['tweet_time'] = row['tweet_time']
            tweet['user_id'] = row['user_id']
            tweet['user_name'] = row['user_name']
            tweet['user_username'] = row['user_username']
            tweet['user_avatar'] = row['user_avatar']   
            tweet['highlighted'] = False
            try: 
                for term in config.stream['highlight_terms']:
                    if term.lower() in tweet['tweet_text'].lower():
                        tweet['highlighted'] = True
            except Exception as e:
                continue
            tweets.append(tweet)
        return tweets    
    

dm = DatabaseManager()

@app.route('/')
def home():
    return render_template('index.html', main_hashtag = config.stream['main_hashtag'])

@app.route('/get_more/<last_id>/<last_media_id>')
def get_more(last_id, last_media_id):
    try:
        last_id = long(last_id)
        last_media_id = long(last_media_id)
        recent_tweets = dm.get_recent_tweets(last_id)
        recent_media = dm.get_recent_media(last_media_id)
        
        r = {}
        r['tweets'] = recent_tweets
        r['media'] = recent_media
        return json.dumps(r)
    except Exception as e:
        print e
        r = {}
        r['tweets'] = []
        r['media'] = []
        return json.dumps(r)
        
def start_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    start_server()
