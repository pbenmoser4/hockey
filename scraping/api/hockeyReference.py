import pprint
from bs4 import BeautifulSoup, Comment

from request import HockeyRequest

class HockeyReference(object):
    """docstring for HockeyReference."""

    search_params = {
        "stats": {

        }
    }

    def __init__(self):
        super(HockeyReference, self).__init__()

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

    def __extract_comments(self, soup):
        all_comments = BeautifulSoup("", "lxml")
        comments =  soup.find_all(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            all_comments.append(BeautifulSoup(comment.string, "lxml"))
        return all_comments

    def __stat_table(self, soup, id):
        soup_table = soup.find('table', id=id)
        comment_table = self.__extract_comments(soup).find('table', id=id)
        return soup_table if soup_table else comment_table

    def __standard_skater_stat_table(self, soup):
        return self.__stat_table(soup, "stats_basic_plus_nhl")

    def __advanced_skater_stat_table(self, soup):
        return self.__stat_table(soup, "skaters_advanced")

    def __misc_skater_stat_table(self, soup):
        return self.__stat_table(soup, "stats_misc_plus_nhl")

    def __parse_table(self, table):
        # Get header information
        table_head = table.find('thead')
        header = table_head.find(lambda tag: tag.name == 'tr' and not tag.has_attr('class'))
        column_labels = {c['data-stat']: c['aria-label'] for c in header.find_all('th')}

        # Get row information
        table_body = table.find('tbody')
        table_rows = table_body.find_all('tr')
        table_row_data = []

        for row in table_rows:
            data = {td['data-stat']: td.string for td in row.find_all('td')}
            table_row_data.append(data)

        return {'header': column_labels, 'data': table_row_data}

    def get_player(self, player_name):
        """ Get player statistics for given player

        Requests player page from hockey-reference.com, and scrapes the returned
        html document to get standard, advanced, and miscellaneous stats as
        shown on the page.

        Args:
            player_name: string - the name of the player you're searching for

        Returns:
            dictionary with all of the stats for the given player:

            {'standard': 'data': [year1data, year2data, ...], 'header': {defs},
             'advanced': 'data': [year1data, year2data, ...], 'header': {defs},
             'misc': 'data': [year1data, year2data, ...], 'header': {defs}}
        """
        req = HockeyRequest("https://www.hockey-reference.com/")

        player_path = self.__player_url_path(player_name)
        soup = BeautifulSoup(req.get(player_path).text, features='lxml')

        return {
        "standard": self.__parse_table(self.__standard_skater_stat_table(soup)),
        "advanced": self.__parse_table(self.__advanced_skater_stat_table(soup)),
        "misc": self.__parse_table(self.__misc_skater_stat_table(soup))
        }

    def test(self, player):
        # document = self.get_player(player)
        return self.__parse_table(self.__advanced_skater_stat_table(document))


if __name__ == "__main__":
    ref = HockeyReference()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ref.get_player("Travis Konecny"))
    # print(ref.get_player("Travis Konecny").text)
