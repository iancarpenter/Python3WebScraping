"""
Produces a CSV file in the same directory where this module is run from
containing the title, site, score, user id, comment count
"""
import requests
from bs4 import BeautifulSoup

PAGE = "https://news.ycombinator.com/"
OK = 200

def get_hacker_news_information(soup):
    '''Return a dictionary with the information from Hackernews'''
    news = soup.find_all('table', 'itemlist')

    print(news[0])

    # for n in news:
    #     print(n)
        



# create csv file


if __name__ == "__main__":
    result = requests.get(PAGE)

    assert result.status_code == 200, f"Got status code {result.status_code} \ which isn't a success"
    
    source = result.text

    soup = BeautifulSoup(source, 'html.parser')

    #print(soup)

    get_hacker_news_information(soup)