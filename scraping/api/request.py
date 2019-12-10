from urllib import parse

from requests import Request, Session

class HockeyRequest(object):
    """docstring for HockeyRequest."""

    def __init__(self, base_url):
        super(HockeyRequest, self).__init__()
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
        self.session = Session()

    def get(self, path):
        url = parse.urljoin(self.base_url, path)
        print(url)
        req = Request('GET', url, headers = self.headers)
        prepped = req.prepare()
        return self.session.send(prepped)
