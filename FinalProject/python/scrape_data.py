from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import numpy as np

import time
import random

def navigateToProfile(profileURL, driver, wait):
    driver.execute_script("document.location.href = \"" + profileURL + "\";")
    profileName = profileURL.split("/")[-1]
    wait.until(EC.url_contains(profileName))

inputPath = input("Url input path? ")
outputPath = input("Data output path? ")

lines = None
with open(inputPath, "r") as inputFile:
    lines = inputFile.readlines()

outFile = open(outputPath, "w")

outFile.write("name,gradYear,major,jobTitle,jobMatches")

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(1500, 900)
driver.implicitly_wait(30)

wait = WebDriverWait(driver, 30)

driver.get("https://www.linkedin.com")

delay = np.random.exponential(4)
print("Delay: " + str(delay + 4) + " seconds")
time.sleep(delay + 4)

counter = 0
while counter < len(lines):
    line = lines[counter].strip()
    
    navigateToProfile(line, driver, wait)
    
    delay = np.random.exponential(4)
    print("Delay: " + str(delay + 4) + " seconds")
    time.sleep(delay + 4)

    if "authwall" in driver.current_url:
        print("Authwall hit! Clearing cookies and trying again...")
        driver.delete_all_cookies()
        driver.get("https://www.linkedin.com")
        continue

    name = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__title").text

    degreeSubtext = driver.find_elements(By.XPATH, "//li/a[contains(@href, \"university-of-utah\")]/..//*[@class=\"education__item education__item--degree-info\"]")
    major = degreeSubtext[0].text + " - " + degreeSubtext[1].text

    print(name + ": " + major)

    counter += 1


input("Finished. Press enter to continue...")

driver.close()