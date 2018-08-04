
import time
import requests
from pathlib import Path

headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAADmO4QAAAAAA1l35b3JfTyYe8rDAX0q7nhR%2BBis%3D90KK4CMhxUBYfLFslUyJmusiEVnhBRLVmIG4Nnb2b6R2SlVxmU',
}

params = (
    ('screen_name', 'realdonaldtrump'),
    ('include_rts', '1'),
    ('count', '1'),
    ('tweet_mode', 'extended'),
)

response = requests.get('https://api.twitter.com:443/1.1/statuses/user_timeline.json', headers=headers, params=params)

data = response.json()

max_id = int(data[0]['id'])


tweet_num=1000 #number of tweets to extract

import requests

#max_id allows to overcome the limit of extracting 200 tweets per time
  
for i in range(tweet_num):
    headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAADmO4QAAAAAA1l35b3JfTyYe8rDAX0q7nhR%2BBis%3D90KK4CMhxUBYfLFslUyJmusiEVnhBRLVmIG4Nnb2b6R2SlVxmU',
    }
    
    params = (
        ('screen_name', 'realdonaldtrump'),
        ('include_rts', '1'),
        ('count', '1'),
        ('tweet_mode', 'extended'),
        ('max_id', max_id),)

    response = requests.get('https://api.twitter.com:443/1.1/statuses/user_timeline.json', headers=headers, params=params)
    data = response.json()
    Path("D:/viburnum/trump find words/data/js_" + str(i)).touch() #creates a new file to put json inside
    
    #java does not recognize ' so a new json will be
    file = open("D:/viburnum/trump find words/data/js_" + str(i), "r+", encoding="utf-8")
    file.write("{\"full_text\": \""+ str(data[0]['full_text'])+ "\", "+
               "\"created_at\": \""+ str(data[0]['created_at'])+ "\","+
               "\"retweet_count\": "+ str(data[0]['retweet_count'])+ "}"+ "\n")
    print("File " + "js_" + str(i) + " was created")
    file.close()
    max_id = int(data[0]['id'])-1 #id less than the one that was processed
    if i % 50 == 0:								#making a pause for 3 seconds every 50th day
        time.sleep(3)


    