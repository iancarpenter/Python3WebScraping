"""
Produces a CSV file in the same directory where this module is run from
containing the title, site, score, user id, comment count
"""
import requests
from bs4 import BeautifulSoup

PAGE = "https://news.ycombinator.com/"
OK = 200

# def get_hacker_news_information(soup):
#     '''Return a dictionary with the information from Hackernews'''
    
#     # news = soup.find_all('table', class_='itemlist')

#     #print(news[0])

#     for i in soup.find_all('table', class_='itemlist').find('tr'):
#         print(i.find('a', class_='storylink').text)        
        



# create csv file


if __name__ == "__main__":
    
    result = requests.get(PAGE)

    assert result.status_code == 200, f"Got status code {result.status_code} \\ which isn't a success"
    
    source = result.text

    soup = BeautifulSoup(source, 'html.parser')

    results = soup.find_all('tr', class_='athing')
    subtext = soup.find_all('td', 'subtext')
    
    result_working = []
    subtext_working = []
    combined = []
    counter = 0
    for result in results:
        # title = result.find('a', class_='storylink')        
        #if title is not None:            
        #    rows.append(title.text)                
        #print(result)
        #print(subtext[counter])        
                
        result_working.append(result)

        # top row of hacker news  
        rank = result.find('span', class_='rank')
        if rank is not None:
            print('the rank is ' + rank.text)

        title = result.find('a', class_='storylink')        
        if title is not None:            
            print('the title is ' + title.text)
    
        site_str = result.find('span', class_='sitestr')
        if site_str is not None:
            print('the site_str is ' + site_str.text)

        # second row of hacker news        
        
        subtext_working.append(subtext[counter])
        combined += result_working + subtext_working
        counter += 1                    

    print(combined[0])
    print(combined[1])

    
    