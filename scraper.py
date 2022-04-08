#!/usr/bin/env python3

from turtle import down
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import os
import pickle
import time
import argparse


# miscellaneous globals
# directory of scraper.py
CUR_DIR = os.path.dirname(__file__)
# length of sleeps, adjust based on internet connection
SLEEP_LEN = 3


def login():
    # website account creds
    with open(f"{CUR_DIR}/account.txt", "r") as fin:
        account = fin.read().split()
    email = account[0]
    password = account[1]

    # Creating a webdriver instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # This instance will be used to log into website

    # Opening website's login page
    with open("website_login_url.txt", "r") as fin:
        login_url = fin.read().strip()
    driver.get(login_url)

    # waiting for the page to load
    time.sleep(SLEEP_LEN)

    # entering username
    username = driver.find_element(By.ID, "username")
    
    # Enter Your Email Address
    username.send_keys(email)  

    # entering password
    pword = driver.find_element(By.ID, "password")
    
    # Enter Your Password
    pword.send_keys(password)   

    # Clicking on the log in button
    # Format (syntax) of writing XPath --> 
    # //tagname[@attribute='value']
    driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()

    # save url after login
    base_url = driver.current_url

    return (driver, base_url)


def do_profile_links(driver, base_url):
    # TODO: maybe try with location services turned off?

    # list of male and female names
    with open(f"{CUR_DIR}/male_names.txt", "r") as fin:
        male_names = fin.read().split()
    with open(f"{CUR_DIR}/female_names.txt", "r") as fin:
        female_names = fin.read().split()

    profile_list = []

    # iterate through all names
    # 0 for male, 1 for female
    for gender in range(2):
        # 100 names in each list 
        for i in range(100):
            if gender == 0:
                name = male_names[i]
            else:
                name = female_names[i]

            # get first profile
            driver.get(base_url)
            time.sleep(SLEEP_LEN)
            # search name
            search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
            search_bar.send_keys(name)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(SLEEP_LEN)
            # another enter should take us to first profile
            actions = ActionChains(driver)
            actions.send_keys(Keys.RETURN)
            actions.perform()
            time.sleep(SLEEP_LEN)
            profile_list.append((driver.current_url, gender))

            # get second profile
            driver.get(base_url)
            time.sleep(SLEEP_LEN)
            # search name
            search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
            search_bar.send_keys(name)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(SLEEP_LEN)
            # 3 tabs to get to next then enter to get to second profile
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.RETURN)
            actions.perform()
            time.sleep(SLEEP_LEN)
            profile_list.append((driver.current_url, gender))

            # get third profile
            driver.get(base_url)
            time.sleep(SLEEP_LEN)
            # search name
            search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
            search_bar.send_keys(name)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(SLEEP_LEN)
            # 6 tabs to get to next then enter to get to second profile
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.RETURN)
            actions.perform()
            time.sleep(SLEEP_LEN)
            profile_list.append((driver.current_url, gender))

            # store incremental progress
            with open(f"{CUR_DIR}/profile_list.pkl", "wb") as fout:
                pickle.dump(profile_list, fout)


def do_picture_links(driver):
    # TODO handle case with no profile picture

    # get list of profile links 
    with open(f"{CUR_DIR}/profile_list.pkl", "rb") as fin:
        profile_list = pickle.load(fin)
    
    picture_list = []

    for item in profile_list:
        profile_link = item[0]
        gender = item[1]

        # visit profile
        driver.get(profile_link)
        time.sleep(SLEEP_LEN)

        # javascript to extract profile picture link
        js = '''var images = document.getElementsByTagName('img'); 
            var index = 0;
            for (var i = 0; i < images.length; i++){ 
                if (images[i].className.includes('profile-picture')){
                    return images[i].src;
                }
            }'''
        try:
            picture_link = driver.execute_script(js)
            if picture_link is not None:
                picture_list.append((picture_link, gender))
        except:
            continue

        # store incremental progress
        with open(f"{CUR_DIR}/picture_list.pkl", "wb") as fout:
            pickle.dump(picture_list, fout)


def do_download_pictures():
    # TODO
    pass


def do_cleanup():
    for fname in os.listdir(CUR_DIR):
        if fname[-4:] == ".pkl":
            os.remove(fname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile_links", action="store_true")
    parser.add_argument("--picture_links", action="store_true")
    parser.add_argument("--download_pictures", action="store_true")
    parser.add_argument("--cleanup", action="store_true")
    args = parser.parse_args()

    profile_links = False 
    picture_links = False 
    download_pictures = False
    cleanup = False
    if not (args.profile_links or args.picture_links or args.download_pictures or args.cleanup):
        profile_links = True
        picture_links = True 
        download_pictures = True
        cleanup = True
    if args.profile_links:
        profile_links = True 
    if args.picture_links:
        picture_links = True 
    if args.download_pictures:
        download_pictures = True 
    if args.cleanup:
        cleanup = True

    (driver, base_url) = login()
    if profile_links:
        print ("Gathering profile links...")
        do_profile_links(driver, base_url)
        print ("Finished.")
    if picture_links:
        print ("Gathering picture links...")
        do_picture_links(driver)
        print ("Finished.")
    driver.close()
    if download_pictures:
        print ("Downloading pictures...")
        do_download_pictures()
        print ("Finished.")
    if cleanup:
        do_cleanup()
    