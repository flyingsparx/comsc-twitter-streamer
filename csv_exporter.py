# Export Tweets collected in the tweets.db SQLite database to CSV
# 
# Creates two CSV files: one for the collected Tweets and another for collected images

import sqlite3, time

def get_tweets(c):
    result = c.execute("SELECT * FROM tweets").fetchall()
    return result

def get_media(c):
    result = c.execute("SELECT * FROM media").fetchall()
    return result

def write_tweet_csv(tweets, timestamp):
    tweet_file = open("tweets_"+str(timestamp)+".csv", "w")
    tweet_file.write("tweet_id,tweet_text,tweet_url,tweet_time,user_id,user_name,user_username,user_avatar_url\n")
    for t in tweets:
        try:
            text = t['tweet_text'].encode('utf8').strip()
            username = t['user_username'].encode('utf8').strip()
            name = t['user_name'].encode('utf8').strip()
            avatar = t['user_avatar'].encode('utf8')

            tweet_file.write(str(t['tweet_id'])+','+text.replace(',',' ')+','+'http://twitter.com/'+username+'/status/'+str(t['tweet_id'])+','+str(t['tweet_time'])+','+str(t['user_id'])+','+name+','+username+','+avatar+"\n")
        except Exception as e:
            print "Couldn't save tweet: "+t['tweet_text']+' - '+str(e)
    tweet_file.close()

def write_media_csv(media, timestamp):
    media_file = open("media_"+str(timestamp)+".csv", "w")
    media_file.write("tweet_id,tweet_text,tweet_url,user_id,user_name,user_username,media_url\n")
    for m in media:
        try:
            text = m['tweet_text'].encode('utf8').strip()
            username = m['user_username'].encode('utf8').strip()
            name = m['user_name'].encode('utf8').strip()
            url = m['url'].encode('utf8')

            media_file.write(str(m['tweet_id'])+','+text.replace(',',' ')+','+'http://twitter.com/'+username+'/status/'+str(m['tweet_id'])+','+str(m['user_id'])+','+name+','+username+','+url+"\n")
        except Exception as e:
            print "Couldn't save media: "+m['tweet_text']+' - '+str(e)
    media_file.close()

con = sqlite3.connect('tweets.db')
con.row_factory = sqlite3.Row
cursor = con.cursor()
timestamp = int(time.time())

tweets = get_tweets(cursor)
media = get_media(cursor)

con.close()

write_tweet_csv(tweets, timestamp)
write_media_csv(media, timestamp)
