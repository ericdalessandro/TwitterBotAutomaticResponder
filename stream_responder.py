import tweepy, time, csv

ACCESS_KEY = ''
ACCESS_SECRET = ''
CONSUMER_KEY =  ''
CONSUMER_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'
KEYWORDS_FILE_NAME = 'schedule_keywords.txt'
KEY_PHRASES = []

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(file_name, last_seen_id):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('Initializing Tweet retrieval and auto-response...')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' -  ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(FILE_NAME, last_seen_id)
        if 'stream link' in mention.full_text.lower():
            print('Found link request...')
            print('Responding...')
            api.update_status('@' + mention.user.screen_name +
                              ' Here is the link :) twitch.tv/hedgi - HedgiBot',
                              mention.id)
            print('Response sent.')

        else:
            for phrase in KEY_PHRASES:
                if phrase in mention.full_text.lower():
                    print('Found schedule reference...')
                    print('Responding...')
                    api.update_status('@' + mention.user.screen_name +
                                      ' I stream Sundays at 6pm, Tuesdays at 4pm, Wednesdays at 2pm, '
                                      'and Thursdays at 4pm (EST) and whenever else I have the chance! - HedgiBot',
                                      mention.id)
                    print('Response sent.')

with open(KEYWORDS_FILE_NAME) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        KEY_PHRASES.append(str(row)[2:-2])

while True:
    reply_to_tweets()
    time.sleep(60)
