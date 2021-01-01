"""
Produces a CSV file in the same directory where this module is run from.
Each row contains the title, site, score, user id, comment count
"""
import csv
import requests
from bs4 import BeautifulSoup

PAGE = "https://news.ycombinator.com/"
OK = 200
CSV_HEADER = ["rank", "title", "site_str",
              "score", "hn_user", "age", "comment_count"]
CSV_FILE_NAME = 'hn.csv'


def first_row_of_hacker_news(story):
    ''' The first row of Hacker news contains the Rank, Title and the site address
        These are extracted into variables and returned to the caller. 

        Args: story: string containing a HTML fragment within which the required data
        is located 

        Returns: Strings: three variables rank_rtn, title_rtn, site_str_rtn
    '''

    rank_rtn = ''
    title_rtn = ''
    site_str_rtn = ''

    rank = story.find('span', class_='rank')
    if rank is not None:
        rank_rtn = rank.text

    title = story.find('a', class_='storylink')
    if title is not None:
        title_rtn = title.text

    site_str = story.find('span', class_='sitestr')
    if site_str is not None:
        site_str_rtn = site_str.text

    return rank_rtn, title_rtn, site_str_rtn


def second_row_of_hacker_news(hn_second_line, counter):
    ''' The second row of Hacker news contains the score, hn_user, age, comment_count

        These are extracted into variables and returned to the caller. 

        Args: hn_second_line: list containing a HTML fragments within which the required data
                              is located 
              counter: int which row from the list is required

        Returns: Strings: four variables; score_rtn, hn_user_rtn, age_rtn, comment_count_rtn
    '''
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
    comment_count = hn_second_line[counter].find(
        'span', class_='age').find_next_sibling('a').find_next_sibling('a')

    if comment_count is not None:
        comment_count_rtn = comment_count.text

    return score_rtn, hn_user_rtn, age_rtn, comment_count_rtn


def get_html():
    ''' Using the requests library for handling HTTP and beautiful soup to parse the HTML document
        When making a request, it will raise an assert error if anything other than 200 is retured 

       Args: None

       Return: soup: Parsed HTML document of the Hacker News website        
    '''

    result = requests.get(PAGE)

    assert result.status_code == OK, f"Got status code {result.status_code} \\ which isn't a success"

    source = result.text

    soup = BeautifulSoup(source, 'html.parser')

    return soup


def extract_hn_to_list(hn_first_line, hn_second_line):
    ''' Extracts information from the HTML fragments for the HacknerNews 
        first and and second lines and returns a list containing the information
        combined from both lines.
        
        Args: HTML fragments 

        Return: list: Containing the information for both lines combined

    '''
    counter = 0

    first_and_second_rows_combined = []

    for story in hn_first_line:

        rank, title, site_str = first_row_of_hacker_news(story)

        score, hn_user, age, comment_count = second_row_of_hacker_news(
            hn_second_line, counter)

        first_and_second_rows_combined.append([rank, title, site_str, score,
                     hn_user, age, comment_count])

        counter += 1

    return first_and_second_rows_combined


def create_csv_file(hn_list):
    ''' creates a csv file in the location that this module
        was run from. The filename is determined by the global
        constant CSV_FILE_NAME.    

        Args: hn_list(list): list of the hacker news stories to
        be written to csv file
        
        Return: None
    '''
    with open(CSV_FILE_NAME, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(CSV_HEADER)
        for i in hn_list:
            wr.writerow(i)


def scrape_hn_front_page():
    '''Entry point into the module. 
    
    Gets the Hacker news HTML then extracts the first and second line details for each story
    These are combined and added to a list which is then written out into a CSV file. 
    
    Args: None

    Returns: None
    '''

    soup = get_html()

    hn_first_line = soup.find_all('tr', class_='athing')

    hn_second_line = soup.find_all('td', 'subtext')

    hn_list = extract_hn_to_list(hn_first_line, hn_second_line)

    create_csv_file(hn_list)


if __name__ == "__main__":
    scrape_hn_front_page()
