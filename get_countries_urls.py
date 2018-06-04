#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 15:36:19 2018

@author: joseramon
"""

from helper_functions import save_to_file, populate_countries_dict

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

"""
File paths where the data will be saved.
"""

COUNTRIES_DICT_FILE_PATH = "countries_dict.txt"
COUNTRIES_FILE_PATH = "countries_urls.txt"


def iterate_through_countries(countries):
    """
    Function that returns a list of the urls of each country in the COUNTRIES list.
    """

    general_url = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/{}'
    list_of_countries_urls = []
    
    dict_of_countries = populate_countries_dict(COUNTRIES_DICT_FILE_PATH)
    
    if countries == "ALL":
        for key, value in dict_of_countries.items():
            list_of_countries_urls.append(general_url.format(value))
    else:
        for country in countries:
            list_of_countries_urls.append(general_url.format(dict_of_countries[country]))
            
    save_to_file(list_of_countries_urls, COUNTRIES_FILE_PATH)
    
    return list_of_countries_urls

if __name__ == "__main__":
    
    iterate_through_countries("ALL")
