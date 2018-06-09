#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 15:47:27 2018

@author: joseramon
"""

from unidecode import unidecode
from urllib import unquote

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

def save_to_file(dataset, file_path):
    """
    Function to save a list of urls into a txt file
    """
    with open(file_path, 'w') as f:
        for item in dataset:
            f.write(item+'\n')
        f.close()
        
def populate_countries_dict(file_path):
    """
    Function to populate dictionary of countries and url numbers.
    """
    
    countries_dict = {}
    
    with open(file_path, 'r') as f:
        for line in f.readlines():
            key_value = line[:-1].split(':')
            countries_dict[key_value[0]] = int(key_value[1])
        
    return countries_dict

def read_from_file(file_path):
    
    file_in_list = []
    
    with open(file_path, 'r') as f:
        for line in f.readlines():
            file_in_list.append(line)
            
    return file_in_list

def append_to_tsv(player, file_path):
    """
    Function to append new data into a tsv file
    """
    with open(file_path, 'a') as f:
        f.write('\t'.join(player)+'\n')
            
def append_to_csv(player, file_path):
    """
    Function to append new data into a tsv file
    """
    with open(file_path, 'a') as f:
        f.write(','.join(player)+'\n')
        
def append_to_file(line, file_path):
    """
    Function to append new data into a tsv file
    """
    with open(file_path, 'a') as f:
        f.write(line+'\n')

def process_info(info):
    try:
        processed = unquote(info)
    except:
        processed = info
        pass
    if isinstance(processed, unicode):
        processed = unidecode(processed)
        
    return processed

