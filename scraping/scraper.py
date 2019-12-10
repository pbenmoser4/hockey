import requests

from bs4 import BeautifulSoup

class Scraper(object):
    """docstring for Scraper."""

    def __init__(self, document):
        super(Scraper, self).__init__()
        self.soup = BeautifulSoup(document)
