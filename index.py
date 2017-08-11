import time
import json
from config import *
import markovify

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

#Load Hierarchical Attention Network
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

def clean_str(string):
    """
    Tokenization/string cleaning for dataset
    Every dataset is lower cased except
    """
    string = re.sub(r"\\", "", string)    
    string = re.sub(r"\'", "", string)    
    string = re.sub(r"\"", "", string)    
    return string.strip().lower()

from nltk import tokenize

# Train Markov Chain
with open('encouraging.txt') as f:
    text = f.read()
text_model = markovify.Text(text)

print "Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict)
print classification_report(testclass, prediction_liblinear)


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            new = json.loads(data)['text'].replace('RT ', '')
            reviews = []
            texts = []

            text = BeautifulSoup(new)
            text = clean_str(text.get_text().encode('ascii','ignore'))
            texts.append(text)
            sentences = tokenize.sent_tokenize(text)
            reviews.append(sentences)

            tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
            tokenizer.fit_on_texts(texts)

            data = np.zeros((len(texts), MAX_SENTS, MAX_SENT_LENGTH), dtype='int32')

            for i, sentences in enumerate(reviews):
                for j, sent in enumerate(sentences):
                    if j< MAX_SENTS:
                        wordTokens = text_to_word_sequence(sent)
                        k=0
                        for _, word in enumerate(wordTokens):
                            if k<MAX_SENT_LENGTH and tokenizer.word_index[word]<MAX_NB_WORDS:
                                data[i,j,k] = tokenizer.word_index[word]
                                k=k+1                    
                                
            word_index = tokenizer.word_index
            print('Total %s unique tokens.' % len(word_index))

            print('Shape of data tensor:', data.shape)

            indices = np.arange(data.shape[0])
            np.random.shuffle(indices)
            data = data[indices]
            p = range(0, 2).index(max(loaded_model.predict(data)))

            if p == 1:
                user = json.loads(data)['user']['screen_name']
                api.update_status("@" + user + " " + text_model.make_short_sentence(138 - len(user)))

        except BaseException as e:
            print('&quot;Error on_data: %s&quot;' % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['anxiety', 'sadness', 'suicide', 'depression', 'sad'])
