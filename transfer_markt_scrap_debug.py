#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program does web scraping of the website www.transfermarkt.com to get a dataset of information
about football soccer players, and then saves this data into a tab-delimited file.

To scrap the website, fill in the constant COUNTRIES with the names of the countries that you want to scrap.
Then, fill in the constant TIERS with the names of the tiers that you want to scrap.
Choose a path to save the tsv.
Finally, run start_scraping to begin the program and get the dataset. 
"""

import requests
import bs4
from collections import OrderedDict
from unidecode import unidecode
from urllib.parse import unquote
import os
from pathlib import Path

"""
Request Headers for the GET Request
"""
REQUEST_HEADERS = {'authority': 'www.transfermarkt.com',
                   'method': 'GET',
                   'scheme': 'https',
                   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'es-ES,es;q=0.8,en;q=0.6,la;q=0.4',
                   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

"""
Countries to scrap
"""
COUNTRIES = ['England',
             'Spain',
             'France',
             'Germany',
             'Italy',
             'China',
             'Japan',
             'United States',
             'Brazil',
             'Russia',
             'Turkey',
             'Netherlands',
             'Switzerland',
             'Belgium',
             'Portugal',
             'Argentina',
             'Austria',
             'Poland',
             'Greece']

#COUNTRIES = ['Afghanistan',
#             'Egypt',
#             'Algeria',
#             'Angola',
#             'Antigua and Barbuda',
#             'Argentina',
#             'Armenia']

"""
Tiers to scrap
"""
TIERS = ['First tier',
         'Second tier']

"""
File paths where the data will be saved.
"""
COUNTRIES_FILE_PATH = "countries_urls"
TIERS_FILE_PATH = "tiers_urls"
TEAMS_FILE_PATH = "teams_urls"
PLAYERS_FILE_PATH = "players_urls"
DATASET_FILE_PATH = "transfermarkt_dataset"

LIST_OF_FILE_PATHS = [COUNTRIES_FILE_PATH,
                      TIERS_FILE_PATH,
                      TEAMS_FILE_PATH,
                      PLAYERS_FILE_PATH,
                      DATASET_FILE_PATH]

"""
Functions to scrap www.transfermarkt.com and save the data into a tab-delimited file.
"""

def save_to_file(dataset, file_path):
    """
    Function to save a list of urls into a txt file
    """
    with open(file_path, 'w') as f:
        for item in dataset:
            f.write(item+'\n')
        f.close()

def append_to_tsv(dataset, file_path):
    """
    Function to append new data into a tsv file
    """
    with open(file_path, 'a') as f:
        for player in dataset:
            f.write('\t'.join(player)+'\n')
        f.close()

def iterate_through_countries(countries, request_headers, file_path):
    """
    Function that returns a list of the urls of each country in the COUNTRIES list.
    """
    general_url = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/{}'
    #Choose a maximum number of countries to scan
    num_of_countries_in_the_world = 200
    len_of_list_of_countries = len(countries)
    
    list_of_countries_urls = []
    
    for ii in range(1, num_of_countries_in_the_world+1):
        #to debug
        print("Country with url number: " + str(ii))
        
        if len(list_of_countries_urls) >= len_of_list_of_countries:
            break
        else:
            try:
                request_obj = requests.get(general_url.format(str(ii)), headers=request_headers, timeout=5)
            except requests.exceptions.ConnectionError as e:
                print("ConnectionError on {}".format(ii))
                print(str(e))
                continue
            except requests.exceptions.Timeout as e:
                print("Timeout error on {}".format(ii))
                print(str(e))
                continue
            except requests.exceptions.RequestException as e:
                print("Request error on {}".format(ii))
                print(str(e))
                continue
            
            parser_obj = bs4.BeautifulSoup(request_obj.text, 'lxml')
            name_of_country = parser_obj.find_all('div', class_='clearer relevante-wettbewerbe-auflistung')
            if name_of_country != None and len(name_of_country) > 0 and \
            name_of_country[0].a.attrs['title'] in countries:
                    list_of_countries_urls.append(general_url.format(str(ii)))
        
    #Contries' urls checkpoint            
    save_to_file(list_of_countries_urls, file_path)

    return list_of_countries_urls
        
#print(iterate_through_countries(COUNTRIES, REQUEST_HEADERS, COUNTRIES_FILE_PATH))
#
five_countries_test = ['https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/1',
                       'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/3',
                       'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/5',
                       'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/7',
                       'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/9',
                       'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/10',
                       'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/236',
                       'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/182']
#
#country_test = ['https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/147']

        
        
def iterate_through_tiers(countries_urls, tiers, request_headers, file_path):
    """
    Function that returns a list of the urls of the first and second tier of each
    country in countries_list.
    """
    
    general_url = 'https://www.transfermarkt.com'
    list_of_tiers_urls = []
    
    for country in countries_urls:
        #to debug
        print("Country with url: " + country)
        
        tiers_found = []
        
        try:
            request_obj = requests.get(country, headers=request_headers, timeout=5)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError on {}".format(country))
            print(str(e))
            continue
        except requests.exceptions.Timeout as e:
            print("Timeout error on {}".format(country))
            print(str(e))
            continue
        except requests.exceptions.RequestException as e:
            print("Request error on {}".format(country))
            print(str(e))
            continue
            
        parser_obj = bs4.BeautifulSoup(request_obj.text, 'lxml')
        hrefs_tiers = parser_obj.find_all('td', class_='hauptlink')
            
        if hrefs_tiers != None:
            for td in hrefs_tiers:
                
                td_text = td.get_text().strip()
                if td.attrs['class'] == ['extrarow', 'bg_blau_20', 'hauptlink'] and \
                td_text not in tiers:
                    break
                if td.attrs['class'] == ['rechts', 'hauptlink']:
                    continue
                if td.attrs['class'] == ['extrarow', 'bg_blau_20', 'hauptlink']:
                    if td_text in tiers_found:
                        break
                    else:
                        tiers_found.append(td_text)
                        continue
                if td.attrs['class'] == ['no-border-links', 'hauptlink']:
                    break
                list_of_tiers_urls.append(general_url+unidecode(unquote(td.find_all('a')[1].attrs['href'])))
                
    save_to_file(list_of_tiers_urls, file_path)
                
    return list_of_tiers_urls
            
        
#print(iterate_through_tiers(five_countries_test, TIERS, REQUEST_HEADERS, TIERS_FILE_PATH))
#        
#tier_test = ['https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1']
tiers_test = ['https://www.transfermarkt.com/kategoria-superiore/startseite/wettbewerb/ALB1',
                              'https://www.transfermarkt.com/primera-division/startseite/wettbewerb/AR1N',
                              'https://www.transfermarkt.com/primera-b-nacional/startseite/wettbewerb/ARG2',
                              'https://www.transfermarkt.com/bardsragujn-chumb/startseite/wettbewerb/ARM1',
                              'https://www.transfermarkt.com/armenian-first-league/startseite/wettbewerb/ARM2']
        
        
def iterate_through_teams(tiers_urls, request_headers, file_path):
    """
    Function that returns a list of the urls of the teams in each of the tiers in TIERS.
    """
    
    general_url = 'https://www.transfermarkt.com'
    list_of_teams_urls = []
    
    for tier in tiers_urls:
        #to debug
        print("Tier with url: " + tier)
        
        try:
            request_obj = requests.get(tier, headers=request_headers, timeout=5)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError on {}".format(tier))
            print(str(e))
            continue
        except requests.exceptions.Timeout as e:
            print("Timeout error on {}".format(tier))
            print(str(e))
            continue
        except requests.exceptions.RequestException as e:
            print("Request error on {}".format(tier))
            print(str(e))
            continue
        
        parser_obj = bs4.BeautifulSoup(request_obj.text, 'lxml')
        teams_table = parser_obj.find_all('div', class_='responsive-table')
        
        if teams_table != None:
            teams_trs = teams_table[0].find_all('tr', class_=['even', 'odd'])
            
        if teams_trs != None:
            for team in teams_trs:
                team_as = team.find_all('a')
                
                if team_as != None:
                    team_name = team_as[1].attrs['href']
                    list_of_teams_urls.append(general_url + unidecode(unquote(team_name)))
                    
    save_to_file(list_of_teams_urls, file_path)
    
    return list_of_teams_urls
            
#print(iterate_through_teams(tiers_test, REQUEST_HEADERS, TEAMS_FILE_PATH))

#for team in team_dataset_test:
#    print(team.endswith('2017'))
#        
argentina_teams_test = ['https://www.transfermarkt.com/club-atletico-river-plate/startseite/verein/209/saison_id/2017',
                        'https://www.transfermarkt.com/club-atletico-boca-juniors/startseite/verein/189/saison_id/2017',
                        'https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/startseite/verein/1775/saison_id/2017',
                        'https://www.transfermarkt.com/racing-club-de-avellaneda/startseite/verein/1444/saison_id/2017',
                        'https://www.transfermarkt.com/ca-independiente-de-avellaneda/startseite/verein/1234/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-lanus/startseite/verein/333/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-rosario-central/startseite/verein/1418/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-huracan/startseite/verein/2063/saison_id/2017', 'https://www.transfermarkt.com/estudiantes-de-la-plata/startseite/verein/288/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-velez-sarsfield/startseite/verein/1029/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-colon-santa-fe-/startseite/verein/1070/saison_id/2017', 'https://www.transfermarkt.com/defensa-y-justicia/startseite/verein/2402/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-talleres/startseite/verein/3938/saison_id/2017', 'https://www.transfermarkt.com/belgrano-de-cordoba/startseite/verein/2417/saison_id/2017', 'https://www.transfermarkt.com/ca-union-santa-fe/startseite/verein/7097/saison_id/2017', 'https://www.transfermarkt.com/club-de-gimnasia-y-esgrima-la-plata/startseite/verein/1106/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-newells-old-boys/startseite/verein/1286/saison_id/2017', 'https://www.transfermarkt.com/club-deportivo-godoy-cruz/startseite/verein/12574/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-tucuman/startseite/verein/14554/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-san-martin-sj-/startseite/verein/10511/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-tigre/startseite/verein/11831/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-banfield/startseite/verein/830/saison_id/2017', 'https://www.transfermarkt.com/argentinos-juniors/startseite/verein/1030/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-patronato/startseite/verein/19806/saison_id/2017', 'https://www.transfermarkt.com/arsenal-de-sarandi-fc/startseite/verein/4673/saison_id/2017', 'https://www.transfermarkt.com/olimpo-de-bahia-blanca/startseite/verein/7468/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-temperley/startseite/verein/14542/saison_id/2017', 'https://www.transfermarkt.com/club-atletico-chacarita-juniors/startseite/verein/2154/saison_id/2017']
#
#team_test = ['https://www.transfermarkt.com/club-atletico-san-lorenzo-de-almagro/startseite/verein/1775/saison_id/2017']
#   
def iterate_through_players(teams_urls, request_headers, file_path):
    """
    Function that returns a list of urls of players for each team in team_urls.
    """
    
    general_url = 'https://www.transfermarkt.com'
    list_of_players_urls = []
    
    for team in teams_urls:
        #to debug
        print("Team with url: " + team)

        try:
            request_obj = requests.get(team, headers=request_headers, timeout=5)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError on {}".format(team))
            print(str(e))
            continue
        except requests.exceptions.Timeout as e:
            print("Timeout error on {}".format(team))
            print(str(e))
            continue
        except requests.exceptions.RequestException as e:
            print("Request error on {}".format(team))
            print(str(e))
            continue
        
        parser_obj = bs4.BeautifulSoup(request_obj.text, 'lxml')
        players_table = parser_obj.find_all('div', class_='responsive-table')
        
        if players_table != None:
            players_trs = players_table[0].find_all('tr', class_=['even', 'odd'])
            
        if players_trs != None:
            for player in players_trs:
                player_as = player.find_all('a')
                if len(player_as) < 4:
                    player_url = player_as[1].attrs['href']
                    list_of_players_urls.append(general_url + unidecode(unquote(player_url)))
                elif len(player_as) == 4:
                    player_url = player_as[2].attrs['href']
                    list_of_players_urls.append(general_url + unidecode(unquote(player_url)))
                else:
                    player_url = player_as[3].attrs['href']
                    list_of_players_urls.append(general_url + unidecode(unquote(player_url)))
                    
    save_to_file(list_of_players_urls, file_path)
            
    return list_of_players_urls
            
        
#print(iterate_through_players(argentina_teams_test, REQUEST_HEADERS, PLAYERS_FILE_PATH))    

players_list_test = ['https://www.transfermarkt.com/sebastian-torrico/profil/spieler/68040', 'https://www.transfermarkt.com/nicolas-navarro/profil/spieler/26727', 'https://www.transfermarkt.com/jose-devecchi/profil/spieler/282684', 'https://www.transfermarkt.com/gonzalo-rodriguez/profil/spieler/19998', 'https://www.transfermarkt.com/fabricio-coloccini/profil/spieler/6150', 'https://www.transfermarkt.com/matias-caruzzo/profil/spieler/56573', 'https://www.transfermarkt.com/marcos-angeleri/profil/spieler/27448', 'https://www.transfermarkt.com/marcos-senesi/profil/spieler/469781', 'https://www.transfermarkt.com/nicolas-zalazar/profil/spieler/471640', 'https://www.transfermarkt.com/gabriel-rojas/profil/spieler/471639', 'https://www.transfermarkt.com/victor-salazar/profil/spieler/347749', 'https://www.transfermarkt.com/paulo-diaz/profil/spieler/271478', 'https://www.transfermarkt.com/cristian-barrios/profil/spieler/503377', 'https://www.transfermarkt.com/robert-piris/profil/spieler/273033', 'https://www.transfermarkt.com/nicolas-bertocchi/profil/spieler/146289', 'https://www.transfermarkt.com/juan-mercier/profil/spieler/54854', 'https://www.transfermarkt.com/franco-mussis/profil/spieler/74821', 'https://www.transfermarkt.com/fernando-belluschi/profil/spieler/26460', 'https://www.transfermarkt.com/alexis-castro/profil/spieler/364602', 'https://www.transfermarkt.com/facundo-quignon/profil/spieler/131218', 'https://www.transfermarkt.com/leandro-navarro/profil/spieler/208663', 'https://www.transfermarkt.com/gabriel-gudino/profil/spieler/458169', 'https://www.transfermarkt.com/bautista-merlini/profil/spieler/431737', 'https://www.transfermarkt.com/juan-cavallaro/profil/spieler/221037', 'https://www.transfermarkt.com/ruben-botta/profil/spieler/88542', 'https://www.transfermarkt.com/fernando-elizari/profil/spieler/223024', 'https://www.transfermarkt.com/leandro-romagnoli/profil/spieler/15694', 'https://www.transfermarkt.com/ezequiel-cerutti/profil/spieler/267882', 'https://www.transfermarkt.com/tomas-conechny/profil/spieler/401571', 'https://www.transfermarkt.com/nicolas-blandi/profil/spieler/153022', 'https://www.transfermarkt.com/mauro-matos/profil/spieler/80241', 'https://www.transfermarkt.com/nicolas-reniero/profil/spieler/496415']
#
#player_test = ['https://www.transfermarkt.com/lionel-messi/profil/spieler/28003']


def get_players_data(players_urls, request_headers, file_path, restart_from_beginning=True):
    """
    Get the required information about each of the players in players_urls.
    """
    
    search_for_file = Path("./" + file_path)
    if search_for_file.exists() and restart_from_beginning:
        os.remove(file_path)
    
    data_to_search = ['Name', 'Date of birth', 'Place of birth', 'Age', 'Height', 'Shoe size',
                    'Nationality', 'Position', 'Foot', 'Current club', 'Current market value',
                    'Highest market value']
    players_data = []
    players_data.append(data_to_search)
    counter_for_checkpoint = 1
    
    for player in players_urls:
        #to debug
        print("Player with url: " + player)
        
        defaults = OrderedDict({'Name':"Undefined", 'Date of birth':"Undefined", 'Place of birth':"Undefined",
                                'Age':"Undefined", 'Height':"Undefined", 'Shoe size':"Undefined",
                                'Nationality':"Undefined", 'Position':"Undefined", 'Foot':"Undefined", 
                                'Current club':"Undefined", 'Current market value':"Undefined", 
                                'Highest market value':"Undefined"})
    
        try:
            request_obj = requests.get(player, headers=request_headers, timeout=5)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError on {}".format(player))
            print(str(e))
            continue
        except requests.exceptions.Timeout as e:
            print("Timeout error on {}".format(player))
            print(str(e))
            continue
        except requests.exceptions.RequestException as e:
            print("Request error on {}".format(player))
            print(str(e))
            continue
        
        parser_obj = bs4.BeautifulSoup(request_obj.text, 'lxml')
        
        #Get the first object
        player_name_h1 = parser_obj.find('div', class_='dataName')
        if player_name_h1 != None:
            defaults['Name'] = unidecode(unquote(player_name_h1.h1.get_text().strip()))
        
        #Get objects 2 to 9
        player_table = parser_obj.find('div', class_='spielerdaten')
        if player_table != None:
            table_body = player_table.find_all('tr')
    
            if table_body != None:
                for info in table_body:
                    info_name = info.find('th').string.strip().strip(':')
                    if info_name == data_to_search[1]:
                        defaults[info_name] = unidecode(unquote(info.find('td').a.string))
                    elif info_name == data_to_search[2]:
                        if info.find('td').img != None:
                            defaults[info_name] = unidecode(unquote(info.find('td').span.get_text().strip('\xa0')+', '+info.find('td').img.get('title')))
                        else:
                            defaults[info_name] = unidecode(unquote(info.find('td').span.get_text().strip('\xa0')))
                    elif info_name in [data_to_search[3], data_to_search[4], data_to_search[5], data_to_search[7], data_to_search[8]]:
                        defaults[info_name] = unidecode(unquote(info.find('td').string.strip().strip('\r').strip('\n').strip('\t').replace('\xa0', ' ')))
                    elif info_name == data_to_search[6]:
                        national_images = info.find('td').find_all('img')
                        if len(national_images) < 2:
                            defaults[info_name] = unidecode(unquote(national_images[0].get('title')))
                        else:
                            defaults[info_name] = unidecode(unquote(national_images[0].get('title')))+\
                            ', '+unidecode(unquote(national_images[1].get('title')))
                    elif info_name == data_to_search[9]:
                        defaults[info_name] = unidecode(unquote(info.find('td').find_all('a')[1].get_text()))
                
        #Get the last 2 objects
        player_value = parser_obj.find('div', class_='marktwertentwicklung')
        if player_value != None:
            current_value = player_value.find(class_='zeile-oben')
            if current_value != None:
                defaults['Current market value'] = unidecode(unquote(current_value.find(class_='right-td').string.strip('\r').strip('\n').strip('\t')))
            highest_value = player_value.find(class_='zeile-unten')
            if highest_value != None:
                value_strings = highest_value.find(class_='right-td')
                value_strings.span.clear()
                defaults['Highest market value'] = unidecode(unquote(value_strings.get_text().strip('\r').strip('\n').strip('\t')))
            
        #Append data to list of players    
        player_data = [value for key, value in defaults.items()]
        players_data.append(player_data)
        
        if counter_for_checkpoint % 5 == 0:
            append_to_tsv(players_data, file_path)
            players_data = []
            
        counter_for_checkpoint += 1
        
    append_to_tsv(players_data, file_path)
        
    print("Scraping finished!")

#dataset_test = get_players_data(players_list_test, REQUEST_HEADERS, DATASET_FILE_PATH)


def start_scraping(request_headers, countries, tiers, file_paths):
    countries_urls = iterate_through_countries(countries, request_headers, file_paths[0])
    tiers_urls = iterate_through_tiers(countries_urls, tiers, request_headers, file_paths[1])
    teams_urls = iterate_through_teams(tiers_urls, request_headers, file_paths[2])
    players_urls = iterate_through_players(teams_urls, request_headers, file_paths[3])
    get_players_data(players_urls, request_headers, file_paths[4])
    
#Uncomment to start scraping
#start_scraping(REQUEST_HEADERS, COUNTRIES, TIERS, LIST_OF_FILE_PATHS)












        
        
        
        
        














        
    
