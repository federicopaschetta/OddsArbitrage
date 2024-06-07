import pandas as pd # DataFrame management
from selenium import webdriver # WebScraping driver
from selenium.webdriver.common.by import By # WebScraping property library
import time # Sleep library

def get_sports_draw_info(filepath: str) -> dict:
    draws_dict = {}
    with open(filepath, 'r') as draw_file:
        for line in draw_file:
            line = line.strip().split(',')
            draws_dict[line[0]] = line[1]=='T'
    return draws_dict

def get_and_accept_cookies(driver, url: str) -> None:
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    
def get_sports_buttons(driver) -> list:
    buttons_list = driver.find_elements(By.CSS_SELECTOR, '.flex.flex-col.w-full.h-auto')
    if len(buttons_list)==0:
        buttons_list = driver.find_elements(By.CSS_SELECTOR, '.text-white-main.flex.h-full.items-center a')
    return buttons_list

def fill_sports_links_dict(sports_links_dict: dict, buttons_list: list) -> dict:
    for button in buttons_list:
            href = button.get_attribute('href')
            sport = button.find_elements(By.CSS_SELECTOR, 'div')[1].text
            if len(sport)==0:
                sport = href.split('/')[-2]
            sports_links_dict[sport.capitalize()] = href
    return sports_links_dict

def fill_main_dict_comps_and_cats(driver, main_dict: dict, sports_links_dict: dict) -> dict:
    for sport in sports_links_dict.keys():
        comps_links_dict = {}
        list_cat = []
        driver.get(sports_links_dict[sport])
        time.sleep(0.5)
        list_categories = driver.find_elements(By.CSS_SELECTOR, '.flex.items-center.w-full.h-10.gap-1.bg-gray-med_light span')
        for elem in list_categories:
            list_cat.append(elem.text)
        list_competitions = driver.find_elements(By.CSS_SELECTOR, 'main .flex.flex-col .flex ul')
        list_comp = []
        for comp in list_competitions:
            single_comp = []
            single = comp.find_elements(By.CSS_SELECTOR, 'li a')
            for elem in single:
                name = ' '.join(elem.text.split(' ')[:-1])
                single_comp.append({name: elem.get_attribute('href')})
            list_comp.append(single_comp)

        for i, j in zip(list_cat, list_comp):
            comps_links_dict[i] = j
        main_dict[sport] = comps_links_dict
    return main_dict

def compute_arbitrage(win1: float, win2: float, draw=None) -> bool:
    if draw is None:
        res = 1/win1+1/win2
    else:
        res = 1/win1+1/win2+1/draw
    return res <1

def get_links_list(driver, sports_links_dict: dict, main_dict: dict):
        links_dict = {}
        for sport in sports_links_dict.keys():
                links_list = []
                for entry in main_dict[sport].keys():
                        entry_list = main_dict[sport][entry]
                        for elem in entry_list:
                                try:
                                        driver.get(elem[list(elem.keys())[0]])
                                        time.sleep(0.5)
                                        all_events = driver.find_elements(By.CSS_SELECTOR, '.group.flex')
                                        all_events.pop(0)
                                except:
                                        print('Ex', elem[list(elem.keys())[0]])
                                        continue
                                try:
                                        for elem in all_events:
                                                div = elem.find_elements(By.CSS_SELECTOR, 'p')
                                                if div[-1].text != '-':
                                                                link_event = elem.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                                                                teams = elem.find_elements(By.CSS_SELECTOR, '.participant-name.truncate')
                                                                links_list.append([link_event, [teams[0].text, teams[1].text]])
                                except:
                                        print('Ex', elem[list(elem.keys())[0]])
                                        continue
                links_dict[sport] = links_list
        return links_dict
                                
                                
def get_arbitrage_matches(driver, game_links_dict, dict_draws):
    arbitrage_list = []
    for link in game_links_dict.keys():
        for game_link in game_links_dict[link]:
            driver.get(game_link[0])
            time.sleep(0.5)
            try:
                highest_cont = driver.find_elements(By.CSS_SELECTOR, 'div.border-black-borders.bg-gray-light.flex.h-9.border-b.border-l.border-r.text-xs')
                p_cont = highest_cont[1].find_elements(By.CSS_SELECTOR, 'p')[1:]
                highest1 = p_cont[0].text
                highest2 = p_cont[-2].text
                if dict_draws[link]:
                    highdraw = p_cont[1].text
                    arbitrage_available = compute_arbitrage(float(highest1), float(highest2), draw=float(highdraw))
                else:
                    arbitrage_available = compute_arbitrage(float(highest1), float(highest2))
                    
                if arbitrage_available:
                    print(link)
                    match_dict = {}
                    time_list = driver.find_elements(By.CSS_SELECTOR, '.flex.flex-col> div> div> p')[:3] # Time and day
                    time_list = [elem.text for elem in time_list]
                    match_dict['Day&Time'] = ' '.join(time_list)
                    match_dict['Participant1'] = link[1][0]
                    match_dict['Participant2'] = link[1][1]
                    container = driver.find_elements(By.CSS_SELECTOR, 'div[data-v-3eae8d94].flex.flex-col > div[data-v-21fd171a]')
                    container.pop(0)
                    for card in container:
                        bm = card.find_element(By.CSS_SELECTOR, 'p[data-v-155f876a]')
                        quotas = card.find_elements(By.CSS_SELECTOR, 'a[data-v-21fd171a]')
                        if len(quotas) == 0:
                            quotas = card.find_elements(By.CSS_SELECTOR, 'p[data-v-21fd171a]')
                        for q in quotas:
                            if q.text == highest1:
                                match_dict['1'] = f'{bm.text}, {q.text}'
                            elif q.text == highest2:
                                match_dict['2'] = f'{bm.text}, {q.text}'
                            elif dict_draws[link] and q.text == highdraw:
                                match_dict['X'] = f'{bm.text}, {q.text}'
                    arbitrage_list.append(match_dict)
            except Exception as ex:
                print('Ex', ex)
                continue
        return arbitrage_list

def main():
    arbitrage_list = []
    dict_draws = get_sports_draw_info('draws.txt')
    base_url = 'https://www.oddsportal.com/it/'
    driver = webdriver.Firefox()
    get_and_accept_cookies(driver, base_url)
    buttons_list = get_sports_buttons(driver)
    sports_links_dict = fill_sports_links_dict({}, buttons_list)
    main_dict = fill_main_dict_comps_and_cats(driver, {}, sports_links_dict)
    game_links_dict = get_links_list(driver, sports_links_dict, main_dict)
    arbitrage_list = get_arbitrage_matches(driver, game_links_dict, dict_draws)
    print(arbitrage_list)

main()