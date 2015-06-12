#!/usr/bin/python

import os
from ast import literal_eval

def filter_output() :
	input_file = open('output.txt', 'r')
	output_file = open('filtered_output.txt', 'w')
	output_file.write('[')
	for line in input_file :
		line = line.strip()
		if line[:4] == "" or line[:4] == "http" : pass
		else : output_file.write(line + ',\n')
	output_file.write(']')

def separate() :
	x=0
	input_file = open('filtered_output.txt', 'r')
	data = literal_eval(input_file.read())
	subreddit_old = ""
	for reddit, subreddit, url, topic in data:
		subreddit_new = subreddit
		if subreddit_new != subreddit_old :
			if x != 0 : output_file.write('\n]')
			else : x=1
			output_file = open('subreddit_urls/'+subreddit, 'w')
			output_file.write('[\n')
		else : output_file.write(",\n")
		link = (reddit,subreddit,url,topic)
		output_file.write("('" + "', '".join(link) + "')")
		subreddit_old = subreddit
	output_file.write('\n]')

def main() :
	filter_output()
	separate()
	os.remove('filtered_output.txt')
	print('done.')

if __name__ == '__main__' : main()