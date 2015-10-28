import re
import csv
import time
import random

from bs4 import BeautifulSoup
import requests

PAGE_URL = "http://runningintheusa.com/Race/Statistics.aspx"
GROUPS = {'County', 'City', 'RaceEvent'}
STATES = {'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
          'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH',
          'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'}
# the url variable is called as Special.
SPECIALS = {'', 'marathon', 'halfmarathon', 'mid', '10K', '5K', 'trail', 'ultra', 'triathlon', 'duathlon', 'other'}


def strip_html_whitespace(html_text):
    """
    Strips the page of extraneous html between the tags.

    :param html_text:
    :return:
    """
    html_text = re.sub(">\s*", ">", html_text)
    html_text = re.sub("\s*<", "<", html_text)
    return html_text


def parse_page(file_name, page_url):
    '''
    Parses the html table and writes a CSV file out of it.

    :param file_name: the csv file to be saved.
    :param page_url: url of the page being accessed.
    :return:
    '''
    page = requests.get(page_url)
    page = strip_html_whitespace(page.text);

    soup = BeautifulSoup(page, "lxml")
    div = soup.find(id="ctl00_MainContent_UpatePanel1")
    table = div.next_sibling.next_sibling

    with open('../output/' + file_name + '.csv', 'w') as f:
        writer = csv.writer(f)
        for row in table.find_all('tr'):
            each_row = [col.text for col in row.find_all('td')]
            # print(each_row)
            writer.writerow(each_row)


def by_special():
    '''
    fetch as per race type

    :return:
    '''
    for special in SPECIALS:
        page_url = PAGE_URL + '?Group=State&Special=' + special
        if special == '':
            special = 'all'
            print('parsing for ' + special)

        # running in the usa, just blocked me, so keeping some gap between the program when accessing the URLs
        time.sleep(5 + random.randint(2, 20))
        parse_page('All_States_' + special, page_url)


def by_group_state():
    '''
    Fetch data for each group per state.
    :return:
    '''
    for group in GROUPS:
        for state in STATES:
            page_url = PAGE_URL + '?Group=' + group + '&State=' + state
            print('parsing for ' + group + ' ' + state)
            file_name = group + '_' + state

            # running in the usa, just blocked me, so keeping some gap between the program when accessing the URLs
            time.sleep(5 + random.randint(2, 45))
            parse_page(file_name, page_url)


# Main program
print('parsing by special')
by_special()
by_group_state()
