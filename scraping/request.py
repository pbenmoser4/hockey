from urllib import parse

from requests import Request, Session

class HockeyRequest(object):
    """docstring for HockeyRequest."""

    def __init__(self, base_url):
        super(HockeyRequest, self).__init__()
        self.base_url = base_url
        self.headers = None
        self.session = Session()

    def get(self, path):
        url = parse.urljoin(self.base_url, path)
        print(url)
        req = Request('GET', url, headers = self.headers)
        prepped = req.prepare()
        return self.session.send(prepped)


class HockeyReference(HockeyRequest):
    """docstring for HockeyReference."""

    def __init__(self):
        super(HockeyReference, self).__init__("https://www.hockey-reference.com/")

    def __id_from_name(self, player_name):
        max_letters = 5
        firstname, lastname = player_name.lower().split()
        if (firstname and lastname):
            return lastname.lower()[:5] + firstname.lower()[:2] + "01"
        else:
            return None

    def __player_url_path(self, player_name):
        player_last_name = player_name.lower().split()[1]
        return "/players/" + player_last_name[:1] + "/" + self.__id_from_name(player_name) + ".html"

    def get_player(self, player_name):
        player_path = self.__player_url_path(player_name)
        return self.get(player_path)

# Travis Konecny
# konectr01
# Claude Giroux
# giroucl01
# Bobby Orr
# orrbo01

if __name__ == "__main__":
    ref = HockeyReference()
    print(ref.get_player("Travis Konecny").text)
