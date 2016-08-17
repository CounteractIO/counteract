from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
import json
from pprint import pprint
from tweepy.streaming import StreamListener

# These values are appropriately filled in the code
consumer_key_real = "rst5oIqIuOOVnRt3UWCycP6hx"
consumer_secret_real = "ttzgiQQWzEep0A7B6J92STiJiFNOdyCTuAsfDMEuwlwBYjFudV"
access_token_real = "765521612783378436-zLHd5Fgvh8egm9ro3DD842W9zxxZ0P2"
access_token_secret_real = "G8GgxmC1CKE4sXiNcJdjY7VTm0tXImOloSXofpIHQRA0P"

consumer_key_test = "JBboCjRWkNmTtd9Ja5VSND1Sy"
consumer_secret_test = "bGTmHrWjaDXYWPWqS4LqQ4cbid5OZ7jK2SarRrOxNpK7fn4bj9"
access_token_test = "765521612783378436-xz8vC8H7Rwp6Tkdvvy8YFJ3Modbnmsx"
access_token_secret_test = "LYO1sF6pzZD4EV9sbgrYMO1UYzwC2N4SX8Z5V2bapVKug"

class StdOutListener( StreamListener ):

    def __init__( self ):
        self.tweetCount = 0

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)


    def on_data( self, data ):
        auth = OAuthHandler(consumer_key_real, consumer_secret_real)
        auth.secure = True
        auth.set_access_token(access_token_real, access_token_secret_real)

        api = API(auth)
        print("Entered on_data()")
        decoded = json.loads(data)
        if('direct_message' in decoded.keys()):
            print decoded['direct_message']['text']
            if('https://t.co/' in decoded['direct_message']['text']):
                tweetid = decoded['direct_message']['entities']['urls'][0]['expanded_url'].split('/')[5]
                if(decoded['direct_message']['text'].split(' ')[0] != 'https://t.co'):
                    tweet = decoded['direct_message']['text'].split(' ')
                    tweet.remove(tweet[len(tweet) - 1])
                    final = ' '.join(tweet)
                    print '@'+decoded['direct_message']['entities']['urls'][0]['expanded_url'].split('/')[3]+' '+final
                    api.update_status('@'+decoded['direct_message']['entities']['urls'][0]['expanded_url'].split('/')[3]+' '+final)
        return True

    def on_error( self, status ):
        print(status)

def main():

    try:
        auth = OAuthHandler(consumer_key_real, consumer_secret_real)
        auth.secure = True
        auth.set_access_token(access_token_real, access_token_secret_real)

        api = API(auth)

        # If the authentication was successful, you should
        # see the name of the account print out
        print(api.me().name)

        stream = Stream(auth, StdOutListener())

        stream.userstream()

    except BaseException as e:
        print("Error in main()", e)

if __name__ == '__main__':
    main()
