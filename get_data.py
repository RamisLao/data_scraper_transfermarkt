#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 16:28:17 2018

@author: joseramon
"""
import bs4
import time
from collections import OrderedDict
import os

import selenium_func as sel

from helper_functions import read_from_file, append_to_file, append_to_tsv, append_to_csv, process_info

"""
File paths where the data will be saved.
"""
PLAYERS_FILE_PATH = "./data/players_urls.txt"
PLAYERS_CLEAN_FILE_PATH = "./data/players_clean_urls.txt"
TSV_FILE_PATH = "./data/transfermarkt_dataset_tsv.txt"
CSV_FILE_PATH = "./data/transfermarkt_dataset_csv.txt"
DATASET_LOG_PATH = "./data/transfermarkt_dataset_log.txt"

def clean_players():
    clean = []
    
    with open(PLAYERS_FILE_PATH, 'r') as f:
        for line in f.readlines():
            clean.append(line)
            
    clean_set = set(clean)
    
    with open(PLAYERS_CLEAN_FILE_PATH, 'w') as f:
        for player in clean_set:
            f.write(player)
            
def get_players_data(start_idx):
    """
    Get the required information about each of the players in players_urls.
    """
    
    players_urls = read_from_file(PLAYERS_CLEAN_FILE_PATH)
    server, driver = sel.start_server_and_driver()
    
    data_to_search = ['Name', 'Date of birth', 'Place of birth', 'Age', 'Height', 'Shoe size',
                    'Nationality', 'Position', 'Foot', 'Current club', 'Current market value',
                    'Highest market value']

    if os.path.isfile(TSV_FILE_PATH):
        pass
    else:
        append_to_tsv(data_to_search, TSV_FILE_PATH)
        
    if os.path.isfile(CSV_FILE_PATH):
        pass
    else:
        append_to_csv(data_to_search, CSV_FILE_PATH)
        
    length = len(players_urls)
    
    for player in players_urls[start_idx:10]:
        error = False
        
        defaults = OrderedDict([('Name',"Undefined"), ('Date of birth',"Undefined"), ('Place of birth',"Undefined"),
                                ('Age',"Undefined"), ('Height',"Undefined"), ('Shoe size',"Undefined"),
                                ('Nationality',"Undefined"), ('Position',"Undefined"), ('Foot',"Undefined"), 
                                ('Current club',"Undefined"), ('Current market value',"Undefined"), 
                                ('Highest market value',"Undefined")])
    
        counter = 0
        while True:
            try:
                driver.get(player)
                break
            except Exception:
                print('\n')
                print("Problem accessing {}".format(player))
                print("Let's try again.")
                print('\n')
                counter += 1
                if counter > 4:
                    append_to_file("Error on: " + player + "\n", DATASET_LOG_PATH)
                    append_to_file("Index: " + str(players_urls.index(player)), DATASET_LOG_PATH)
                    error = True
                    break
                
        if error == True:
            continue
        
        content = driver.page_source
        soup = bs4.BeautifulSoup(''.join(content), 'lxml')
        
        try:
            #Get the first object
            player_name_h1 = soup.find('div', class_='dataName')
            if player_name_h1 != None:
                defaults['Name'] = process_info(player_name_h1.h1.get_text().strip())
            
            #Get objects 2 to 9
            player_table = soup.find('div', class_='spielerdaten')
            if player_table != None:
                table_body = player_table.find_all('tr')
        
                if table_body != None and len(table_body) > 0:
                    for info in table_body:
                        info_name = info.find('th').string.strip().strip(':')
                        if info_name == 'Date of birth':
                            defaults[info_name] = process_info(info.find('td').a.get_text())
                        elif info_name == 'Place of birth':
                            if info.find('td').img != None:
                                defaults[info_name] = process_info(info.find('td').span.get_text().replace(u'\xa0', u' ').strip(' ')+', '+info.find('td').img.get('title'))
                            else:
                                defaults[info_name] = process_info(info.find('td').span.get_text().replace(u'\xa0', u' ').strip(' '))
                        elif info_name in ['Age', 'Height', 'Shoe size', 'Position', 'Foot']:
                            defaults[info_name] = process_info(info.find('td').string.strip().strip('\r').strip('\n').strip('\t').replace(u'\xa0', u' ').strip(' '))
                        elif info_name == 'Nationality':
                            national_images = info.find('td').find_all('img')
                            if len(national_images) < 2:
                                defaults[info_name] = process_info(national_images[0].get('title'))
                            else:
                                defaults[info_name] = process_info(national_images[0].get('title'))+\
                                ', '+process_info(national_images[1].get('title'))
                        elif info_name == 'Current club':
                            defaults[info_name] = process_info(info.find('td').find_all('a')[1].get_text())
                    
            
            #Get the last 2 objects
            player_value = soup.find('div', class_='marktwertentwicklung')
            if player_value != None:
                current_value = player_value.find(class_='zeile-oben')
                if current_value != None:
                    defaults['Current market value'] = process_info(current_value.find(class_='right-td').string.strip('\r').strip('\n').strip('\t'))
                highest_value = player_value.find(class_='zeile-unten')
                if highest_value != None:
                    value_strings = highest_value.find(class_='right-td')
                    value_strings.span.clear()
                    defaults['Highest market value'] = process_info(value_strings.get_text().strip('\r').strip('\n').strip('\t'))
        
        except Exception as e:
            print('\n')
            print("Problem accessing {}".format(player))
            print(str(e))
            print('\n')
            append_to_file("Error on: " + player + "\n", DATASET_LOG_PATH)
            append_to_file("Index: " + str(players_urls.index(player)), DATASET_LOG_PATH)
            error = True
        
        #Append data to list of players   
        if error == False:
            player_data = [value for key, value in defaults.items()]
            if len(player_data) > 0:
                append_to_tsv(player_data, TSV_FILE_PATH)
                append_to_csv(player_data, CSV_FILE_PATH)
                
            append_to_file("Successfully retrieved from: " + str(players_urls.index(player)) + "/" + str(length), DATASET_LOG_PATH)
        
        time.sleep(2)
    
    sel.stop_server_and_driver(server, driver)

    return

if __name__ == "__main__":
    get_players_data(1)