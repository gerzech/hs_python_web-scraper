import requests
from bs4 import BeautifulSoup
import string
import re
import os


def get_urlinfo():
    url_ = input('Input the URL:\n')
    valid_ = False
    if 'nature.com/articles' in url_:
        response_ = requests.get(url_, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if response_.status_code == 200:
            out_dict = {}
            soup = BeautifulSoup(response_.content, 'html.parser')
            out_dict['title'] = soup.find('title').text
            description_ = soup.find('meta', property="og:description")
            out_dict['description'] = description_.get("content", None)
            print(out_dict)
            valid_ = True
    if not valid_:
        print('Invalid page!')


def write_url():
    url_ = input('Input the URL:\n')
    status_code = requests.get(url_).status_code
    if status_code == 200:
        with open("source.html", "wb") as source_file:
            source_file.write(requests.get(url_).content)
        print('Content saved.')
    else:
        print(f'The URL returned {status_code}!')


def batch_save(url_, article_type):
    status_code = requests.get(url_).status_code
    if status_code == 200:
        url_list = []
        match_ = article_type + '</span>'
        soup = BeautifulSoup(requests.get(url_, headers={'Accept-Language': 'en-US,en;q=0.5'}).content, 'html.parser')
        for li in soup.find_all('li'):
            if match_ in str(li):
                href_ = re.search(r'/articles/d[0-9-]+', str(li))
                url_list.append('https://www.nature.com' + href_.group())
        path_ = 'C:/Users/gerze/PycharmProjects/Web Scraper/Web Scraper/task/Page_' + url_[-1:]
        os.mkdir(path_)
        for ele in url_list:
            article_ = requests.get(ele)
            article_soup = BeautifulSoup(article_.content, 'html.parser')
            article_title = path_ + '/'
            article_teaser = article_soup.find("p", {"class": "article__teaser"}).text.encode(encoding = 'UTF-8')
            for char in article_soup.title.text:
                if char not in string.punctuation:
                    if char in string.whitespace:
                        if article_title[-1] != "_":
                            article_title += '_'
                    else:
                        article_title += char
            with open(article_title + ".txt", "wb") as source_file:
                source_file.write(article_teaser)


def func_main():
    num_pages = int(input())
    article_type = input()
    for i in range(1, num_pages+1):
        url_ = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + str(i)
        batch_save(url_, article_type)


func_main()
