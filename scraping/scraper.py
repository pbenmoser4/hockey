import requests 

from bs4 import BeautifulSoup

class Scraper(object):
    """docstring for Scraper."""

    def __init__(self, arg):
        super(Scraper, self).__init__()
        self.arg = arg
