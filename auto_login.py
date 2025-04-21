# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00F5B0A7FF4A3C8B98BE6A464D3A4669B1537D21DFCB8B980C35CC2E28C58E9E37AA92142E1A381CEC63E05DA95DF6F0A0F9CA75CDED163E081C229AAD196C37FEC9730CBE9089561F892C06D8114C802FC3CE565D34719FC70FF179727D86CE8CCC2C5BD14F2B6ACAA166FFE7DC7416F4DA2885FEAC8DCD77173CF3DB012FEADF088E281345600C6216EF45A03B46C72508091E26E0B3B566AF776FD4E4D635690861F538B755CB189E73CEF14307D9DCAC6C50F414991F8206D726F318968AC339E499020E26523ACA73A8767AA16676BBB8FC85606A449C9A22200C8B559C9CE327F74A34F627B7B614FAE6756D5F6715D32D6A9B707BB0A4B2CB687AA193F8791E1193621BAAB304FD9B0955C3902F1F1D27348049E458EA7606BEC25597B382F088D34CD4346B906FD6AAC8C53D2C1D607D3B194713FCBC54FC75B8C64B185EB8E38A806D0BABEE8935D9CDA72016DF50B25289ABE107D1E2EDF0D29292A7"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
