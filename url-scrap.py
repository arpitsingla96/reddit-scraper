#!/usr/bin/python


from nltk.corpus import stopwords
import re
import httplib2
from bs4 import BeautifulSoup
from ast import literal_eval

error_file = open('error.log', 'w')
HEADER = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36' }
SUBREDDIT_CATEGORIES = (
	'machinelearning',
	'compsci',
	'programming',
	'business',
	'web_design',
	'graphic_design',
	'Music',
	'movies',
	'books',
	'television',
	'science',
	'Physics',
	'chemistry',
	'biology',
	'math',
	'hacking',
	'ComputerSecurity',
	'worldnews',
	'news',
	'truenews'
	)


def get_page_content(subreddit, url) :
	connection = httplib2.Http()
	connection.follow_redirects = True
	try : (repsonse, html) = connection.request(url, headers=HEADER)
	except :
		error = (subreddit, url)
		error_file.write(str(error))
		html = ""
	return html

def get_cleantext(html) :
	soup = BeautifulSoup(html)
	[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	cleantext = soup.getText()
	cleantext = cleantext.encode('utf8', 'ignore')
	cleantext = " ".join(cleantext.split())
	return cleantext

def filter_stop_words(cleantext) :
	stop = stopwords.words('english')
	x = [i for i in re.findall(r"[\w'-]+", cleantext) if i.lower() not in stop]
	return " ".join(x)


def main() :
	for subreddit in SUBREDDIT_CATEGORIES :
		infile = open('subreddit_url/'+subreddit, 'r')
		outfile = open('subreddit_data/'+subreddit, 'w')
		data = literal_eval(infile.read())
		outfile.write('[\n')
		for url, topic in data:
			print(subreddit, url)
			html = get_page_content(subreddit, url)
			if html != "" :
				cleantext = get_cleantext(html)
				corpus = filter_stop_words(cleantext)
				outdata = (topic,corpus)
				outdata = str(outdata) + ',\n'
				outfile.write(outdata)
		outfile.write(']')

if __name__ == '__main__':
	main()