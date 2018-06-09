#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 15:45:42 2018

@author: joseramon
"""
import bs4
from unidecode import unidecode
from urllib import unquote

import selenium_func as sel

from helper_functions import read_from_file, append_to_file

"""
File paths where the data will be saved.
"""
COUNTRIES_FILE_PATH = "./data/countries_urls.txt"
TIERS_FILE_PATH = "./data/tiers_urls.txt"
TIERS_LOG_PATH = "./data/tiers_log.txt"

def iterate_through_tiers(start_idx):
    """
    Function that returns a list of the urls of the first and second tier of each
    country in countries_list.
    """
    
    countries_urls = read_from_file(COUNTRIES_FILE_PATH)
    server, driver = sel.start_server_and_driver()
    
    general_url = 'https://www.transfermarkt.com'
    
    for country in countries_urls[start_idx:]:
        list_of_tiers_urls = []
        
        counter = 0
        while True:
            try:
                driver.get(country)
                break
            except Exception:
                print('\n')
                print("Problem accessing {}".format(country))
                print("Let's try again.")
                print('\n')
                counter += 1
                if counter > 4:
                    append_to_file("Error on: " + country + "\n", TIERS_LOG_PATH)
                    append_to_file("Index: " + str(countries_urls.index(country)), TIERS_LOG_PATH)
                    break
            
        content = driver.page_source
        soup = bs4.BeautifulSoup(''.join(content), 'lxml')
        hrefs_tiers = soup.find_all('td', class_='hauptlink')
            
        if hrefs_tiers != None:
            for td in hrefs_tiers:
    
                hrefs_as = td.find_all('a')
                
                if hrefs_as != None:
                    if len(hrefs_as) == 0:
                        continue
                    if "verein" in hrefs_as[0].attrs['href']:
                        break
                    processed = unquote(hrefs_as[1].attrs['href'])
                    if type(processed) == 'unicode':
                        processed = unidecode(processed)
                    list_of_tiers_urls.append(general_url+processed)
                    
        if len(list_of_tiers_urls) > 0:
            for tier in list_of_tiers_urls:
                append_to_file(tier, TIERS_FILE_PATH)
                
        append_to_file("Successfully retrieved from: " + str(countries_urls.index(country)), TIERS_LOG_PATH)
        
    sel.stop_server_and_driver(server, driver)
    
    return

if __name__ == "__main__":
    iterate_through_tiers(0)
        