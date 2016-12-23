#nlp test
import numpy
from sklearn import svm
from sklearn import datasets
#returns a sourcefile's array of sentences, dictionary of words with respective counts, and arbitrary (but consistently) ordered list of words
def sentencify(sourcefile):
	sentences = []
	for line in open(sourcefile,'r'):
		l1 = ''
		for i in range(len(line)):
			try:
				if line[i] != '\n':
					l1+=(line[i]) 
			except UnicodeEncodeError:
				pass
		line_sent = l1.lower().split(".")
		if len(sentences)>0:
			if len(line_sent)>0:
				sentences[-1]+=line_sent[0]
			sentences+=line_sent[1:]
		else:
			sentences = line_sent
	words = {}
	for x in sentences:
		for y in x.split(" "):
			words[y] = words.get(y,0)+1
	word_list = list(words)
	word_list.sort()
	while '' in sentences:
		sentences.remove('')
	return sentences, words, word_list

#simple helper method that counts the number of occurences of element in list_
def count(list_,element):
	lc = list_.copy()
	r= 0
	while element in lc:
		lc.remove(element)
		r+=1
	return r

#represents each sentence as a vector related to its relative frequency of words in the word_list
def vectorize(sentence, words, word_list):
	l = []
	for word in word_list:
		l.append(count(sentence.split(" "),word)*1.0/len(sentence.split(" "))*1/words.get(word,1)) #adds vector data on relative frequency of word
	return l

sentences,words,word_list = sentencify('posts.txt')
sentence_d = {}
for sentence in sentences:
	sentence_d[sentence] = vectorize(sentence,words,word_list)
tags = {} #blank tags dictionary (for user submitted tags)
print("A series of sentences will be presented to you.")
print("On a scale from 0-100, indicate the 'positivity' of the statement, where 100 represents an extremely positive statement.")
print("You will have to hit enter to submit each time. You will also have to hit enter an additional time when all sentences have been prompted.")
#allows user to rate sentences
with open('classify.txt') as f:
	for a in f.readlines():
		for sentence in sentences:
			tags[sentence] = a
l_vectors,l_tags = [],[]
for sentence in sentences:
	l_vectors.append(sentence_d[sentence])
	l_tags.append(tags[sentence])
l_tags,l_vectors = numpy.asarray(l_tags),numpy.asarray(l_vectors)
print(str(l_vectors)+"vectors in training")
train = svm.SVC()
train.fit(l_vectors,l_tags)
#forms our vectors and tags and submits them as appropriate into our virtual machine
test_sent,_,_1 = sentencify('test.txt')
#extracts sentences from test document
test_d = {}
for sentence in test_sent:
	test_d[sentence] = vectorize(sentence,words,word_list) # we use the dictionary and list ordering from the training data for consistency
l,lname = [],[]
for x in test_d:
	lname.append(x)
	l.append(test_d[x])
x = train.predict(numpy.asarray(l))#prints our predicted ratings
print("PREDICTED POSITIVITY LEVELS\n for")
for i in range(len(x)):
	print(lname[i]+" : "+str(x[i]))