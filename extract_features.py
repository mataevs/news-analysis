from ast import literal_eval as make_tuple
from textblob import TextBlob, Word
import nltk
import nltk.classify
from sklearn.svm import LinearSVC
import operator

# Read list of words and their frequency
words = {}
for line in open("word_freq.txt"):
	line = line.rstrip("\n").split(" ")
	words[line[0]] = line[1] == 'True'

pos_patterns = []
for line in open("pos_patterns.txt"):
	pattern = make_tuple(line)
	pos_patterns.append(pattern)

neg_patterns = []
for line in open("neg_patterns.txt"):
	pattern = make_tuple(line)
	neg_patterns.append(pattern)

patterns = pos_patterns + neg_patterns

def parseArticleCollection(files):

	pos_articles = []
	neg_articles = []

	for i in range(0,len(files)):
		f = files[i]

		articleStarted = False
		articleTitle = ''
		articleBody = ''
		articleClass = 0

		for line in open(f):
			line = line.rstrip('\n')

			if line == '<article>' or line == '</article>':
				continue

			if articleStarted:
				if line.endswith('</text>'):
					articleBody = articleBody + "\n" + line.replace("</text>", '')

					if (articleClass == 0):
						pos_articles.append((articleTitle, articleBody))
					else:
						neg_articles.append((articleTitle, articleBody))

					articleStarted = False

					articleTitle = ''
					articleBody = ''
					articleClass = 0
				else:
					articleBody = articleBody + "\n" + line
			else:
				if line == '<text>':
					articleStarted = True
				elif line.startswith('<title>'):
					articleTitle = line.replace("<title>", "").replace("</title>", "")
				elif line.startswith('<class>'):
					articleClass = int(line.replace('<class>', '').replace('</class>', ''))
	return pos_articles, neg_articles

#pos_articles, neg_articles = parseArticleCollection(["onion.txt", "daily_currant.txt", "daily_mash.txt", "news_biscuit.txt", "chaser.txt", "cnn.txt", "nytimes.txt"])

pos_articles, neg_articles = parseArticleCollection(["pos_test.txt", "neg_test.txt"])

def extractPatternsFromArticle(article, patterns, wordFreq):
	feature = [0] * len(patterns)

	text = article[1]

	art = TextBlob(text)
	for sent in art.sentences:
		for i in range(3, 7):
			ngrams = sent.ngrams(n=i)

			for ngram in ngrams:
				pattern = []
				usefulPattern = False
				achievablePattern = True
				noFreqWords = 0

				for word in ngram:
					word = word.lower()
					if word in wordFreq:
						if wordFreq[word]:
							pattern.append(word)
							noFreqWords = noFreqWords + 1
						else:
							pattern.append('CW')
							usefulPattern = True
					else:
						achievablePattern = False

				if usefulPattern and achievablePattern and (noFreqWords >= 2):
					pattern = tuple(pattern)
					
					if pattern in patterns:
						i = patterns.index(pattern)
						feature[i] = 1
	return feature


pos_features = []
neg_features = []

i = 0
for article in pos_articles:
	feature = extractPatternsFromArticle(article, patterns, words)
	pos_features.append(feature)
	print("pos" + str(i))
	i = i + 1

f = open("features_pos_test.txt", "w")
for feature in pos_features:
	f.write(str(feature) + "\n")
f.close()

i = 0
for article in neg_articles:
	feature = extractPatternsFromArticle(article, patterns, words)
	neg_features.append(feature)
	print("neg" + str(i))
	i = i + 1

f = open("features_neg_test.txt", "w")
for feature in neg_features:
	f.write(str(feature) + "\n")
f.close()
