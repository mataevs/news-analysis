import sys
sys.path.insert(1, '/usr/local/lib/python2.7/site-packages')
sys.path.insert(1, '/usr/local/lib/python2.7/site-packages/lxml-3.3.4-py2.7-macosx-10.9-x86_64.egg/lxml')

import feedparser
from goose import Goose
#from textblob import TextBlob

# Takes as input a feed address and returns a file with the articles
# contained in the feed.
def extractArticlesFromFeed(url, c):
	g = Goose()

	# Parse the URL feed
	d = feedparser.parse(url)

	feedName = d.feed.title.replace(' ', '_')

	# Open file for writing the article contents
	f = open(feedName, 'w')

	for entry in d.entries:
		# For each feed entry
		article = g.extract(url=entry.link)

		# Convert title and article body to ascii
		title = article.title.encode('ascii', 'ignore').strip()
		text = article.cleaned_text.encode('ascii', 'ignore').strip()

		# Write the article title and body in the file

		f.write('<article>\n')
		f.write("<class>" + str(c) + "</class>\n")
		f.write('<title>' + title + '</title>\n')
		f.write('<text>\n' + text + '</text>\n')
		f.write("</article>\n")

	f.close()

# Example feed for The Onion
#extractArticlesFromFeed("http://feeds.theonion.com/theonion/daily")
extractArticlesFromFeed("http://www.enduringvision.com/ev_rss.xml", 0)