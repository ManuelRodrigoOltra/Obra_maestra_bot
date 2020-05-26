from bs4 import BeautifulSoup
import requests
from myDictionary import urlperretes
from random import randrange
import sys


class FilmScraperScore:

    def __init__(self, titulo, *args, **kwargs):
        # Get the website and parse to HTML
        url = 'https://www.imdb.com/find?q=' + ''.join(titulo)
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.item = self.getFilm()
        self.findScore = self.getScore(self.item)
        self.picture = self.getLinkImg(self.item)

    def getFilm(self):
        # Find the searchBar and add to the url website
        findSection = self.soup.find_all('table', class_='findList')
        return 'https://www.imdb.com/' + findSection[0].a['href']

    def getScore(self, urlFilm):
        # Get the new website after the search with the input and get the rating value
        pageFilm = requests.get(urlFilm)
        soup = BeautifulSoup(pageFilm.content, 'html.parser')
        return soup.find_all('span', itemprop='ratingValue')

    def getLinkImg(self, urlFilm):
        url = urlperretes[str(randrange(3))]
        pageFilm = requests.get(urlFilm)
        soup = BeautifulSoup(pageFilm.content, 'html.parser')
        findImg = soup.find_all('div', class_='poster')
        if findImg:
            return findImg[0].a.img['src']
        else:
            return url
