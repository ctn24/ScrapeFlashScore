import random
from time import sleep
from selenium import webdriver
import csv

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome('./chromedriver.exe')

# Otro driver para el cumpleanos
#driver2 = webdriver.Chrome('./chromedriver.exe')

# Voy a la pagina que requiero
driver.get('https://www.flashscore.com/match/ttobio9E/#lineups;1')
sleep(random.uniform(5.0, 6.0))

'''
# Busco el boton para cargar mas informacion
boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
for i in range(3): # Voy a darle click en cargar mas 3 veces
    try:
        # le doy click
        boton.click()
        # espero que cargue la informacion dinamica
        sleep(random.uniform(8.0, 10.0))
        # busco el boton nuevamente para darle click en la siguiente iteracion
        boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
    except:
        # si hay algun error, rompo el lazo. No me complico.
        break
'''

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
League = driver.find_element_by_xpath('//span[@class="description__country"]/a').text
Date = driver.find_element_by_id('utime').text

Score = driver.find_element_by_xpath('//div[@class="current-result"]')
ClubH = driver.find_element_by_xpath('//div[@class="team-text tname-home"]')
ClubA = driver.find_element_by_xpath('//div[@class="team-text tname-away"]')

playersHome = driver.find_elements_by_xpath('//td[@class="summary-vertical fl"]')
playersAway = driver.find_elements_by_xpath('//td[@class="summary-vertical fr"]')

playerRow = []
lineup = []

x = 0

playerPosSearch = 1
NumFound = []
global pos_left
global pos_top
pos_left = ""
pos_top = ""


# Recorro cada uno de los jugadores que he encontrado
for player in playersHome:
    # Por cada jugador hallo el nombre
    try:
        if x >= 11:
            x = 0
            break
        Club = ClubH.find_element_by_xpath('.//a[@href="#"]').text
        Goals = Score.find_element_by_xpath('.//span[1]').text
        Name = player.find_element_by_xpath('.//a[@href="#"]').text
        JerseyNum = player.find_element_by_xpath('.//div[@class="time-box"]').text
        Nationality = player.find_element_by_xpath('.//span[1]').get_attribute('title')
        linkraw = player.find_element_by_xpath('.//a[@href="#"]').get_attribute('onClick')
        link = linkraw.split("'")[1].lstrip().split("'")[0]

        # Get birthday
        driver2 = webdriver.Chrome('./chromedriver.exe')
        driver2.get('https://www.flashscore.com' + link)
        sleep(random.uniform(3.5, 4.0))
        BirthdayRaw = driver2.find_element_by_xpath('.//span[@class="jsl-age"]').text
        Birthday = BirthdayRaw.split("(")[1].lstrip().split(")")[0]
        sleep(0.2)
        driver2.close()
        sleep(0.2)
        print(Birthday)
        while playerPosSearch < 11:
            posIteration = driver.find_element_by_id('h' + str(playerPosSearch))
            ActualNum = posIteration.find_elements_by_xpath('.//div')
            for textTry in ActualNum:
                try:
                    NumFound.append(int(textTry.text))
                except:
                    next
                if int(JerseyNum) in NumFound:
                    pos = driver.find_element_by_id('h' + str(playerPosSearch)).get_attribute('style')
                    pos_left = pos.split("left:")[1].lstrip().split("p")[0]
                    pos_top = pos.split("top:")[1].lstrip().split("p")[0]
                    #print('Left: ' + posL + ' Top: ' + posT)
                    NumFound = []
                    playerPosSearch = 99
            playerPosSearch += 1
        playerPosSearch = 1

        playerRow = [League, Date, Club, Goals, Name, JerseyNum, Nationality, pos_left, pos_top, Birthday]
        lineup.append(playerRow)
        x += 1
    except:
        next

for player in playersAway:
    # Por cada jugador hallo el nombre
    # Por cada jugador hallo el nombre
    try:
        if x >= 11:
            x = 0
            break
        Club = ClubA.find_element_by_xpath('.//a[@href="#"]').text
        Goals = Score.find_element_by_xpath('.//span/span[2]').text
        Name = player.find_element_by_xpath('.//a[@href="#"]').text
        JerseyNum = player.find_element_by_xpath('.//div[@class="time-box"]').text
        Nationality = player.find_element_by_xpath('.//span[1]').get_attribute('title')
        linkraw = player.find_element_by_xpath('.//a[@href="#"]').get_attribute('onClick')
        link = linkraw.split("'")[1].lstrip().split("'")[0]
        # Get birthday
        driver2 = webdriver.Chrome('./chromedriver.exe')
        driver2.get('https://www.flashscore.com' + link)
        sleep(random.uniform(3.5, 4.0))
        BirthdayRaw = driver2.find_element_by_xpath('.//span[@class="jsl-age"]').text
        Birthday = BirthdayRaw.split("(")[1].lstrip().split(")")[0]
        sleep(0.2)
        driver2.close()
        sleep(0.2)
        print(Birthday)
        while playerPosSearch < 11:
            posIteration = driver.find_element_by_id('a' + str(playerPosSearch))
            ActualNum = posIteration.find_elements_by_xpath('.//div')
            for textTry in ActualNum:
                try:
                    NumFound.append(int(textTry.text))
                except:
                    next
                if int(JerseyNum) in NumFound:
                    pos = driver.find_element_by_id('a' + str(playerPosSearch)).get_attribute('style')
                    pos_left = pos.split("left:")[1].lstrip().split("p")[0]
                    pos_top = pos.split("top:")[1].lstrip().split("p")[0]
                    NumFound = []
                    playerPosSearch = 99
            playerPosSearch += 1
        playerPosSearch = 1
        playerRow = [League, Date, Club, Goals, Name, JerseyNum, Nationality, pos_left, pos_top, Birthday]
        lineup.append(playerRow)
        x += 1
    except:
        next


# Cerrar el Navegador
driver.quit()

# Exportar la info a csv
data = lineup
with open("temp.csv", "w", newline="") as f:
   writer = csv.writer(f)
   writer.writerows(data)
with open('temp.csv', newline='') as csvfile:
 data = csv.reader(csvfile, delimiter=' ')
 for row in data:
   print(', '.join(row))
