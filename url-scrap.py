#!/usr/bin/python


import os
from nltk.corpus import stopwords
import re
import httplib2
from bs4 import BeautifulSoup
from ast import literal_eval
from lxml import html

error_file = open('error.log', 'w')
HEADER = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (Khtml_data, like Gecko) Chrome/42.0.2311.135 Safari/537.36' }
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
	try : (repsonse, html_data) = connection.request(url, headers=HEADER)
	except :
		error = (subreddit, url)
		error_file.write(str(error))
		html_data = ""
	return html_data

def get_text(html_data) :
	try :
		root = html.fromstring(html_data)
		texts = root.xpath("//p/text()")\
			+ root.xpath("//div/text()")\
			+ root.xpath("//span/text()")\
			+ root.xpath("//pre/text()")
		plaintext = " ".join([text.strip() for text in texts])
	except :
		plaintext = ""
	return plaintext

def filter_stop_words(plaintext) :
	try :
		stop = stopwords.words('english')
		x = [i for i in re.findall(r"[\w'-]+", plaintext) if i.lower() not in stop]
		cleantext = " ".join(x)
	except :
		cleantext = ""
		error_file.write(url)
	return cleantext


def main() :
	if os.path.exists('subreddit_data/') == False :
		os.makedirs('subreddit_data/')
	for subreddit in SUBREDDIT_CATEGORIES :
		output = []
		infile = open('subreddit_urls/'+subreddit, 'r')
		outfile = open('subreddit_data/'+subreddit, 'w')
		for url in infile.readlines() :
			html_data = get_page_content(subreddit, url)
			if html_data == "" : continue
			plaintext = get_text(html_data)
			if plaintext == "" : continue
			cleantext = filter_stop_words(plaintext)
			if cleantext == "" : continue
			output.append(cleantext)
		outfile.write(str(output))



if __name__ == '__main__':
	main()