from bs4 import BeautifulSoup
import requests
import re
import csv

PAGE_URL = "http://runningintheusa.com/Race/Statistics.aspx"


def strip_html_whitespace(html_text):
    """
    Strips the page of extraneous html between the tags.

    :param html_text:
    :return:
    """
    html_text = re.sub(">\s*", ">", html_text)
    html_text = re.sub("\s*<", "<", html_text)
    return html_text


# <tr>
#     <td class="StatisticsColumnHeader">State</td>
#     <td class="StatisticsColumnHeader">Jan</td>
#     <td class="StatisticsColumnHeader">Feb</td>
#     <td class="StatisticsColumnHeader">Mar</td>
#     <td class="StatisticsColumnHeader">Apr</td>
#     <td class="StatisticsColumnHeader">May</td>
#     <td class="StatisticsColumnHeader">Jun</td>
#     <td class="StatisticsColumnHeader">Jul</td>
#     <td class="StatisticsColumnHeader">Aug</td>
#     <td class="StatisticsColumnHeader">Sep</td>
#     <td class="StatisticsColumnHeader">Oct</td>
#     <td class="StatisticsColumnHeader">Nov</td>
#     <td class="StatisticsColumnHeader">Dec</td>
#     <td class="MenuGridViewHeader">Total</td>
# </tr>
def parse_page():
    rows = []

    page = requests.get(PAGE_URL)
    page = strip_html_whitespace(page.text);

    soup = BeautifulSoup(page, "lxml")
    div = soup.find(id="ctl00_MainContent_UpatePanel1")
    table = div.next_sibling.next_sibling

    with open('output_file.csv', 'w') as f:
        writer = csv.writer(f)
        for row in table.find_all('tr'):
            each_row = [col.text for col in row.find_all('td')]
            print(each_row)
            writer.writerow(each_row)


parse_page()
