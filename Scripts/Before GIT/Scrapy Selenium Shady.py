import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
#driver = driver = webdriver.Firefox()
driver = webdriver.Chrome('./chromedriver.exe')
# Voy a la pagina que requiero
driver.get('https://www.flashscore.com/match/ttobio9E/#lineups;1')

sleep(5)

html_page_source = driver.page_source
soup = BeautifulSoup(html_page_source, 'html.parser')
lineups_soup = soup.find("div", {"class": "lineups-wrapper"})
table_rows = lineups_soup.find("tbody").find_all("tr")

for row in table_rows:
    if row.find("span"):
        country_name = row.find("span")['title']
        print(country_name)

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
playersHome = driver.find_elements_by_xpath('//td[@class="summary-vertical fl"]')
playersVisitor = driver.find_elements_by_xpath('//td[@class="summary-vertical fr"]')
# players = players.append(driver.find_elements_by_xpath('//tf[@class="even"'))
# print(players)
PlayerRow = []
LineupHome = []
LineupVisitor = []

# Recorro cada uno de los jugadores que he encontrado
for playerH in playersHome:
    # Por cada jugador hallo el nombre
    try:
        NombreH = playerH.find_element_by_xpath('.//a[@href="#"]').text
        JerseyNum = playerH.find_element_by_xpath('.//div[@class="time-box"]').text
        Nationality = playerH.find_element_by_xpath('.//span[@class="flag"]').get_attribute('title')
        linkrawH = playerH.find_element_by_xpath('.//a[@href="#"]').get_attribute('onClick')
        linkH = linkrawH.split("'")[1].lstrip().split("'")[0]
        PlayerRow = [NombreH, JerseyNum, linkH]
        LineupHome.append(PlayerRow)
    except:
        next
print(LineupHome)
print(len(LineupHome))
'''
for playerV in playersVisitor:
    # Por cada jugador hallo el nombre
    try:
        NombreV = playerV.find_element_by_xpath('.//a[@href="#"]').text
        LineupVisitor.append(NombreV)
    except:
        break
print(LineupVisitor)
print(len(LineupVisitor))
'''