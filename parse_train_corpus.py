from textblob import TextBlob, Word
import commons
import operator

pos_articles, neg_articles = commons.parseArticleCollection(["onion.txt", "daily_currant.txt", "daily_mash.txt", "news_biscuit.txt", "chaser.txt", "cnn.txt", "nytimes.txt"])

def wordCount(pos_articles, neg_articles):
	wc = {}
	nowords = 0

	for article in pos_articles:
		text = article[1]
		title = article[0]

		articleBlob = TextBlob(title)

		sentences = articleBlob.sentences

		for sentence in sentences:

			words = sentence.words
			nowords = nowords + len(words)
			
			for word in words:
				lw = word.lower()

				if lw in wc:
					wc[lw] = wc[lw] + 1
				else:
					wc[lw] = 1

	for article in neg_articles:
		text = article[1]
		title = article[0]

		articleBlob = TextBlob(text)
		words = articleBlob.words
		nowords = nowords + len(words)

		sentences = articleBlob.sentences

		for sentence in sentences:

			words = sentence.words
			nowords = nowords + len(words)
			
			for word in words:
				lw = word.lower()

				if lw in wc:
					wc[lw] = wc[lw] + 1
				else:
					wc[lw] = 1

	print(nowords)

	return sorted(wc.iteritems(), key=operator.itemgetter(1)), nowords

words, nowords = wordCount(pos_articles, neg_articles)

def decideFrequencyWords(words, nowords):
	wordFreq = {}
	for word in words:
		freq = float(word[1]) * 1000 / nowords;
		if (freq > 2):
			wordFreq[word[0]] = True
		else:
			wordFreq[word[0]] = False

	f = open("word_freq.txt", "w")
	for word, freq in wordFreq.iteritems():
		f.write(word + " " + str(freq) + "\n")
	f.close()

	return wordFreq

wordFreq = decideFrequencyWords(words, nowords)

def getPatterns(pos_articles, neg_articles, wordFreq):
	patterns = {}

	for article in pos_articles:
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
						if not(pattern in patterns):
							patterns[pattern] = 1

	for article in neg_articles:
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
						if not(pattern in patterns):
							patterns[pattern] = -1
						else:
							patterns[pattern] = 0

	pos_patterns = []
	neg_patterns = []

	for key, value in patterns.iteritems():
		if value == 1:
			pos_patterns.append(key)
		elif value == -1:
			neg_patterns.append(key)

	return pos_patterns, neg_patterns

pos_patterns, neg_patterns = getPatterns(pos_articles, neg_articles, wordFreq)

print(len(pos_patterns))
print(len(neg_patterns))

f = open("pos_patterns.txt", "w")
for pattern in pos_patterns:
	f.write(str(pattern) + "\n")
f.close()

f = open("neg_patterns.txt", "w")
for pattern in neg_patterns:
	f.write(str(pattern) + "\n")
f.close()