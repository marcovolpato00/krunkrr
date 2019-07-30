"""                    
     _                 _           
    | |___ _ _  _ _ _ | |___ _ _ _ 
    | / / '_| || | ' \| / / '_| '_|
    |_\_\_|  \_,_|_||_|_\_\_| |_|  
                                
    Marco Volpato 2019

"""

import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from loguru import logger

from localstorage import LocalStorage


DIR_PATH = os.path.dirname(os.path.abspath(__file__))

BASE_URL = 'https://krunker.io'
CHROMEDRIVER_PATH = 'chromedriver'
LOCALSTORAGE_FILE = os.path.join(DIR_PATH, 'localstorage.json')
LOGS_FILE = os.path.join(DIR_PATH, 'krunkrr.log')
LOG_LEVEL = 'INFO'


def load_localstorage_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def set_localstorage(driver_localstorage, localstorage, clear=False):
    if clear:
        driver_localstorage.clear()
    for key in localstorage:
        driver_localstorage.set(key, localstorage.get(key))


def get_page(driver):
    driver.get(BASE_URL)
    driver.execute_script( \
        'let el = document.getElementById("gameUI");' \
        'el.parentNode.removeChild(el);')
    driver.execute_script( \
        'let el = document.getElementById("menuClassContainer");' \
        'el.parentNode.removeChild(el);')



if __name__ == '__main__':
    logger.add(LOGS_FILE, format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}', level=LOG_LEVEL)
    logger.info('Starting')

    logger.debug('Loading {}'.format(LOCALSTORAGE_FILE))
    localstorage = load_localstorage_file(LOCALSTORAGE_FILE)

    options = Options()
    options.add_argument('--headless')

    logger.debug('Initiating webdriver')
    driver = webdriver.Chrome(chrome_options=options, executable_path=CHROMEDRIVER_PATH)

    try:
        logger.debug('Loading page')
        get_page(driver)

        logger.debug('Injecting localstorage')
        driver_localstorage = LocalStorage(driver)
        set_localstorage(driver_localstorage, localstorage, clear=True)

        logger.debug('Reloading page')
        get_page(driver)

        logger.debug('Waiting for menuAccountUsername to be visible')
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'menuAccountUsername')))
        username = driver.find_element_by_id('menuAccountUsername').get_attribute('innerHTML')
        logger.info('Successfuly logged in, username: {}'.format(username))

        claim_timer = driver.find_element_by_id('claimTimer').get_attribute('innerHTML')
        if claim_timer == '':
            logger.info('Claiming the reward...')
            claim = driver.find_element_by_id('claimHolder')
            claim.click()
            logger.debug('Waiting for claimTimer to be visible')
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'claimTimer')))
            logger.info('Reward claimed')
        else:
            logger.info('Cannot claim the reward. You have to wait {}'.format(claim_timer))
    except Exception as e:
        driver.quit()
        logger.error(str(e))

    logger.info('Quitting')
    driver.quit()

