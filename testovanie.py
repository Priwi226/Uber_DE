#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 15:34:59 2023

@author: zakazky
"""

def show_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            print(line.strip())

# Nastavte cestu k souboru 'Kniha_objednavok.txt'
file_path = 'Kniha_objednavok.txt'

# Zobrazit obsah souboru
show_file_content(file_path)
