from bs4 import BeautifulSoup
import requests
import csv
import os


def init():

    state = {}

    base_url_start = "https://www.hockey-reference.com/draft/NHL_"
    base_url_end = "_entry.html"

    start_year = 2000
    end_year = 2019
    years = [i for i in range(start_year, end_year + 1)]
    year_dict = dict([(year, base_url_start + str(year) + base_url_end) for year in years])

    state['year_dict'] = year_dict
    state['start_year'] = start_year
    state['end_year'] = end_year

    return year_dict

def run(year_dict):

    records_by_year = {}

    for year, url in year_dict.items():

        # setup and get the HTML page
        response = requests.get(url)
        content = response.content

        # create the soup object
        soup = BeautifulSoup(content, 'html.parser')

        column_ids = []
        column_labels = {}
        all_records = []

        stat_table = soup.find('table', id="stats")

        header = stat_table.find('thead').find_all('tr')[1]
        for c in header.find_all('th'):
            cid = c.attrs['data-stat']
            column_ids.append(cid)
            column_labels[cid] = c.string

        body = stat_table.find('tbody')

        for r in body.find_all(tr_no_class):
            record = {}
            for cid in column_ids:
                record[cid] = r.find(attrs={"data-stat": cid}).string

            all_records.append(record)

        records_by_year[year] = {"columns": column_labels, "records": all_records}

    return records_by_year


def pythonize_label(label):
    return label.lower().replace(' ', '_').strip()

def does_not_have_class(tag):
    return not tag.has_attr('class')

def tr_no_class(tag):
    return does_not_have_class(tag) and tag.name == 'tr'

def write_csv_by_year(records_by_year, write_dir = None):
    if write_dir:
        try:
            os.mkdir(write_dir)
        except Exception:
            pass
    for year, year_vals in records_by_year.items():
        column_names = year_vals['columns']
        records = year_vals['records']
        filename = str(year) + '_draft.csv'
        write_csv_from_records(filename, column_names, records, write_dir=write_dir)

def write_csv_from_records(file, column_ids, records, write_dir = None):
    with open(os.path.join(write_dir, file), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = column_ids)
        writer.writeheader()
        for record in records:
            # records a list of dictionaries
            writer.writerow(record)
    csvfile.close()


if __name__ == "__main__":
    records_by_year = run(init())
    write_csv_by_year(records_by_year, write_dir = 'data')
