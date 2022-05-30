#!/bin/python3

LOGIN_URL = u"https://www.strava.com/login"
SESSION_URL = u"https://www.strava.com/session"


LOGIN = ""
PASSWORD = ""

from os import link
import time
from selenium import webdriver
import urllib.parse
from bs4 import BeautifulSoup
import glob


def download_list_of_athletes(_email, _password, _club_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.add_argument("--lang=ru")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.binary_location = "/usr/bin/chromium-browser"
    driver = webdriver.Chrome(chrome_options=options)

    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 2048)

    driver.get('https://strava.com/login')

    email = driver.find_element_by_id("email")
    email.send_keys(_email)

    password = driver.find_element_by_id("password")
    password.send_keys(_password)

    driver.find_element_by_id("login-button").click()

    print("sleep for 5 seconds...")
    time.sleep(5)

    for page in range(12):
        members_url = "https://www.strava.com/clubs/{}/members?page={}".format(_club_id, page)
        print(members_url)
        driver.get(members_url)
        with open('page{}.html'.format(page), 'w') as f:
            f.write(driver.page_source)

    driver.close()


def parse_page_with_athletes(page_number):
    ret = set()
    html_filename = 'page' + str(page_number) + '.html'
    html_doc = open(html_filename, 'r').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    list_athletes = soup.find_all('ul', class_='list-athletes')

    if len(list_athletes) != 2:
        return ret

    # members = list_athletes[1]
    members = list_athletes[0]
    links = members.find_all('a')
    for l in links:
        ret.add(l.get('href'))

    return ret

def download_athletes(_email, _password, athletes):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.add_argument("--lang=ru")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.binary_location = "/usr/bin/chromium-browser"
    driver = webdriver.Chrome(chrome_options=options)

    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 2048)

    driver.get('https://strava.com/login')

    email = driver.find_element_by_id("email")
    email.send_keys(_email)

    password = driver.find_element_by_id("password")
    password.send_keys(_password)

    driver.find_element_by_id("login-button").click()

    print("sleep for 3 seconds...")
    time.sleep(3)

    for athlete_id in athletes:
        # downloaded = glob.glob("athlete*.html")
        # downloaded = [x.split('_')[-1] for x in downloaded]
        # downloaded = [x.split('.')[0] for x in downloaded]
        # ath_id = athlete_id.split('/')[2]
        # if ath_id in downloaded:
        #     print('skip', ath_id)
        #     continue
        url = "https://strava.com" + athlete_id
        athlete_id = athlete_id.replace('/', '_')
        fname = 'athlete{}.html'.format(athlete_id)
        print('downloading', url, 'to', fname)
        driver.get(url)
        time.sleep(3)
        with open(fname, 'w') as f:
            f.write(driver.page_source)

        print("sleep for x seconds...")
        time.sleep(1)

    driver.close()

failed_by_cycling = []
failed_by_name = []

def get_distance_for_athlete(athlete_html_fname):
    html_doc = open(athlete_html_fname, 'r').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    athlete_name = soup.find_all('h1', class_='text-title1 athlete-name')
    if len(athlete_name) == 0:
        print('failed to find name', athlete_html_fname)
        failed_by_name.append(athlete_html_fname)
        return
    athlete_name = athlete_name[0].get_text()
    cycling_shit = soup.find_all(id='cycling-ytd')
    if len(cycling_shit) == 0:
        print('failed to find cycling shit', athlete_html_fname)
        failed_by_cycling.append(athlete_html_fname)
        return
    cycling_shit = cycling_shit[0]
    # print(cycling_shit)
    distance = str(cycling_shit.find_all('td')[1])
    distance = distance[4:-7]
    distance = distance.replace(',','')
    distance = distance.replace('.',',')
    # distance = float(distance)

    strava_link = athlete_html_fname.split('_')[2]
    strava_link = strava_link.split('.')[0]
    strava_link = 'https://strava.com/athletes/' + strava_link
    print(athlete_name, ';', distance, ';', strava_link)
    open('result.csv', 'a').write('{};{};{}\n'.format(athlete_name, distance, strava_link))

if __name__ == "__main__":

    email = LOGIN
    password = PASSWORD
    club_id = 182569

    # members = set()
    # for i in range(12):
    #     x = parse_page_with_athletes(i)
    #     members.update(x)

    # print(len(members))
    # print(members)
    # download_athletes(email, password, members)

    # to_download = ['athlete_athletes_31235500.html', 'athlete_athletes_51358699.html', 'athlete_athletes_2157706.html', 'athlete_athletes_15174612.html', 'athlete_athletes_15961837.html', 'athlete_athletes_37624277.html', 'athlete_athletes_17764175.html', 'athlete_athletes_41995975.html', 'athlete_athletes_17410865.html', 'athlete_athletes_15218619.html', 'athlete_athletes_26999688.html', 'athlete_athletes_6107250.html', 'athlete_athletes_21638295.html', 'athlete_athletes_35876957.html', 'athlete_athletes_95709986.html', 'athlete_athletes_22965802.html', 'athlete_athletes_39637967.html', 'athlete_athletes_17713955.html', 'athlete_athletes_14231954.html', 'athlete_athletes_9531480.html', 'athlete_athletes_41162732.html', 'athlete_athletes_42389444.html', 'athlete_athletes_30131581.html', 'athlete_athletes_18952564.html', 'athlete_athletes_27469601.html', 'athlete_athletes_9768786.html', 'athlete_athletes_42483535.html', 'athlete_athletes_42095731.html', 'athlete_athletes_50593985.html', 'athlete_athletes_22368322.html']
    # to_download = [x.split('_')[2] for x in to_download]
    # to_download = [x.split('.')[0] for x in to_download]
    # to_download = ['/athletes/' + x for x in to_download]
    # download_athletes(email, password, to_download)

    all_athletes = glob.glob("athlete*.html")
    print(len(all_athletes))
    for a in all_athletes:
        get_distance_for_athlete(a)

    print ('cycling:', failed_by_cycling, len(failed_by_cycling))
    print ('name:', failed_by_name, len(failed_by_name))