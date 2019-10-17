from bs4 import BeautifulSoup

import requests
import csv
import os
import datetime


def init():

    state = {}

    base_url_start = "https://www.hockey-reference.com/draft/NHL_"
    base_url_end = "_entry.html"

    start_year = 1990
    end_year = 2019
    years = [i for i in range(start_year, end_year + 1)]
    year_dict = dict([(year, base_url_start + str(year) + base_url_end) for year in years])

    state['year_dict'] = year_dict
    state['start_year'] = start_year
    state['end_year'] = end_year

    # return year_dict
    return state

def run(state):

    column_ids = ["year", "round"]
    column_labels = {"year": "Year", "round": "Draft Round"}
    all_records = []

    for year, url in state['year_dict'].items():
        now = datetime.datetime.now()
        print("%s -- Getting draft data for %d" % (now.strftime("%b %d %H:%M:%S"), year))
        soup = soup_from_url(url)

        stat_table = soup.find('table', id="stats")
        header = stat_table.find('thead').find_all('tr')[1]
        body = stat_table.find('tbody')

        cids = [c.attrs['data-stat'] for c in header.find_all('th')]
        clabels = dict([(c.attrs['data-stat'], c.string) for c in header.find_all('th')])

        # Catching any discrepancies between years hopefully
        column_ids = column_ids + [x for x in cids if x not in column_ids]
        column_labels = {**column_labels, **clabels}

        # start off at round 1
        round = 1

        for r in body.find_all('tr'):
            if r.has_attr('class'):
                if "over_header" in r.attrs["class"]:
                    round = r.find(attrs={"data-stat": "header_draft"}).string.split()[1]
            else:
                record = {"year": year, "round": round}
                for cid in cids:
                    record[cid] = r.find(attrs={"data-stat": cid}).string
                all_records.append(record)


    return {"columns": column_ids, "labels": column_labels, "records": all_records}

# def run_by_year(year_dict):
#
#     records_by_year = {}
#
#     for year, url in year_dict.items():
#
#         # setup and get the HTML page
#         response = requests.get(url)
#         content = response.content
#
#         # create the soup object
#         soup = BeautifulSoup(content, 'html.parser')
#
#         column_ids = []
#         column_labels = {}
#         all_records = []
#
#         stat_table = soup.find('table', id="stats")
#
#         header = stat_table.find('thead').find_all('tr')[1]
#         for c in header.find_all('th'):
#             cid = c.attrs['data-stat']
#             column_ids.append(cid)
#             column_labels[cid] = c.string
#
#         body = stat_table.find('tbody')
#
#         for r in body.find_all(tr_no_class):
#             record = {}
#             for cid in column_ids:
#                 record[cid] = r.find(attrs={"data-stat": cid}).string
#
#             all_records.append(record)
#
#         records_by_year[year] = {"columns": column_labels, "records": all_records}
#
#     return records_by_year


def pythonize_label(label):
    return label.lower().replace(' ', '_').strip()

def does_not_have_class(tag):
    return not tag.has_attr('class')

def tr_no_class(tag):
    return does_not_have_class(tag) and tag.name == 'tr'

def soup_from_url(url):
    res = requests.get(url)
    return BeautifulSoup(res.content, 'html.parser')

def write_csv_by_year(records_by_year, write_dir = None):
    if write_dir:
        create_directory(write_dir)
    for year, year_vals in records_by_year.items():
        column_names = year_vals['columns']
        records = year_vals['records']
        filename = str(year) + '_draft.csv'
        write_csv_from_records(filename, column_names, records, write_dir=write_dir)

def write_csv_from_records(file, column_ids, records, write_dir = None):
    if write_dir:
        create_directory(write_dir)
    now = datetime.datetime.now()
    print("%s -- Writing to file %s" % (now.strftime("%b %d %H:%M:%S"), file))
    with open(os.path.join(write_dir, file), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = column_ids)
        writer.writeheader()
        for record in records:
            # records a list of dictionaries
            writer.writerow(record)
    csvfile.close()

def create_directory(dirname):
    try:
        os.mkdir(dirname)
    except Exception:
        pass


if __name__ == "__main__":
    state = init()
    scraped_data = run(state)

    columns = scraped_data['columns']
    labels = scraped_data['labels']
    records = scraped_data['records']

    # print(columns)
    # print(labels)

    write_csv_from_records("all_data.csv", columns, records, "data")
