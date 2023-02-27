import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

firefox_options = Options()
firefox_profile = FirefoxProfile()
# firefox_options.headless = True
firefox_options.add_argument("--start-maximized")
firefox_options.add_argument("--mute-audio")
firefox_options.add_argument("--disable-notifications")
firefox_options.add_argument("--disable-popup-blocking")
firefox_options.add_argument("--disable-extensions")

driver = webdriver.Firefox(firefox_profile=firefox_profile, options=firefox_options)
with open("data/cams.csv") as f:
    watchable_urls = f.read().split("\n")

# shuffle the list of urls
random.shuffle(watchable_urls)

# remove bad urls
bad_urls = []

for url in watchable_urls:
    if url not in bad_urls:
        time.sleep(2)
        try:
            driver.get(url)
        except Exception as e:
            print(e)
            bad_urls.append(url)
            continue
        # now click the play button at .ytp-play-button
        time.sleep(1)
        try:
            play_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-play-button"))
            )
            play_button.click()
        except Exception as e:
            print(e)
            bad_urls.append(url)
            continue
        # now wait for the video to load
        time.sleep(1)
        try:
            video = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
            )
        except Exception as e:
            print(e)
            bad_urls.append(url)
            continue
        # skip the ad
        time.sleep(1)
        try:
            skip_ad_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-ad-skip-button"))
            )
            skip_ad_button.click()
        except Exception as e:
            print(e)
            bad_urls.append(url)
            continue
        # now maximize the video by clicking the fullscreen button
        try:
            fullscreen_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-fullscreen-button"))
            )
            fullscreen_button.click()
        except Exception as e:
            print(e)
            bad_urls.append(url)
            continue
    # save bad urls to a file
    with open("data/bad_urls.csv", "w") as f:
        for url in bad_urls:
            f.write(url + "\n ")


    time.sleep(60)
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])

driver.close()
