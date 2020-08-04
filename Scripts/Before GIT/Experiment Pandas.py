import random
from time import sleep
from selenium import webdriver
import csv
import pandas as pd
import numpy as np

# Experiment with dictionaries with zip
'''
lineup_home = [['h'], ['Arsenal'], ['3'], ['Aubameyang'], ['14'], ['Gabon'], ['120'], ['62'], ['17.06.1989']]
lineup_away = ['a', 'Anal', '3', 'Ang', '14', 'Gaon', '12', '2', '1.06.1989']
headers = ['HomeAway', 'Club', 'Goals', 'Player_Name', 'Jersey_Num',
           'Nationality', 'Pos_Left', 'Pos_Top', 'Birthday']
match_info_dict = dict(zip(headers, lineup_home))
#print(match_info_dict)
df = pd.DataFrame(match_info_dict)
league_col = ['SetsoAnal'] * 1
date_col = ['tuCumple'] * 1
df.insert(0, "League", league_col, True)
df['Date'] = date_col
print(df.__dict__)
'''
# Experiment with dictionaries
'''
player_row = {'HomeAway': ['h'], 'Club': ['Arsenal'], 'Goals': ['3'], 'Player_Name': ['Aubameyang'],
              'Jersey_Num': ['14'], 'Nationality': ['Gabon'], 'Pos_Left': ['120'],
              'Pos_Top': ['62'], 'Birthday': ['17.06.1989']}

player_row2 = {'HomeAway': ['hd'], 'Club': ['dafadsf'], 'Goals': ['4'], 'Player_Name': ['agfsd'],
              'Jersey_Num': ['41'], 'Nationality': ['Gabon'], 'Pos_Left': ['100'],
              'Pos_Top': ['34'], 'Birthday': ['01.06.1966']}

df1 = pd.DataFrame(player_row)
df2 = pd.DataFrame(player_row2)
df = df1.append(df2)
df = df.append(df1)
df = df.append(df)
df = df.append(df)

print(df)

'''
# Experiment from lists to DataFrame

# Calling DataFrame constructor
df = pd.DataFrame()

# list of strings
headers = ['HomeAway', 'Club', 'Goals', 'Player_Name', 'Jersey_Num',
           'Nationality', 'Pos_Left', 'Pos_Top', 'Birthday']
lineup_away1 = ['a', 'Tanned', '3', 'Ang', '14', 'Ganon', '12', '2', '1.06.1989']
lineup_home1 = ['h', 'Carlos', '5', 'Soka', '12', 'Mile', '32', '42', '17.04.1959']
lineup_away2 = ['a', 'Maria', '4', 'PAKA', '14', 'Ganon', '12', '2', '1.06.1989']
lineup_home2 = ['h', 'Andres', '5', 'LOL', '12', 'Mile', '32', '42', '17.04.1959']

lineup_away = [lineup_away1, lineup_away2]
lineup_home = [lineup_home1, lineup_home2]

table = [headers, lineup_away, lineup_home]
# print(table)

# Calling DataFrame constructor on list
#df = pd.DataFrame(headers)
df1 = pd.DataFrame(lineup_home)
df2 = pd.DataFrame(lineup_away)
df = df.append(df1, ignore_index=True)
df = df.append(df2, ignore_index=True)
df.insert(0, 'League', 'Premiere League', True)

print(df)
df.to_csv('PruebaMesta.csv')

'''
data = df
with open('Prueba' + ".csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
with open('Prueba' + ".csv", newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=' ')
    for row in data:
        print(', '.join(row))
'''

