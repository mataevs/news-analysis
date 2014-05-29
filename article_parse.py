from textblob import TextBlob
import newspaper

def readArticleCollectionFile(site, filename, c):
	f = open(filename, 'w')

	paper = newspaper.build(site, memoize_articles=False)

	print len(paper.articles)

	i = 0
	for article in paper.articles:
		article.download()
		article.parse()

		title = article.title.encode('ascii', 'ignore')
		text = article.text.encode('ascii', 'ignore')

		#article.nlp()
		#keywords = article.keywords
		#summary = article.summary.encode('ascii', 'ignore')

		f.write('<article>\n')
		f.write("<class>" + str(c) + "</class>\n")
		f.write('<title>' + title + '</title>\n')
		f.write('<text>\n' + text + '</text>\n')
		#f.write('<keywords>' + str(keywords) + '</keywords>\n')
		#f.write('<summary>' + summary + '</summary>\n')
		f.write("</article>\n")
		i = i + 1
		if i > 40:
			break
	f.close()


readArticleCollectionFile("http://www.private-eye.co.uk/", "pos_test2.txt", 0)