import random
import time
from selenium import webdriver
import pandas as pd
import concurrent.futures
import csv


def get_birthday(player_link):
    driver2 = webdriver.Chrome('./chromedriver.exe')
    driver2.get('https://www.flashscore.com' + player_link)
    time.sleep(random.uniform(3.5, 4.0))
    birthday_raw = driver2.find_element_by_xpath('.//span[@class="jsl-age"]').text
    birthday = birthday_raw.split("(")[1].lstrip().split(")")[0]
    time.sleep(0.2)
    driver2.close()
    time.sleep(0.2)
    print(birthday)
    return birthday


class ScrapeMatch:
    def __init__(self, match_link, output_filename, chromedriver_path='./chromedriver.exe'):
        self.match_link = match_link.split("#")[0] + '#lineups;1'
        self.output_filename = output_filename
        self.chromedriver_path = chromedriver_path
        self.driver = webdriver.Chrome(self.chromedriver_path)
        self.league = None
        self.date = None
        self.club_home = None
        self.club_away = None
        self.goals_home = None
        self.goals_away = None
        self.players_links = []
        self.players_home_paths = None
        self.players_away_paths = None
        self.lineup_home = None
        self.lineup_away = None
        self.df = pd.DataFrame()

        self.export_to_cvs()

    def export_to_cvs(self):
        self.match_scrape()
        self.df.to_csv(self.output_filename + '.csv')


    def match_scrape(self):

        self.driver.get(self.match_link)
        time.sleep(random.uniform(5.0, 6.0))
        self.league = self.driver.find_element_by_xpath('//span[@class="description__country"]/a').text
        self.date = self.driver.find_element_by_id('utime').text
        club_home_path = self.driver.find_element_by_xpath('//div[@class="team-text tname-home"]')
        club_away_path = self.driver.find_element_by_xpath('//div[@class="team-text tname-away"]')
        score_path = self.driver.find_element_by_xpath('//div[@class="current-result"]')
        players_home_paths = self.driver.find_elements_by_xpath('//td[@class="summary-vertical fl"]')
        players_away_paths = self.driver.find_elements_by_xpath('//td[@class="summary-vertical fr"]')

        self.club_home = club_home_path.find_element_by_xpath('.//a[@href="#"]').text
        self.club_away = club_away_path.find_element_by_xpath('.//a[@href="#"]').text

        self.goals_home = score_path.find_element_by_xpath('.//span[1]').text
        self.goals_away = score_path.find_element_by_xpath('.//span/span[2]').text

        self.lineup_home = self.players_scrape(players_home_paths, 'h')
        self.lineup_away = self.players_scrape(players_away_paths, 'a')

        columns_names = ['Home_Away', 'Name', 'Jersey_Num', 'Nationality', 'pos_left', 'pos_top', 'player_link']
        df1 = pd.DataFrame(self.lineup_home, columns=columns_names)
        df2 = pd.DataFrame(self.lineup_away, columns=columns_names)
        self.df = self.df.append(df1, ignore_index=True)
        self.df = self.df.append(df2, ignore_index=True)
        self.df.insert(0, 'League', self.league, True)
        self.df.insert(0, 'Date', self.date, True)

        self.driver.quit()

    def players_scrape(self,  players_paths, ha):
        # Recorro solo a los primeros 11 jugadores que he encontrado (para evitar substitutos, banca y coach)
        lineup = []
        x = 0
        player_pos_search = 1
        num_found = []
        players_paths = players_paths[:11]
        for player_path in players_paths:
            try:
                name = player_path.find_element_by_xpath('.//a[@href="#"]').text
                jersey_num = player_path.find_element_by_xpath('.//div[@class="time-box"]').text
                nationality = player_path.find_element_by_xpath('.//span[1]').get_attribute('title')
                player_link_raw = player_path.find_element_by_xpath('.//a[@href="#"]').get_attribute('onClick')
                player_link = player_link_raw.split("'")[1].lstrip().split("'")[0]
                # get_birthday(player_link)
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

                player_row = [ha, name, jersey_num, nationality, pos_left, pos_top, player_link]
                # player_row = [ha, name, jersey_num, nationality, player_link]
                lineup.append(player_row)
            except:
                next
        return lineup

start = time.perf_counter()

lastMatch = ScrapeMatch('https://www.flashscore.com/match/2JDks1o7/#match-summary', 'LastMatch')
finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')