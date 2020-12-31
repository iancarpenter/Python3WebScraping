"""
Produces a CSV file in the same directory where this module is run from
containing the title, site, score, user id, comment count
"""
import csv
import requests
from bs4 import BeautifulSoup

PAGE = "https://news.ycombinator.com/"
OK = 200
CSV_HEADER = ["rank", "title", "site_str", "score", "hn_user" , "age", "comment_count"]
CSV_FILE_NAME = 'hn.csv'

def first_row_of_hacker_news(result):
    
    rank_rtn = ''
    title_rtn = ''
    site_str_rtn = ''

    # first row of hacker news  
    rank = result.find('span', class_='rank')
    if rank is not None:
        rank_rtn = rank.text

    title = result.find('a', class_='storylink')        
    if title is not None:            
        title_rtn = title.text

    site_str = result.find('span', class_='sitestr')
    if site_str is not None:
        site_str_rtn = site_str.text
    
    return rank_rtn, title_rtn, site_str_rtn


def second_row_of_hacker_news(hn_second_line, counter):
    # second row of hacker news
    
    score_rtn = ''
    hn_user_rtn = ''
    age_rtn = ''
    comment_count_rtn = ''

    score = hn_second_line[counter].find('span', class_='score')        
    if score is not None:
        score_rtn = score.text

    hn_user = hn_second_line[counter].find('a', class_='hnuser')        
    if hn_user is not None:
        hn_user_rtn = hn_user.text

    age_enclosing_tag = hn_second_line[counter].find('span', class_='age')
    age = age_enclosing_tag.find('a')
    if age is not None:
        age_rtn = age.text
    
    # the comment count is in a block of html that requires some extra steps to extract. 
    # Two solutions I found, one using a lambda and one using find_next_sibling
    #comment_count = hn_second_line[counter].find(lambda tag:tag.name=="a" and "comments" in tag.text)        
    comment_count = hn_second_line[counter].find('span', class_='age').find_next_sibling('a').find_next_sibling('a')
    
    if comment_count is not None:              
        comment_count_rtn = comment_count.text

    return score_rtn, hn_user_rtn, age_rtn, comment_count_rtn

def get_html():
    
    result = requests.get(PAGE)

    assert result.status_code == 200, f"Got status code {result.status_code} \\ which isn't a success"
    
    source = result.text

    soup = BeautifulSoup(source, 'html.parser')

    return soup


def extract_hn_to_list(hn_first_line, hn_second_line):
    
    counter = 0

    data = []

    for result in hn_first_line:

        # top row of hacker news  
        rank, title, site_str = first_row_of_hacker_news(result)

        # second row of hacker news
        score, hn_user, age, comment_count = second_row_of_hacker_news(hn_second_line, counter)                

        data.append([rank, title, site_str, score, hn_user, age, comment_count])

        counter += 1  
    
    return data


def create_csv_file(hn_list):
    with open(CSV_FILE_NAME, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        # wr.writerow(["rank", "title", "site_str", "score", "hn_user" , "age", "comment_count"])
        wr.writerow(CSV_HEADER)
        for i in hn_list:
            wr.writerow(i)


def scrape_hn_front_page():
        
    soup = get_html()
    
    hn_first_line = soup.find_all('tr', class_='athing')
    
    hn_second_line = soup.find_all('td', 'subtext')
        
    hn_list = extract_hn_to_list(hn_first_line, hn_second_line)                    

    create_csv_file(hn_list)

                
if __name__ == "__main__":
    scrape_hn_front_page()    
    