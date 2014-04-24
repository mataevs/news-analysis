import feedparser
from goose import Goose
#from textblob import TextBlob

# Takes as input a feed address and returns a file with the articles
# contained in the feed.
def extractArticlesFromFeed(url):
	g = Goose()

	# Parse the URL feed
	d = feedparser.parse(url)

	feedName = d.feed.title.replace(' ', '_')
	date = d.feed.published.replace(' ', '_').replace(':', '_').replace(',', '_')

	# Open file for writing the article contents
	f = open(feedName + '_' + date, 'w')

	for entry in d.entries:
		# For each feed entry
		article = g.extract(url=entry.link)

		# Convert title and article body to ascii
		title = article.title.encode('ascii', 'ignore').strip()
		text = article.cleaned_text.encode('ascii', 'ignore').strip()

		# Write the article title and body in the file
		f.write("<article>\n")
		f.write(title + '\n')
		f.write(text + '\n')
		f.write("</article>\n")

		#txt = TextBlob(text)
		#print(title + " " + str(txt.sentiment))

	f.close()

# Example feed for The Onion
extractArticlesFromFeed("http://feeds.theonion.com/theonion/daily")