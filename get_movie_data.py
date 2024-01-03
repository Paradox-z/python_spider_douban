# -*- coding:utf-8 -*-
from ssl import _create_unverified_context
from json import loads
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter.messagebox
import urllib.request
import urllib.parse

moviedata = ' [' \
            '{"title":"Doc", "type":"1", "interval_id":"100:90"}, ' \
            ' {"title":"Bio", "type":"2", "interval_id":"100:90"}, ' \
            ' {"title":"Crim", "type":"3", "interval_id":"100:90"}, ' \
            ' {"title":"His", "type":"4", "interval_id":"100:90"}, ' \
            ' {"title":"Act", "type":"5", "interval_id":"100:90"}, ' \
            ' {"title":"X", "type":"6", "interval_id":"100:90"}, ' \
            ' {"title":"Danc", "type":"7", "interval_id":"100:90"}, ' \
            ' {"title":"Kid", "type":"8", "interval_id":"100:90"}, ' \
            ' {"title":"Mys", "type":"10", "interval_id":"100:90"}, ' \
            ' {"title":"Dra", "type":"11", "interval_id":"100:90"}, ' \
            ' {"title":"Disa", "type":"12", "interval_id":"100:90"}, ' \
            ' {"title":"Rom", "type":"13", "interval_id":"100:90"}, ' \
            ' {"title":"Musi", "type":"14", "interval_id":"100:90"}, ' \
            ' {"title":"Adv", "type":"15", "interval_id":"100:90"}, ' \
            ' {"title":"Fan", "type":"16", "interval_id":"100:90"}, ' \
            ' {"title":"SciF", "type":"17", "interval_id":"100:90"}, ' \
            ' {"title":"Spo", "type":"18", "interval_id":"100:90"}, ' \
            ' {"title":"Thr", "type":"19", "interval_id":"100:90"}, ' \
            ' {"title":"Hor", "type":"20", "interval_id":"100:90"}, ' \
            ' {"title":"War", "type":"22", "interval_id":"100:90"}, ' \
            ' {"title":"Sho", "type":"23", "interval_id":"100:90"}, ' \
            ' {"title":"Com", "type":"24", "interval_id":"100:90"}, ' \
            ' {"title":"Ani", "type":"25", "interval_id":"100:90"}, ' \
            ' {"title":"Homo", "type":"26", "interval_id":"100:90"}, ' \
            ' {"title":"Wes", "type":"27", "interval_id":"100:90"}, ' \
            ' {"title":"Fam", "type":"28", "interval_id":"100:90"}, ' \
            ' {"title":"MA", "type":"29", "interval_id":"100:90"}, ' \
            ' {"title":"Cos", "type":"30", "interval_id":"100:90"}, ' \
            ' {"title":"BlkCom", "type":"31", "interval_id":"100:90"}' \
            ']'

def get_url_data_in_ranking_list(typeId, movie_count, rating, vote_count):
    """
    :param typeId:
    :param movie_count:
    :param rating:
    :param vote_count:
    :return:
    """

    try:
        context = _create_unverified_context()  # SSL blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        url = 'https://movie.douban.com/j/chart/top_list?type=' + str(typeId) + '&interval_id=100:90&action=unwatched&start=0&limit=' + str(movie_count)
        req = urllib.request.Request(url=url, headers=headers)
        f = urllib.request.urlopen(req, context=context)
        response = f.read()
        jsondata = loads(response)  # transform json to Python objects

        res_list = []
        for subdata in jsondata:  # operating on each film in turn
            if (float(subdata['rating'][0]) >= float(rating)) and (float(subdata['vote_count']) >= float(vote_count)):
                sub_list= []
                sub_list.append(subdata['title'])
                sub_list.append(subdata['rating'][0])
                sub_list.append(subdata['rank'])
                sub_list.append(subdata['vote_count'])
                res_list.append(sub_list)

        for data in res_list:
            print(data)

        return [res_list, jsondata]

    except Exception as ex:
        err_str = "Unknown error: {}".format(ex)
        return [err_str]

