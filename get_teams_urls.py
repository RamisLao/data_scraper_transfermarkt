#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 06:52:11 2018

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
TIERS_FILE_PATH = "./data/tiers_urls.txt"
TEAMS_FILE_PATH = "./data/teams_urls.txt"
TEAMS_LOG_PATH = "./data/teams_log.txt"


def iterate_through_teams(start_idx):
    """
    Function that returns a list of the urls of the teams in each of the tiers in TIERS.
    """
    
    tiers_urls = read_from_file(TIERS_FILE_PATH)
    server, driver = sel.start_server_and_driver()
    
    general_url = 'https://www.transfermarkt.com'
    
    length = len(tiers_urls)
    for tier in tiers_urls[start_idx:]:
        list_of_teams_urls = []
        
        counter = 0
        while True:
            try:
                driver.get(tier)
                break
            except Exception:
                print('\n')
                print("Problem accessing {}".format(tier))
                print("Let's try again.")
                print('\n')
                counter += 1
                if counter > 4:
                    append_to_file("Error on: " + tier + "\n", TEAMS_LOG_PATH)
                    append_to_file("Index: " + str(tiers_urls.index(tier)), TEAMS_LOG_PATH)
                    break
        
        content = driver.page_source
        soup = bs4.BeautifulSoup(''.join(content), 'lxml')
        
        
        teams_table = soup.find_all('div', class_='responsive-table')
        
        teams_trs = None
        if teams_table != None:
            if len(teams_table) > 0:
                teams_trs = teams_table[0].find_all('tr', class_=['even', 'odd'])
            
        if teams_trs != None:
            for team in teams_trs:
                team_as = team.find_all('a')
                
                if team_as != None:
                    if len(team_as) > 0:
                        team_name = team_as[1].attrs['href']
                        processed = unquote(team_name)
                        if type(processed) == 'unicode':
                            processed = unidecode(processed)
                        list_of_teams_urls.append(general_url + processed)
    
    
        if len(list_of_teams_urls) > 0:
            for team in list_of_teams_urls:
                append_to_file(team, TEAMS_FILE_PATH)
                
        append_to_file("Successfully retrieved from: " + str(tiers_urls.index(tier)) + "/" + str(length), TEAMS_LOG_PATH)
        time.sleep(1)
    
    sel.stop_server_and_driver(server, driver)
    
    return

if __name__ == "__main__":
    iterate_through_teams(142)
    
    