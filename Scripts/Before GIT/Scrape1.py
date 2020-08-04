import requests
from bs4 import BeautifulSoup

URL = 'https://www.flashscore.com/match/ttobio9E/#match-summary'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup)
# print(soup.prettify())

'''
results = soup.find(id="utime")
# print(results.prettify())
soup = BeautifulSoup('<div id="utime" class="description__time">22.07.2020 14:15</div>', "html.parser")
# print(soup.prettify())
tag = soup.div
# print(tag)
# print(tag.name)
# print(tag.text)
print(tag.attrs)
print(tag['class'])
print(tag['id'])
del tag['id']
print(tag)
'''

