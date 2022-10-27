from ast import Break
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from time import sleep
from database import Database
import csv

Database.connectDb()
Database.createTable()

arguments = sys.argv[1:]
print(arguments)
try:
    for arg in arguments:
        if 'nb_page=' in arg :
            nb_anime = arg.split('=')[-1]
        if 'tags=' in arg:
            tags = arg.split('=')[-1]
except:
    nb_anime = 50
    tags = 'popular'

driver = webdriver.Chrome('./chromedriver.exe')
driver.get("https://www.crunchyroll.com/fr/videos/popular")
sleep(5)
driver.find_element(By.ID, "_evidon-decline-button").click()

nb_anime = 36
def scroll_down(nb_scroll) :
    for i in range(nb_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('scrollDown: ', i)
        sleep(3)

def infos_anime(start, nb_anime, max_anime, page) :
    data = {}
    for i in range(start, nb_anime):
        if (i == max_anime) : break
        scroll_down(page)
        animes = driver.find_elements(By.CLASS_NAME, "browse-card")
        animes[i].find_element(By.TAG_NAME, "a").click()
        sleep(1)

        item = {}
        try:
            item['image'] = driver.find_element(
                By.CLASS_NAME, "blurred-wrapper").find_element(By.TAG_NAME, 'img').get_attribute('src')
        except:
            item['image'] = None

        # Recupere tous le champ d'information
        infos = driver.find_element(By.CLASS_NAME, "erc-series-hero")
        try:
            item['name'] = infos.find_element(By.CLASS_NAME, "title").text
        except:
            item['name'] = None
        rating = [rate.text for rate in infos.find_element(
            By.CLASS_NAME, "erc-ratings").find_elements(By.TAG_NAME, "span")]
        for rate in rating:
            if ('avis' in rate):
                try:
                    item['nb_avis'] = int(rate.split(' ')[0])
                except:
                    item['nb_avis'] = 0
            elif (' (' in rate):
                r = rate.split(' (')
                try:
                    item['note'] = float(r[0])
                except:
                    item['note'] = 0
                r = r[-1].split(')')[0]
                try:
                    if 'K' in r:
                        item['nb_votant'] = int(float(r.split('K')[0])*1000)
                    else:
                        item['nb_votant'] = int(r)
                except:
                    item['nb_votant'] = 0
        try:
            item['description'] = infos.find_element(
                By.CLASS_NAME, 'erc-show-description').find_element(By.TAG_NAME, 'p').text
        except:
            item['description'] = None

        try:
            item['production'] = infos.find_element(
                By.CLASS_NAME, "show-details-table").find_elements(By.TAG_NAME, 'h5')[-1].text
        except:
            item['production'] = None

        try:
            item['tags'] = ','.join([n.text for n in infos.find_element(
                By.CLASS_NAME, "genres-wrapper").find_elements(By.TAG_NAME, 'a')])
        except:
            item['tags'] = None

        Database.addRow(item)
        driver.back()
        sleep(2)
        data[item['name']] = item
    return data


def get_infos_page(nb_anime):
    max_page = 36
    data = {}
    for page in range(round(nb_anime/max_page)+1):
        print(page)
        data[page] = infos_anime(page*36, (page+1)*36, nb_anime, page)
    sleep(10)
    return data

data = get_infos_page(nb_anime)

print(data)
driver.close()