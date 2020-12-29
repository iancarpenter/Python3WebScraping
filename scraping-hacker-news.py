"""
Produces a CSV file in the same directory where this module is run from
containing the title, site, score, user id, comment count
"""
import requests
from bs4 import BeautifulSoup

PAGE = "https://news.ycombinator.com/"
OK = 200

def first_row_of_hacker_news():
    # first row of hacker news  
    rank = result.find('span', class_='rank')
    if rank is not None:
        print('the rank is ' + rank.text)

    title = result.find('a', class_='storylink')        
    if title is not None:            
        print('the title is ' + title.text)

    site_str = result.find('span', class_='sitestr')
    if site_str is not None:
        print('the site_str is ' + site_str.text)


def second_row_of_hacker_news():
    # second row of hacker news
    score = subtext[counter].find('span', class_='score')        
    if score is not None:
        print('the score is ' + score.text)

    hn_user = subtext[counter].find('a', class_='hnuser')        
    if hn_user is not None:
        print('the hn user is ' + hn_user.text)

    age_enclosing_tag = subtext[counter].find('span', class_='age')
    age = age_enclosing_tag.find('a')
    if age is not None:
        print('the age is ' + age.text) 
    
    # the comment count is in a block of html that requires some extra steps to find. 
    # Two solutions I found, one using a lambda and one using find_next_sibling
    # comment_count = subtext[counter].find(lambda tag:tag.name=="a" and "comments" in tag.text)        
    comment_count = subtext[counter].find('span', class_='age').find_next_sibling('a').find_next_sibling('a')
    
    if comment_count is not None:              
        print('the comment count is ' + comment_count.text)

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
                        
        result_working.append(result)

        # top row of hacker news  
        first_row_of_hacker_news()

        # second row of hacker news
        second_row_of_hacker_news()
        
        subtext_working.append(subtext[counter])
        combined += result_working + subtext_working
        counter += 1                    

    print(combined[0])
    print(combined[1])

    
    