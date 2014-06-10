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