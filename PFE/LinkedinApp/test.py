import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
from linkedin_api import Linkedin
from bs4 import BeautifulSoup

secteur = 'Administration publique'



driver_options = webdriver.ChromeOptions()
sleep(3)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
sleep(5)
experience = pd.DataFrame()
skills = pd.DataFrame()
education = pd.DataFrame()
profiles = pd.DataFrame()


li_us = 'anasselbouni@hotmail.com'
li_pa = 'Bim@1997'

driver.get("https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
sleep(2)
username = driver.find_element_by_id("username")
username.send_keys(li_us)
password = driver.find_element_by_id("password")
password.send_keys(li_pa)
login = driver.find_element_by_class_name("btn__primary--large")
login.click()

sleep(2)

classname ="artdeco-hoverable-content artdeco-hoverable-content--visible reusable-search-filters-trigger-dropdown__content artdeco-hoverable-content--inverse-theme artdeco-hoverable-content--default-spacing artdeco-hoverable-content--bottom-placement"

industry = "industry=%5B%224%22%5D&origin=FACETED_SEARCH"
schoolFilter = "schoolFilter=%5B%222475568%22%5D"
serviceCategory = "serviceCategory=%5B%22602%22%5D&sid=a%2CD"
page = "page={}".format(1)
base = "https://www.linkedin.com/search/results/people/?"
link = '{}{}&{}&{}&{}'.format(base, industry, schoolFilter, serviceCategory, page)
driver.get(link)

sleep(2)
selects = driver.find_element_by_id("artdeco-hoverable-artdeco-gen-42")
driver.execute_script("arguments[0].setAttribute('class', 'artdeco-hoverable-content artdeco-hoverable-content--visible reusable-search-filters-trigger-dropdown__content artdeco-hoverable-content--inverse-theme artdeco-hoverable-content--default-spacing artdeco-hoverable-content--bottom-placement')", selects)
secteur_input = driver.find_element_by_xpath('//*[@id="artdeco-hoverable-artdeco-gen-42"]/div[1]/div/form/fieldset/div[1]/div/div/input')
secteur_input.send_keys(secteur)
sleep(300)
