import re
from urllib.parse import urljoin
import time
import requests
from selenium import webdriver

BASE_URL = 'https://www.youtube.com'
SOURCE_URL = 'https://www.youtube.com/playlist?list=PL5PpGecB7x5QAW2jmYtrDKKj0IDytpc2c'
MAXIMUM_TAB = 4
NUMBER_OF_VIDEOS = 0
TIMEOUT_SLEEP = 5
PATH_EDGE_DRIVER = r'path to edge driver'


def get_link():
    r = requests.get(SOURCE_URL)
    if r.ok:
        links = re.findall('/watch.?v=[a-zA-Z0-9_]{11}', str(r.content))
        links = list(dict.fromkeys(links))
        global NUMBER_OF_VIDEOS
        NUMBER_OF_VIDEOS = len(links)
        browser = webdriver.Edge(PATH_EDGE_DRIVER, {})
        browser.get(urljoin(BASE_URL, links[0]))
        index = 0
        index_tab = 0
        while True:
            time.sleep(TIMEOUT_SLEEP)
            index += 1
            index_tab += 1
            if index >= NUMBER_OF_VIDEOS:
                index = 0
            elif index_tab >= 100:
                index_tab = MAXIMUM_TAB
            index = index % NUMBER_OF_VIDEOS
            if index_tab < MAXIMUM_TAB:
                browser.execute_script("window.open(" + "'" + urljoin(BASE_URL, links[index]) + "'" + ")")
            else:
                browser.switch_to.window(browser.window_handles[index_tab % MAXIMUM_TAB])
                browser.get(urljoin(BASE_URL, links[index]))
    else:
        print('Fail')


if __name__ == '__main__':
    get_link()
