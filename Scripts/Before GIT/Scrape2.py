# YouTube Link:

# Let's obtain the links from the following website:
# https://www.whitehouse.gov/briefings-statements/

# One of the things this website consists of is records of presidential
# briefings and statements.

# Goal: Extract all of the links on the page that point to the
# briefings and statements.

import requests
from bs4 import BeautifulSoup

# result = requests.get('https://www.flashscore.com/match/ttobio9E/#match-summary')
result = requests.get('https://www.flashscore.com/match/ttobio9E/#lineups;1')
src = result.content
soup = BeautifulSoup(src, 'html.parser')
'''
urls = []
for a_tag in soup.find_all('a'):
    if "#" == a_tag.attrs['href']:
        hashtag_tag = a_tag
        urls.append(hashtag_tag.text)

print(urls)
'''
lineup = soup.find(id="lineups-content")
print(soup.prettify())
print(soup.find_all('a'))
















