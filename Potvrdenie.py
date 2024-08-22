#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 20:47:41 2023

@author: priwi
"""

from selenium.webdriver.common.by import By

def find_button_by_row_text(table_body, desired_text):
    rows = table_body.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')

        found_text = False
        for index, cell in enumerate(cells):
            # Preskočíme porovnanie pre stĺpec 0 a stĺpec 8
            if index == 0 or index == 8:
                continue
            
            if desired_text[index-1] in cell.text:
                found_text = True
                break

        if found_text:
            button = row.find_element(By.TAG_NAME, 'button')
            button_class = button.get_attribute('class')
            #print("Porovnávaný riadok:", [cell.text for cell in cells])
            #print("Nájdený riadok:", [cell.text for cell in cells])
            #print(button_class)
            return button, button_class

    print("Riadok s hľadaným textom sa nenašiel.")
    return None, None