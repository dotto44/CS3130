from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import random
from getpass import getpass

outputPath = input("Output location? ")
username = input("LinkedIn username? ")
password = getpass("LinkedIn password? ")
numPages = int(input("Pages to scrape? "))

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(1500, 900)
driver.implicitly_wait(30)

wait = WebDriverWait(driver, 30)

### Log into LinkedIn

print("Logging in...")

driver.get("https://www.linkedin.com/login")

usernameBox = driver.find_element_by_id("username")
passwordBox = driver.find_element_by_id("password")

usernameBox.send_keys(username)
passwordBox.send_keys(password)

submitButton = driver.find_element_by_css_selector("button[type=submit]")

submitButton.click()

time.sleep(3)

### Enter advanced search

print("Opening search dialog...")

searchBox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-global-typeahead__input')))
time.sleep(1)
searchBox.click()
time.sleep(1)
searchBox.send_keys(" ")
time.sleep(1)
searchBox.send_keys(Keys.BACKSPACE)
time.sleep(1)
searchBox.send_keys(Keys.RETURN)

peopleButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label=People]')))
time.sleep(3)
peopleButton.click()

wait.until(EC.url_contains("linkedin.com/search/results/people"))
time.sleep(3)

filtersButton = driver.find_element_by_xpath("//button[text()='All filters']")
filtersButton.click()

# wait for filter dialog to appear
filterModalDiv = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='a11y-text' and text()='All filters']/.."))) 
time.sleep(1)

### Enter filter criteria

print("Entering search criteria...")

schoolInput = driver.find_element_by_xpath("//label[text()='School']/input")
schoolInput.send_keys('University of Utah -"Utah State University" -"Utah Valley University" -"Southern Utah University"')

time.sleep(1)

showResultsButton = driver.find_element_by_xpath("//span[@class='a11y-text' and text()='All filters']/..//span[@class='artdeco-button__text' and text()='Show results']/..")
showResultsButton.click()

print("Scraping starting in 10 seconds...")
time.sleep(10)

### Start scraping loop

with open(outputPath, "w") as output:

    pageCounter = 0
    while True:
        print("Scraping page #" + str(pageCounter + 1))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        profileLinks = driver.find_elements_by_css_selector("span.entity-result__title-text a")

        for profileLink in profileLinks:
            # profile url without parameters
            profileURL = profileLink.get_attribute("href").split("?")[0]

            # only save if it actually points to a profile
            if "linkedin.com/in" in profileURL:
                output.write(profileURL + "\n")
        
        nextButton = driver.find_element(By.CSS_SELECTOR, ".artdeco-pagination__button--next")

        if not nextButton.is_enabled():
            break
        
        pageCounter += 1
        if pageCounter >= numPages:
            break
    
        nextButton.click()

        time.sleep(random.uniform(4, 5))

print("Finished. Results written to " + outputPath)
driver.close()