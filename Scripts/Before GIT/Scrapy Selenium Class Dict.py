import random
from time import sleep
from selenium import webdriver
import csv
import pandas as pd


class ScrapeMatch:
    def __init__(self, match_link, output_filename, chromedriver_path='./chromedriver.exe'):
        self.match_link = match_link.split("#")[0] + '#lineups;1'
        self.output_filename = output_filename
        self.chromedriver_path = chromedriver_path
        self.driver = webdriver.Chrome(self.chromedriver_path)
        self.league = None
        self.date = None
        self.score_path = None
        self.club_home_path = None
        self.club_away_path = None
        self.players_home_paths = None
        self.players_away_paths = None
        self.lineup_home = None
        self.lineup_away = None
        self.match_info_dict = None
        self.export_to_cvs()

    def export_to_cvs(self):
        self.match_scrape()
        data = self.match_info_dict
        with open(self.output_filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        with open(self.output_filename + ".csv", newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=' ')
            for row in data:
                print(', '.join(row))

    def match_scrape(self):

        self.driver.get(self.match_link)
        sleep(random.uniform(5.0, 6.0))
        self.league = self.driver.find_element_by_xpath('//span[@class="description__country"]/a').text
        self.date = self.driver.find_element_by_id('utime').text
        self.club_home_path = self.driver.find_element_by_xpath('//div[@class="team-text tname-home"]')
        self.club_away_path = self.driver.find_element_by_xpath('//div[@class="team-text tname-away"]')
        self.score_path = self.driver.find_element_by_xpath('//div[@class="current-result"]')
        self.players_home_paths = self.driver.find_elements_by_xpath('//td[@class="summary-vertical fl"]')
        self.players_away_paths = self.driver.find_elements_by_xpath('//td[@class="summary-vertical fr"]')

        self.lineup_home = self.players_scrape(self.club_home_path, self.players_home_paths, 'h')
        self.lineup_away = self.players_scrape(self.club_away_path, self.players_away_paths, 'a')
        headers = ['HomeAway', 'Club', 'Goals', 'Player_Name', 'Jersey_Num',
                   'Nationality', 'Pos_Left', 'Pos_Top', 'Birthday']
        self.match_info_dict = dict(zip(headers, self.lineup_home + self.lineup_away))
        df = pd.DataFrame(self.match_info_dict)
        league_col = [self.league] * 22
        date_col = [self.date] * 22
        df['League'] = league_col
        df['Date'] = date_col
        self.driver.quit()

    def players_scrape(self, club_path, players_paths, ha):
        # Recorro cada uno de los jugadores que he encontrado
        lineup = []
        x = 0
        player_pos_search = 1
        num_found = []
        pos_left = 0
        pos_top = 0
        for player_path in players_paths:
            try:
                if x >= 11:
                    x = 0
                    break
                club = club_path.find_element_by_xpath('.//a[@href="#"]').text
                name = player_path.find_element_by_xpath('.//a[@href="#"]').text
                jersey_num = player_path.find_element_by_xpath('.//div[@class="time-box"]').text
                nationality = player_path.find_element_by_xpath('.//span[1]').get_attribute('title')
                player_link_raw = player_path.find_element_by_xpath('.//a[@href="#"]').get_attribute('onClick')
                player_link = player_link_raw.split("'")[1].lstrip().split("'")[0]
                if ha == 'h':
                    goals = self.score_path.find_element_by_xpath('.//span[1]').text
                else:
                    goals = self.score_path.find_element_by_xpath('.//span/span[2]').text
                # Get birthday
                driver2 = webdriver.Chrome(self.chromedriver_path)
                driver2.get('https://www.flashscore.com' + player_link)
                sleep(random.uniform(3.5, 4.0))
                birthday_raw = driver2.find_element_by_xpath('.//span[@class="jsl-age"]').text
                birthday = birthday_raw.split("(")[1].lstrip().split(")")[0]
                sleep(0.2)
                driver2.close()
                sleep(0.2)
                print(birthday)
                while player_pos_search < 11:
                    pos_iteration = self.driver.find_element_by_id(ha + str(player_pos_search))
                    actual_num = pos_iteration.find_elements_by_xpath('.//div')
                    for textTry in actual_num:
                        try:
                            num_found.append(int(textTry.text))
                        except:
                            next
                        if int(jersey_num) in num_found:
                            pos = self.driver.find_element_by_id(ha + str(player_pos_search)).get_attribute('style')
                            pos_left = pos.split("left:")[1].lstrip().split("p")[0]
                            pos_top = pos.split("top:")[1].lstrip().split("p")[0]
                            num_found = []
                            player_pos_search = 99
                    player_pos_search += 1
                player_pos_search = 1
                player_row = {'HomeAway': [ha], 'Club': [club], 'Goals': [goals], 'Player_Name': [name],
                              'Jersey_Num': [jersey_num], 'Nationality': [nationality], 'Pos_Left': [pos_left],
                              'Pos_Top': [pos_top], 'Birthday': [birthday]}
                lineup.append(player_row)
                x += 1
            except:
                next
        return lineup


lastMatch = ScrapeMatch('https://www.flashscore.com/match/2JDks1o7/#match-summary', 'LastMatch')
