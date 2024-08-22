from datetime import datetime, timedelta

def analyze_and_update_schedule(schedule_time_on):
    def count_occurrences_in_column(filename, column_index, keyword, start_date, end_date):
        count = 0
        total_lines_in_range = 0
        total_lines_with_keyword = 0
    
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if "Cena pod garantovanou úrovní!!" in line:
                    # Pokud řádek obsahuje "Cena pod garantovanou úrovní!!", ignoruj ho a přeskoči ho
                    continue
    
                total_lines_in_range += 1
                columns = line.strip().split(';')
                if len(columns) <= column_index:
                    continue
    
                # Získání data z daného řádku ve sloupci A (pokud je správně formátováno)
                try:
                    date_obj = datetime.strptime(columns[0].strip(), '%d.%m.%Y')
    
                    # Pokud datum je v daném období, zvýšit počet řádků s hledaným slovem
                    if start_date <= date_obj <= end_date:
                        total_lines_with_keyword += 1
                        # Porovnání slov bez diakritiky
                        if columns[column_index].strip().lower() == keyword.lower():
                            count += 1
    
                except ValueError:
                    # Ignoruj řádek, pokud datum nelze správně přečíst
                    pass
    
        return count, total_lines_with_keyword

    # Nastavte cestu k souboru 'Kniha_objednavok.txt'
    file_path = 'Kniha_objednavok.txt'

    # Sloupec I má index 8 (počítáme od nuly)
    column_index = 8

    # Hledané slovo
    search_word = 'Prijate'

    # Získání aktuálního data
    current_date = datetime.now()

    # Výpočet počátečního a koncového data aktuálního týdne
    current_weekday = current_date.weekday()
    start_date = current_date - timedelta(days=current_weekday)  # Pondělí aktuálního týdne
    end_date = start_date + timedelta(days=6)  # Neděle aktuálního týdne

    # Získání počtu výskytů slova 'Prijate' a celkového počtu řádků v daném časovém rozmezí
    occurrences, total_lines_in_range = count_occurrences_in_column(file_path, column_index, search_word, start_date, end_date)
    print(total_lines_in_range )
    # Výpočet procentuálního výskytu, pokud total_lines_in_range není nulový
    if total_lines_in_range > 0:
        percent_value = (occurrences / total_lines_in_range) * 100
    else:
        percent_value = 0

    # Ak percent_value je menší alebo rovný 0, nastavíme schedule_time_on na 0
    if percent_value <= 0:
        schedule_time_on = 0

    # Výpis výsledků
    print("Období: {} - {}".format(start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y')))
    print("Počet výskytů slova '{}': {}".format(search_word, occurrences))
    print("Celkový počet řádků v daném časovém rozmezí: {}".format(total_lines_in_range))
    print("Percentuální výskyt slova '{}' v daném období: {:.2f}%".format(search_word, percent_value))
    print("schedule_time_on =", schedule_time_on)

    # Vytvoření proměnné s hodnotou procentuálního výskytu
    percentage_value = round(percent_value, 2)

    return percentage_value, schedule_time_on

# Zavolání funkce pro analýzu a aktualizaci
percent_value, schedule_time_on = analyze_and_update_schedule(1)

print("Hodnota procentuálního výskytu v daném období:", percent_value)
print("Hodnota proměnné schedule_time_on po analýze:", schedule_time_on)
