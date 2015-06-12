#!/bin/sh


python reddit-scraper.py >> output.txt
python separator.py
python url-scraper.py
