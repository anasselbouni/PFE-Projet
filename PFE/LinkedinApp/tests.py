import pandas as pd
from linkedin_api import Linkedin

from time import sleep
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""


a, b, c, d = 0, 0, 0, 0
li_us = 'elmotaouakilmehdi@gmail.com'
li_pa = 'ENSA@2022'
industr = "Design graphique"
keyword = ""

if industr == '' and keyword != '':
    keywords = '{} linkedin maroc site:https://www.linkedin.com/in/'.format(keyword)
if industr != '' and keyword == '':
    keywords = '{} linkedin maroc site:https://www.linkedin.com/in/'.format(industr)
if industr != '' and keyword != '':
    keywords = '{} {} linkedin maroc site:https://www.linkedin.com/in/'.format(industr, keyword)

from duckduckgo_search import ddg

profilesname_list = []
results = ddg(keywords, region='ma-ma', max_results=900)
print(results[0]['href'])
for td in results:
    href = find_between_r(td['href'], "https://www.linkedin.com/in/", "")
    if href != '':
        profilesname_list.append(href)
profilesname_list = list(dict.fromkeys(profilesname_list))
print(profilesname_list)

def profile_lookup(li_us, li_pa,vanityname):
    api = Linkedin(li_us, li_pa)
    profil = api.get_profile(vanityname)

    return profil

def profile_compilation(profilesnames):
    experience = pd.DataFrame()
    skills = pd.DataFrame()
    education = pd.DataFrame()
    profiles = pd.DataFrame()
    for vanityname in profilesnames:
        try:
            profil = profile_lookup(li_us, li_pa, vanityname)
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
                    'sector': industr,
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

            try:
                df2 = pd.read_excel('data.xlsx', sheet_name='profiles', index_col=0)

                df3 = profiles.append(df2)

                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    df3.to_excel(writer, sheet_name="profiles")
            except:
                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    profiles.to_excel(writer, sheet_name="profiles")

            try:
                df2 = pd.read_excel('data.xlsx', sheet_name='experience', index_col=0)

                df3 = experience.append(df2)

                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    df3.to_excel(writer, sheet_name="experience")
            except:
                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    experience.to_excel(writer, sheet_name="experience")

            try:
                df2 = pd.read_excel('data.xlsx', sheet_name='experience', index_col=0)

                df3 = education.append(df2)

                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    df3.to_excel(writer, sheet_name="education")
            except:
                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    education.to_excel(writer, sheet_name="education")

            try:
                df2 = pd.read_excel('data.xlsx', sheet_name='experience', index_col=0)

                df3 = skills.append(df2)

                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    df3.to_excel(writer, sheet_name="skills")
            except:
                with pd.ExcelWriter("data.xlsx",
                                    mode="a",
                                    engine="openpyxl",
                                    if_sheet_exists="overlay",
                                    ) as writer:
                    skills.to_excel(writer, sheet_name="skills")
        except:
            pass
        print('waiting....')
        sleep(200)


try:

    profile_compilation(profilesname_list)
except:
    pass
