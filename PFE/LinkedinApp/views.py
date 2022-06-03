from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep
from linkedin_api import Linkedin
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


counter = 0
li_us = 'elmotaouakilmehdi@gmail.com'
li_pa = 'ENSA@2022'

def driver_sele():
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("user-data-dir=C:\\Users\\Administrateur\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    sleep(3)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
    return driver

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

def profile_lookup(li_us, li_pa,profile):
    api = Linkedin(li_us, li_pa)
    profil = api.get_profile("{}".format(profile))

    return profil

def login(li_us, li_pa,driver):
    driver.get("https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    sleep(2)
    username = driver.find_element_by_id("username")
    username.send_keys(li_us)
    password = driver.find_element_by_id("password")
    password.send_keys(li_pa)
    login = driver.find_element_by_class_name("btn__primary--large")
    login.click()

    sleep(2)

def Scrapping_script(keyword,industr):
    experience = pd.DataFrame()
    skills = pd.DataFrame()
    education = pd.DataFrame()
    profiles = pd.DataFrame()


    if industr == '' and keyword != '':
        keywords = '{} linkedin maroc site:https://www.linkedin.com/in/'.format(keyword)
    if industr != '' and keyword == '':
        keywords = '{} linkedin maroc site:https://www.linkedin.com/in/'.format(industr)
    if industr != '' and keyword != '':
        keywords = '{} {} linkedin maroc site:https://www.linkedin.com/in/'.format(industr, keyword)

    from duckduckgo_search import ddg
    profilesnames = []
    results = ddg(keywords, region='ma-ma', max_results=900)
    print(results[0]['href'])
    for td in results:
        href = find_between_r(td['href'], "https://www.linkedin.com/in/", "")
        if href != '':
            profilesnames.append(href)
    profilesnames = list(dict.fromkeys(profilesnames))
    print(profilesnames)

    a, b, c, d = 0, 0, 0, 0

    sleep(5)

    for vanityname in profilesnames:
        #try:
        profil = profile_lookup(li_us, li_pa, vanityname)
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
        print(profil['firstName'] + ' ' + profil['lastName'])
        profiles = profiles.append(
            {
                'id': vanityname,
                'Nom': profil['firstName'] + ' ' + profil['lastName'],
                'headline': profil['headline'],
                'location': location,
                'Lien Linkedin': ' https://www.linkedin.com/in/{}'.format(vanityname)
            }, ignore_index=True
        )

        for i in profil['experience']:
            try:
                if i['timePeriod']['endDate']['month'] == '' and i['timePeriod']['endDate']['year'] == '':
                    endate = ''
                if i['timePeriod']['endDate']['month'] == '' and i['timePeriod']['endDate']['year'] != '':
                    endate = '{}'.format(i['timePeriod']['endDate']['year'])
                if i['timePeriod']['endDate']['month'] != '' and i['timePeriod']['endDate']['year'] == '':
                    endate = '{}'.format(i['timePeriod']['endDate']['month'])
                if i['timePeriod']['endDate']['month'] != '' and i['timePeriod']['endDate']['year'] != '':
                    endate = '{}/{}'.format(i['timePeriod']['endDate']['month'], i['timePeriod']['endDate']['year'])
            except:
                endate = ''

            try:
                if i['timePeriod']['startDate']['month'] == '' and i['timePeriod']['startDate']['year'] == '':
                    startDate = ''
                if i['timePeriod']['startDate']['month'] == '' and i['timePeriod']['startDate']['year'] != '':
                    startDate = '{}'.format(i['timePeriod']['startDate']['year'])
                if i['timePeriod']['startDate']['month'] != '' and i['timePeriod']['startDate']['year'] == '':
                    startDate = '{}'.format(i['timePeriod']['startDate']['month'])
                if i['timePeriod']['startDate']['month'] != '' and i['timePeriod']['startDate']['year'] != '':
                    startDate = '{}/{}'.format(i['timePeriod']['startDate']['month'],
                                               i['timePeriod']['startDate']['year'])
            except:
                startDate = ''

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
                    'PersonID': vanityname,
                    'title': i['title'],
                    'locationName': exp,
                    'companyName': companyName,
                    'startdate': startDate,
                    'endDate': endate,
                }, ignore_index=True
            )
        for i in profil['skills']:
            skills = skills.append(
                {
                    'PersonID': vanityname,
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
                    'PersonID': vanityname,
                    'degreeName': degreeName,
                    'schoolName': i['schoolName'],
                    'fieldOfStudy': fieldOfStudy,
                    'startdate': startdate,
                    'endDate': endate,
                }, ignore_index=True
            )
        #except:
            #pass



    return profiles, experience, skills, education



def index(request):

    return render(request, 'index.html')

def recherche(request):

    return render(request, 'rech.html')

@csrf_exempt
def compute(request):
    keyword = request.POST.get("keyword")
    industr = request.POST.get("Cat_services")
    if keyword == '':
        print("null")
    print(keyword)
    print(industr)

    try:
        profiles, experience, skills, education = Scrapping_script(keyword,industr)
        print(profiles)
        print(experience)
        print(skills)
        print(education)
    except Exception as e: print(e)

    context = {
    }

    return render(request, 'result.html', context)

@csrf_exempt
def idsearch(request):
    username = request.POST.get("username")
    if username == '':
        print("null")
    print(username)

    try:
        tt = profile_lookup(li_us, li_pa, username)
    except Exception as e: print(e)

    context = {
    }

    return render(request, 'result.html', context)