def get_url_data_in_keyword(key_word):
    """
    :param key_word:
    :return:
    """

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Set as headless mode
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"')  # set user status as agent
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # Set as developer mode
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # avoid loading images temporarily

    load_driver_success = False  # loading chromedriver
    browser = None
    wait = None
    try:
        browser = webdriver.Chrome(executable_path='D:/Program Files (x86)/chromedriver.exe', chrome_options=chrome_options)  # set ChromeDriver loaded path
        browser.set_page_load_timeout(10)  # webpage loading timeout duration sets 10s
        browser.set_script_timeout(10)  # webpage js loading timeout duration sets 10s

        wait = WebDriverWait(browser, 10)  # waiting timeout duration sets 10s
        load_driver_success = True
    except Exception as ex:
        load_driver_success = False
        err_str = "Fail to load chromedriver, download chromedriver again and write the correct path.\n\nError information: {}".format(ex)
        return [err_str]


    # ChromeDriver running well
    if load_driver_success:

        try:
            # browsing papes
            browser.get('https://movie.douban.com/subject_search?search_text=' + urllib.parse.quote(key_word) + '&cat=1002')  # get jason, to capture for returning data
            # js dynamically rendered web pages
            # waiting class=root element in div
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.root')))

            dr = browser.find_elements(by=By.XPATH, value="//div[@class='item-root']") # Cause there are multiple results, get div with class item-root
            jsondata = []
            res_list = []
            for son in dr:
                moviedata = {'rating': ['', 'null'], 'cover_url': '', 'types': '', 'title': '', 'url': '', 'release_date': '', 'vote_count': '', 'actors': ''}
                sub_list = ['', '', '', '']

                url_element = son.find_elements(by=By.XPATH, value=".//a")  # Cause there are multiple results, get the url of the first 'a' tag
                if url_element:
                    moviedata['url'] = (url_element[0].get_attribute("href"))

                img_url_element = url_element[0].find_elements(by=By.XPATH, value=".//img")  # get the film poster image address
                if img_url_element:
                    moviedata['cover_url'] = (img_url_element[0].get_attribute("src"))

                title_element = son.find_elements(by=By.XPATH, value=".//div[@class='title']")  # get title element
                if title_element:
                    temp_title = title_element[0].text
                    moviedata['title'] = (temp_title.split('('))[0]
                    moviedata['release_date'] = temp_title[temp_title.find('(') + 1:temp_title.find(')')]
                    sub_list[0] = moviedata['title']

                rating_element = son.find_elements(by=By.XPATH, value=".//span[@class='rating_nums']")  # get ranking
                if rating_element:
                    moviedata['rating'][0] = rating_element[0].text
                    sub_list[1] = moviedata['rating'][0]

                vote_element = son.find_elements(by=By.XPATH, value=".//span[@class='pl']")  # get amount
                if vote_element:
                    moviedata['vote_count'] = vote_element[0].text.replace('(', '').replace(')', '').replace(' rating quantities', '')
                    sub_list[3] = moviedata['vote_count']

                type_element = son.find_elements(by=By.XPATH, value=".//div[@class='meta abstract']")  # get type element
                if type_element:
                    moviedata['types'] = type_element[0].text
                    sub_list[2] = moviedata['types']

                actors_element = son.find_elements(by=By.XPATH, value=".//div[@class='meta abstract_2']")  # get actor element
                if actors_element:
                    moviedata['actors'] = actors_element[0].text

                jsondata.append(moviedata)
                res_list.append(sub_list)

            for data in res_list:
                print(data)

            browser.quit()
            return [res_list, jsondata]

        except Exception as ex:
            browser.quit()  # browser closed
            err_str = "chromedriver load successfully, whereas unknown error happened: {}".format(ex)
            return [err_str]
