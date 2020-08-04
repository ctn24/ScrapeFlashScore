import random
from time import sleep
from selenium import webdriver
import csv


class ScrapeMatch:
    def __init__(self, match_link, output_filename, chromedriver_path='./chromedriver.exe'):
        self.match_link = match_link
        self.output_filename = output_filename
        self.driver = webdriver.Chrome(chromedriver_path)
        self.league = None
        self.date = None
        self.score = None
        self.club_home = None
        self.club_away = None
        self.players_home = None
        self.players_away = None
        self.ha = None

    def match_scrape(self):

        self.driver.get(self.match_link)
        sleep(random.uniform(5.0, 6.0))
        self.league = self.driver.find_element_by_xpath('//span[@class="description__country"]/a').text
        self.date = self.driver.find_element_by_id('utime').text
        self.club_home = self.driver.find_element_by_xpath('//div[@class="team-text tname-home"]')
        self.club_away = self.driver.find_element_by_xpath('//div[@class="team-text tname-away"]')
        self.score = self.driver.find_element_by_xpath('//div[@class="current-result"]')
        self.players_home = self.driver.find_elements_by_xpath('//td[@class="summary-vertical fl"]')
        self.players_away = self.driver.find_elements_by_xpath('//td[@class="summary-vertical fr"]')
        self.ha = 'h'

        self.players_scrape(self.league, self.date, self.club_home, self.score, self.players_home, self.ha,
                            self.driver, self.chromedriver_path)

    def players_scrape(self, league, date, club, score, players, ha, driver, chromedriver_path):
        # Recorro cada uno de los jugadores que he encontrado
        lineup = []
        x = 0
        player_pos_search = 1
        num_found = []
        global pos_left
        global pos_top
        pos_left = ""
        pos_top = ""
        for player in players:
            try:
                if x >= 11:
                    x = 0
                    break
                club = club.find_element_by_xpath('.//a[@href="#"]').text
                goals = score.find_element_by_xpath('.//span[1]').text
                name = player.find_element_by_xpath('.//a[@href="#"]').text
                jersey_num = player.find_element_by_xpath('.//div[@class="time-box"]').text
                nationality = player.find_element_by_xpath('.//span[1]').get_attribute('title')
                linkraw = player.find_element_by_xpath('.//a[@href="#"]').get_attribute('onClick')
                link = linkraw.split("'")[1].lstrip().split("'")[0]

                # Get birthday
                driver2 = webdriver.Chrome('./chromedriver.exe')
                driver2.get('https://www.flashscore.com' + link)
                sleep(random.uniform(3.5, 4.0))
                birthday_raw = driver2.find_element_by_xpath('.//span[@class="jsl-age"]').text
                birthday = birthday_raw.split("(")[1].lstrip().split(")")[0]
                sleep(0.2)
                driver2.close()
                sleep(0.2)
                print(birthday)
                while player_pos_search < 11:
                    pos_iteration = driver.find_element_by_id('h' + str(player_pos_search))
                    actual_num = pos_iteration.find_elements_by_xpath('.//div')
                    for textTry in actual_num:
                        try:
                            num_found.append(int(textTry.text))
                        except:
                            next
                        if int(jersey_num) in num_found:
                            pos = driver.find_element_by_id('h' + str(player_pos_search)).get_attribute('style')
                            pos_left = pos.split("left:")[1].lstrip().split("p")[0]
                            pos_top = pos.split("top:")[1].lstrip().split("p")[0]
                            # print('Left: ' + posL + ' Top: ' + posT)
                            num_found = []
                            player_pos_search = 99
                    player_pos_search += 1
                player_pos_search = 1

                player_row = [league, date, club, goals, name, jersey_num, nationality, pos_left, pos_top, birthday]
                lineup.append(player_row)
                x += 1
            except:
                next

    for player in players_away:
        # Por cada jugador hallo el nombre
        # Por cada jugador hallo el nombre
        try:
            if x >= 11:
                x = 0
                break
            club = club_a.find_element_by_xpath('.//a[@href="#"]').text
            goals = score.find_element_by_xpath('.//span/span[2]').text
            name = player.find_element_by_xpath('.//a[@href="#"]').text
            jersey_num = player.find_element_by_xpath('.//div[@class="time-box"]').text
            nationality = player.find_element_by_xpath('.//span[1]').get_attribute('title')
            linkraw = player.find_element_by_xpath('.//a[@href="#"]').get_attribute('onClick')
            link = linkraw.split("'")[1].lstrip().split("'")[0]
            # Get birthday
            driver2 = webdriver.Chrome('./chromedriver.exe')
            driver2.get('https://www.flashscore.com' + link)
            sleep(random.uniform(3.5, 4.0))
            birthday_raw = driver2.find_element_by_xpath('.//span[@class="jsl-age"]').text
            birthday = birthday_raw.split("(")[1].lstrip().split(")")[0]
            sleep(0.2)
            driver2.close()
            sleep(0.2)
            print(birthday)
            while player_pos_search < 11:
                pos_iteration = driver.find_element_by_id('a' + str(player_pos_search))
                actual_num = pos_iteration.find_elements_by_xpath('.//div')
                for textTry in actual_num:
                    try:
                        num_found.append(int(textTry.text))
                    except:
                        next
                    if int(jersey_num) in num_found:
                        pos = driver.find_element_by_id('a' + str(player_pos_search)).get_attribute('style')
                        pos_left = pos.split("left:")[1].lstrip().split("p")[0]
                        pos_top = pos.split("top:")[1].lstrip().split("p")[0]
                        num_found = []
                        player_pos_search = 99
                player_pos_search += 1
            player_pos_search = 1
            player_row = [league, date, club, goals, name, jersey_num, nationality, pos_left, pos_top, birthday]
            lineup.append(player_row)
            x += 1
        except:
            next

    # Cerrar el Navegador
    driver.quit()

    # Exportar la info a csv
    data = lineup
    with open(output_filename + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    with open(output_filename + ".csv", newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=' ')
        for row in data:
            print(', '.join(row))
