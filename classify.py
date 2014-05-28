from ast import literal_eval as make_list
from ast import literal_eval as make_tuple
import nltk
import nltk.classify
from sklearn.svm import LinearSVC
import operator


pos_patterns = []
for line in open("pos_patterns.txt"):
	pattern = make_tuple(line)
	pos_patterns.append(pattern)

neg_patterns = []
for line in open("neg_patterns.txt"):
	pattern = make_tuple(line)
	neg_patterns.append(pattern)

patterns = pos_patterns + neg_patterns

pos_features = []
neg_features = []

train = []

i = 0
for line in open("features_pos.txt"):
	line = line.rstrip("\n")
	labels = make_list(line)

	features = {}
	for j in range(0,len(labels)):
		features[j] = labels[j]

	pos_features.append(features)
	print(i)
	i = i + 1
	train.append((features, 1))

i = 0
for line in open("features_neg.txt"):
	line = line.rstrip("\n")
	labels = make_list(line)

	features = {}
	for j in range(0,len(labels)):
		features[j] = labels[j]

	neg_features.append(features)
	print(i)
	i = i + 1
	train.append((features, 0))

classifier = nltk.classify.SklearnClassifier(LinearSVC())
classifier.train(train)

test = []

i = 0
for line in open("features_pos_test.txt"):
	line = line.rstrip("\n")
	labels = make_list(line)

	features = {}
	for j in range(0,len(labels)):
		features[j] = labels[j]

	print(i)
	i = i + 1
	test.append(features)

i = 0
for line in open("features_neg_test.txt"):
	line = line.rstrip("\n")
	labels = make_list(line)

	features = {}
	for j in range(0,len(labels)):
		features[j] = labels[j]

	print(i)
	i = i + 1
	test.append(features)

results = []
for features in test:
	predicted = classifier.classify(features)
	results.append(predicted)
print(results)