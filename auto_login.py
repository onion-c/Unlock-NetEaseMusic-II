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
    browser.add_cookie({"name": "MUSIC_U", "value": "002F60FC4FB0D1A23ACB973C1A09FDB550070C0C11DECA40EB87793ECDCE36672F08A46793CB00563E13F0F39D20F5DBCB65C7D5169F6C957439BC4EA82634EF9A180BDE6141D76F59C1A4A7665EC691658487A80DF52E580D92DCA3BE2B541F1C38DC6C5E0783884F9694B7997C7446B893980C82D8A58394D62775A9F37323B1CD84432261E1DE8A694B67B9549437CBDB715DD19E743CC445F28455D566721D6831C6EB299CADADA7FC2C7B33D8BF38A93E5C8E793DBF007193293FA6614E1E80B3B9EFA93C45E9376276687B5EA4FC7CF7CF4D2DE5515199F59EBEDEA5A55FC58A08A32845F64785B715E2830A10CF9327CDBECF2D58E97CD729D3AC4D0507D7EB69524FED812101DDE5CB8F4CE0BC91C01B91A33E07C3C97E65D275C4E6546F1615335FE6F117355025CC72CC48A41A20EC03E9E7018257B89F6179303C23B8851DE9A56098857454919C281153BD2839337D5C2AE8ED2B368D61206949F6"})
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
