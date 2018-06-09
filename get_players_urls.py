#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 07:00:10 2018

@author: joseramon
"""

import bs4
from unidecode import unidecode
from urllib import unquote
import time

import selenium_func as sel

from helper_functions import read_from_file, append_to_file

"""
File paths where the data will be saved.
"""
TEAMS_FILE_PATH = "./data/teams_urls.txt"
PLAYERS_FILE_PATH = "./data/players_urls.txt"
PLAYERS_LOG_PATH = "./data/players_log.txt"


def iterate_through_players(start_idx):
    """
    Function that returns a list of urls of players for each team in team_urls.
    """
    
    teams_urls = read_from_file(TEAMS_FILE_PATH)
    server, driver = sel.start_server_and_driver()
    
    general_url = 'https://www.transfermarkt.com'
    length = len(teams_urls)
    
    for team in teams_urls[start_idx:]:
        list_of_players_urls = []

        counter = 0
        while True:
            try:
                driver.get(team)
                break
            except Exception:
                print('\n')
                print("Problem accessing {}".format(team))
                print("Let's try again.")
                print('\n')
                counter += 1
                if counter > 4:
                    append_to_file("Error on: " + team + "\n", PLAYERS_LOG_PATH)
                    append_to_file("Index: " + str(teams_urls.index(team)), PLAYERS_LOG_PATH)
                    break
        
        content = driver.page_source
        soup = bs4.BeautifulSoup(''.join(content), 'lxml')
        players_table = soup.find_all('div', class_='responsive-table')
        
        try:
            if players_table != None:
                players_trs = players_table[0].find_all('tr', class_=['even', 'odd'])
                
            if players_trs != None:
                for player in players_trs:
                    player_as = player.find_all('a')
                    if player_as != None and len(player_as) > 0:
                            for as_ in player_as:
                                href = as_.attrs['href']
                                if 'profil/spieler' in href:
                                    processed = unquote(href)
                                    if type(processed) == 'unicode':
                                        processed = unidecode(processed)
                                    list_of_players_urls.append(general_url + processed)
                                    break
        except Exception:
            print('\n')
            print("Problem accessing {}".format(team))
            print('\n')
            append_to_file("Error on: " + team + "\n", PLAYERS_LOG_PATH)
            append_to_file("Index: " + str(teams_urls.index(team)), PLAYERS_LOG_PATH)

        if len(list_of_players_urls) > 0:
            for player in list_of_players_urls:
                append_to_file(player, PLAYERS_FILE_PATH)
                
        append_to_file("Successfully retrieved from: " + str(teams_urls.index(team)) + "/" + str(length), PLAYERS_LOG_PATH)
        time.sleep(2)
    
    sel.stop_server_and_driver(server, driver)
                                
    return

if __name__ == "__main__":
    iterate_through_players(0)
    
    
    
    