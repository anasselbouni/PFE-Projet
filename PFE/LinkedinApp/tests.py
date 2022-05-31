import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
from linkedin_api import Linkedin
from bs4 import BeautifulSoup

driver_options = webdriver.ChromeOptions()
sleep(3)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def profile_lookup(profile):
    api = Linkedin('anasselbouni@hotmail.com', 'Bim@1997')
    profile = api.get_profile("{}".format(profile))
    return profile

def login(li_us, li_pa):

    driver.get("https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    sleep(2)
    username = driver.find_element_by_id("username")
    username.send_keys(li_us)
    password = driver.find_element_by_id("password")
    password.send_keys(li_pa)
    login = driver.find_element_by_class_name("btn__primary--large")
    login.click()

    sleep(2)

def Scrapping_script(page):

    sleep(5)
    experience = pd.DataFrame()
    skills = pd.DataFrame()
    education = pd.DataFrame()
    profiles = pd.DataFrame()
    industry = "industry=%5B%224%22%5D&origin=FACETED_SEARCH"
    schoolFilter = "schoolFilter=%5B%222475568%22%5D"
    serviceCategory = "serviceCategory=%5B%22602%22%5D&sid=a%2CD"
    page = "page={}".format(page)
    base = "https://www.linkedin.com/search/results/people/?"
    link = '{}{}&{}&{}&{}'.format(base, industry, schoolFilter, serviceCategory, page)
    driver.get(link)
    sleep(3)

    # link = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/ul/li[1]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a").get_attribute('href')
    # link = driver.find_element_by_xpath("//*[@id='main']/div/div/div[1]/ul/li[1]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a").get_attribute('href')
    linktest = driver.find_element_by_xpath("//*[@id='main']/div/div/div[1]/ul")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    reviews_selector = soup.find_all('ul', class_='reusable-search__entity-result-list')
    profilesnames = []
    for td in reviews_selector[0].find_all("li"):
        # remove any newlines and extra spaces from left and right
        # headings.append(td.b.text.replace('\n', ' ').strip())

        for a in td.find_all("a", class_='app-aware-link', href=True):
            href = find_between_r(a['href'], "https://www.linkedin.com/in/", "?miniProfileUrn")
            if href != '':
                profilesnames.append(href)
    profilesnames = list(dict.fromkeys(profilesnames))
    print(profilesnames)

    # profilenam = find_between_r( link, "https://www.linkedin.com/in/", "?miniProfileUrn" )

    a, b, c, d = 0, 0, 0, 0

    sleep(5)

    for i in profilesnames:

        print(i)
        profil = profile_lookup(i)
        print(profil)
        a = a + 1
        try:
            location = profil['geoLocationName'] + ' ' + profil['geoCountryName'],
        except:
            try:
                location = profil['geoLocationName'],
            except:
                try:
                    location = profil['geoCountryName']
                except:
                    location = ''
        profiles = profiles.append(
            {
                'id': a,
                'Nom': profil['firstName'] + ' ' + profil['lastName'],
                'headline': profil['headline'],
                'location': location,
                'Lien Linkedin': ' https://www.linkedin.com/in/{}'.format(i)
            }, ignore_index=True
        )

        for i in profil['experience']:
            try:
                endate = '{}/{}'.format(i['timePeriod']['endDate']['month'], i['timePeriod']['endDate']['year'])
            except:
                endate = ''

            try:
                exp = i['geoLocationName']
            except:
                exp = ''

            try:
                companyName = i['companyName']
            except:
                companyName = ''

            experience = experience.append(
                {
                    'id': b + 1,
                    'PersonID': a,
                    'title': i['title'],
                    'locationName': exp,
                    'companyName': companyName,
                    'startdate': '{}/{}'.format(i['timePeriod']['startDate']['month'],
                                                i['timePeriod']['startDate']['year']),
                    'endDate': endate,
                }, ignore_index=True
            )
        for i in profil['skills']:
            skills = skills.append(
                {
                    'id': c + 1,
                    'PersonID': a,
                    'skill': i['name'],
                }, ignore_index=True
            )
        for i in profil['education']:
            try:
                endate = '{}'.format(i['timePeriod']['endDate']['year'])
            except:
                endate = ''
            try:
                degreeName = i['degreeName']
            except:
                degreeName = ''
            try:
                fieldOfStudy = i['fieldOfStudy']
            except:
                fieldOfStudy = ''
            try:
                startdate = i['timePeriod']['startDate']['year']
            except:
                startdate = ''
            education = education.append(
                {
                    'id': d + 1,
                    'PersonID': a,
                    'degreeName': degreeName,
                    'schoolName': i['schoolName'],
                    'fieldOfStudy': fieldOfStudy,
                    'startdate': startdate,
                    'endDate': endate,
                }, ignore_index=True
            )

    print(profiles)
    print(experience)
    print(skills)
    print(education)

counter = 0
page = 0
li_us = 'anasselbouni@hotmail.com'
li_pa = 'Bim@1997'

while counter == 0:
    try:
        login(li_us, li_pa)
        page = page + 1
        Scrapping_script(page)
    except:
        driver.close()