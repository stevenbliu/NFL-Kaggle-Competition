from bs4 import BeautifulSoup
import re
import webbrowser
import requests
from PIL import Image
from io import BytesIO
import urllib
import kivy
from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os

# Selenium to move to the proper page
url = 'https://www.mangareader.net/'

# Beautiful Soup, scrape the page
links = {}
chapters = {}

web = 'https://www.mangareader.net/nanatsu-no-taizai'
response = requests.get(web)
soup = BeautifulSoup(response.content, 'html.parser')

img_tags = soup.find_all('a')

# show images
# img = Image.open(BytesIO(response.content))
# img.show()

series = soup.title.text.split('Manga')[0][:-1]
chapters[series] = []
links[series] = []

# Links and Chapters
for i in img_tags:
    chapters[series].append(i.contents)
    links[series].append(i['href'])
print('links:',links)

series_format = series.replace(' ', '-').lower()
print('series:',series_format)

filtered_links = filter(lambda x: series_format in x, links[series])
filtered_links = list(filtered_links)

temp_url = url + filtered_links[4][1:]
print(url,filtered_links[4][1:])
print('temp_url:', temp_url)
temp_response = requests.get(temp_url)
temp_soup = BeautifulSoup(temp_url, 'html.parser')
temp_img_tag = soup.src

print('src', temp_img_tag)

#img = Image.open(BytesIO(temp_img_tag))
#img.show()

webbrowser.open_new_tab(temp_url)