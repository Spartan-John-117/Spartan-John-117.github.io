#!/usr/bin/env python3

import argparse
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC

user_data = []

def parse_arguments():
    parser = argparse.ArgumentParser(description="Automate data insertion into my_dumbsite.")
    parser.add_argument("-u", default="http://localhost:5000")
    parser.add_argument("-p", required=True)
    return parser.parse_args()

def insert_user(driver, url, name, lastname, login, desc):

    driver.get(f"{url}/add_user")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name")))
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "lastname").send_keys(lastname)
    driver.find_element(By.ID, "login").send_keys(login)
    driver.find_element(By.ID, "desc").send_keys(desc)

    driver.find_element(By.TAG_NAME, "form").submit()


def main():
    args = parse_arguments()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))

    # Read csv file
    with (open(args.p, "r") as f):
        users = csv.reader(f, delimiter=";")

        # Skip the header
        next(users)

        for user in users: 
            insert_user(driver, args.u, user[0], user[1], user[2], user[3])

if __name__ == "__main__":
    main()
