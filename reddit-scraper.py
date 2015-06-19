#!/usr/bin/python


import httplib
import time
from bs4 import BeautifulSoup
from separator import filter_output, separate
import os

URL = "http://www.reddit.com/r/"
HEADER = { 'User-Agent' : 'hubble-tags' }
CONNECTION = httplib.HTTPConnection('www.reddit.com')
dirname = 'subreddit_urls/'

REDDIT_CATEGORIES = [
	('programming', 'machinelearning', 150),
	('programming', 'compsci', 250),
	('programming', 'programming', 150),

	('business', 'business', 200),

	('design', 'web_design', 300),
	('design', 'graphic_design', 300),

	('entertaiment', 'Music', 150),
	('entertaiment', 'movies', 150),
	('entertaiment', 'books', 150),
	('entertaiment', 'television', 150),

	('science', 'science', 100),
	('science', 'Physics', 100),
	('science', 'chemistry', 100),
	('science', 'biology', 100),
	('science', 'math', 100),

	('security', 'networking', 200),
	('security', 'hacking', 200),
	('security', 'ComputerSecurity', 200),

	('worldnews', 'worldnews', 200),
	('worldnews', 'news', 200),
	('worldnews', 'truenews', 200),
	]


def get_soup(subreddit, partial_url) :
	CONNECTION.request('GET', '/r/'+subreddit+partial_url, headers=HEADER)
	html = CONNECTION.getresponse().read()
	time.sleep(2)
	soup= BeautifulSoup(html)
	return soup


def get_next_link(soup) :
	next_a_tag = soup.find('a', rel='nofollow next')
	if next_a_tag is not None : next_link = next_a_tag['href']
	else : next_link = ""
	return next_link


def output_url(output_file, soup, size) :
	post_a_tags = soup.find_all('a', class_='title may-blank ')
	for post_a_tag in post_a_tags :
		if post_a_tag['href'][:4] == 'http' :
			output_file.write(post_a_tag['href'])
			size+=1
	return size

def main() :
	if os.path.exists(dirname) == False :
		os.makedirs(dirname)
	for reddit, subreddit, limit in REDDIT_CATEGORIES :
		output_file = open(dirname + subreddit, 'w')
		url = URL + subreddit
		print(url)
		size = 0
		partial_url = ""
		while size<=limit :
			soup = get_soup(subreddit, partial_url)
			next_link = get_next_link(soup)
			if next_link == "" : break
			partial_url = next_link.split('/')[-1]
			size = output_url(output_file, soup, size)
		output_file.close()
	CONNECTION.close()

if __name__ == "__main__" : main()