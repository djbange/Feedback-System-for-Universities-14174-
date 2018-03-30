#https://github.com/gutfeeling/word_forms
""" Installation:

git clone https://github.com/gutfeeling/word_forms.git
sudo pip install -e word_forms

"""
"""GAIKWAD's ALGORITM TO PREDICT TAGS AND PERFORM SENTIMENT ANALYSIS ON A GIVEN SENTENCE"""

from word_forms.word_forms import get_word_forms
from nltk.corpus import wordnet as wn
from itertools import chain

#this part of the code will run as soon as server starts 
#add db query to find out all tags and convert it in a list 
from app.models import Tag
tags = list(Tag.objects.all())
# tags = []
# for i in range(len(tags_all)):
# 	tags.append(tags_all[i].tag_title)

#print (tags)

tags_synonyms = {tag:set(chain.from_iterable([word.lemma_names() for word in wn.synsets(tag.tag_title)])) for tag in tags}
#to find out all forms of that tag which is going to be used in sentence

#print(tags_synonyms)

optimised_tags = {}
for tag,syns in tags_synonyms.items():
	optimised_tags[tag] = set()
	for syn in syns:
		words = get_word_forms(syn)
		
		for key,values in words.items():
			for word in values:
				optimised_tags[tag].add(word)
from pprint import pprint as pp
#pp(optimised_tags)

#removing stop words from a sentence using NLTK
from nltk import word_tokenize
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))

def get_tags(sentence):
	optimised_sentence =  [i for i in sentence.lower().split() if i not in stop]
	print(optimised_sentence)

	#compare two lists 
	tags_in_sentence = []
	for word in optimised_sentence:
		if word not in stop:
			for key,values in optimised_tags.items():
				if word in values:
						tags_in_sentence.append(key.id)
	print("Tags in the sentence are",tags_in_sentence)
	if len(tags_in_sentence) == 0:
		return 5
	else:
		return tags_in_sentence[0]
	#get_sentiment(sentence)

#sentiment analysis part using VaderSentiment
"""

sudo pip install vaderSentiment

if you already have upgrade using "pip install --upgrade vaderSentiment"



"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(sentence):
	vs = analyzer.polarity_scores(sentence)
	vs.pop('compound')
	type = max(vs.items(),key=lambda x:x[1])[0]
	print("Sentiment is",type)
	return type

'''
for i in tags:
	words = get_word_forms(i)
	for key,val in words.items():
			for word in val:
				optimised_tags[i].append(word)
 

print 

from collections import defaultdict
optimised_tags = defaultdict(list)

optimised_tags = {}
for i in tags:
	words = get_word_forms(i)
	for key,val in words.items():
			for word in val:
				optimised_tags[i].append(word)

print(optimised_tags)
'''
'''
while(1):
	sentence = input("Enter sentence:")
	get_tags(sentence)
	'''