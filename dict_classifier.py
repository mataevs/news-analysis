import commons
from textblob import TextBlob
from textblob import Word
from topia.termextract import extract
from collections import Counter, OrderedDict
import operator
import nltk
import random
from nltk.collocations import *
import nltk.classify
from sklearn.svm import LinearSVC
import operator

def extract_keywords(article, stopwords):
	keywords = []

	title = article[0]
	text = article[1]

	# Extract words from title and make them keywords
	titleBlob = TextBlob(title)
	for word in titleBlob.words:
		if word.lower() not in stopwords:
			keywords.append(word.lower())

	# Extract most frequent words and make them keywords
	textBlob = TextBlob(text)
	numWords = len(textBlob.words)
	t = [x.lower() for x in textBlob.words if x.lower() not in stopwords]
	freq = Counter()
	for word in t:
		freq[word]+=1

	minSize = min(10, len(freq))
	kw = tuple(freq.most_common(minSize))
	kw = dict((x,y) for x, y in kw)

	for k in kw:
		articleScore = kw[k] * 1.0 / max(numWords, 1)
		kw[k] = articleScore * 1.5 + 1
	kw = sorted(kw.iteritems(), key = operator.itemgetter(1))
	kw.reverse()
	for k in kw:
		word = k[0]
		keywords.append(word)

	keywords = list(set(keywords))

	lm_keywords = []
	for keyword in keywords:
		lm_keywords.append(Word(keyword).lemmatize())

	return lm_keywords

def extract_features(article, poswords, negwords, badwords, keywords):
	title = article[0]
	text = article[1]

	titleBlob = TextBlob(title)
	textBlob = TextBlob(text)

	features = {}
	for w in keywords:
		features[w] = 0

	features['p'] = 0
	features['n'] = 0
	features['b'] = 0

	# features['!'] = float(text.count('!')) / len(textBlob.sentences) * 10 + title.count('!') * 1.5
	# features['?'] = float(text.count('?')) / len(textBlob.sentences) * 10 + title.count('?') * 1.5
	# features['"'] = float(text.count('"')) / len(textBlob.sentences) * 10 + title.count('"') * 1.5
	# features['...'] = float(text.count('...')) / len(textBlob.sentences) * 10 + title.count('...') * 1.5

	for word in titleBlob.words:
		w = Word(word.lower()).lemmatize()
		if w in poswords:
			features['p'] = features['p'] + 1.5
		if w in negwords:
			features['n'] = features['n'] + 1.5
		if w in badwords:
			features['b'] = features['b'] + 1.5
		if w in keywords:
			features[w] = features[w] + 1

	for word in textBlob.words:
		w = Word(word.lower()).lemmatize()
		if w in poswords:									
			features['p'] = features['p'] + 1
		if w in negwords:
			features['n'] = features['n'] + 1
		if w in badwords:
			features['b'] = features['b'] + 1
		if w in keywords:
			features[w] = features[w] + 1

	return features


stopwords = []
for line in open("data/stop_words.txt"):
	line = line.rstrip("\n")
	stopwords.append(line)

badwords = []
for line in open("data/bad_words.txt"):
	line = line.rstrip("\n")
	badwords.append(line)

negwords = []
for line in open("data/negative_words.txt"):
	line = line.rstrip("\n")
	negwords.append(line)

poswords = []
for line in open("data/positive_words.txt"):
	line = line.rstrip("\n")
	poswords.append(line)

p_articles, n_articles = commons.parseArticleCollection([
	"corpus/onion.txt", 
	"corpus/daily_currant.txt", 
	"corpus/daily_mash.txt", 
	"corpus/news_biscuit.txt", 
	"corpus/chaser.txt", 
	"corpus/cnn.txt", 
	"corpus/nytimes.txt", 
	"corpus/neg_test.txt", 
	"corpus/pos_test.txt"])

pos_order = []
for line in open("tmp/pos_order.txt"):
	pos_order.append(int(line.rstrip('\n')))

neg_order = []
for line in open("tmp/neg_order.txt"):
	neg_order.append(int(line.rstrip('\n')))

# Do here the selection of the 30 articles to be used as test
pos_order = pos_order[120:] + pos_order[:120]
neg_order = neg_order[120:] + neg_order[:120]

# Reorder the articles in a shuffled manner
pos_articles = [p_articles[i] for i in pos_order]
neg_articles = [n_articles[i] for i in neg_order]

# Partition the sets into training and test sets
train_pos_articles = pos_articles[30:]
train_neg_articles = neg_articles[30:]

test_pos_articles = pos_articles[:30]
test_neg_articles = neg_articles[:30]

print("pos train samples = " + str(len(train_pos_articles)))
print("neg train samples = " + str(len(train_neg_articles)))

# Extract the keywords corpus
keywords = []
i = 0
for article in train_pos_articles + train_neg_articles:
	k = extract_keywords(article, stopwords)
	keywords = keywords + k
	i = i + 1
keywords = list(set(keywords))

print("keywords = " + str(len(keywords)))

# Extract features for train sample
train_examples = []
for article in train_pos_articles:
	features = extract_features(article, poswords, negwords, badwords, keywords)
	train_examples.append((features, 1))
for article in train_neg_articles:
	features = extract_features(article, poswords, negwords, badwords, keywords)
	train_examples.append((features, 0))

# Train the classifier
classifier = nltk.classify.SklearnClassifier(LinearSVC())
classifier.train(train_examples)

# Extract features for test sample
test_examples = []
for article in test_pos_articles:
	features = extract_features(article, poswords, negwords, badwords, keywords)
	test_examples.append((features, 1))
for article in test_neg_articles:
	features = extract_features(article, poswords, negwords, badwords, keywords)
	test_examples.append((features, 0))

failures = 0

for t in test_examples:
	pc = classifier.classify(t[0])
	ec = t[1]
	if pc != ec:
		failures = failures + 1
		print(str(pc) + " " + str(ec) + " failures = " + str(failures))
	else:
		print(pc)