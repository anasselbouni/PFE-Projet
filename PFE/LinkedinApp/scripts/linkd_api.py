import requests
from linkedin_api import Linkedin
import pandas as pd
import random
from time import sleep
from .proxy_list import get_proxies
from LinkedinApp.models import Linkedin_Profils


class linkedin_manager:
    def __init__(self,accounts=None,industr=None,pl=None,prx=None):
        self.accounts=accounts
        self.industr=industr
        self.pl=pl
        self.proxy=prx

    def profile_lookup(self,vanityname):

        profil={'has not been lookup':vanityname}
        print(profil)
        for account in self.accounts:
            print(account)

            experience = []
            skills = []
            education = []
            try:
                li_us=str(account['username'])
                print(li_us)
                li_pa=str(account['password'])
                if self.proxy != None:
                    api = Linkedin(li_us,li_pa,proxies=self.proxy)
                else:
                    api = Linkedin(li_us,li_pa)

                prfl = api.get_profile(vanityname)
                #

                dataa = {}
                l = [f.name for f in Linkedin_Profils._meta.get_fields()]
                for key, value in prfl.items():
                    if key in l:
                        dataa[key] = value
                    else:
                        pass

                try:
                    dataa['location'] = prfl['geoLocationName'] + ' ' + prfl['geoCountryName'],
                except:
                    try:
                        dataa['location'] = prfl['geoLocationName'],
                    except:
                        try:
                            dataa['location'] = prfl['geoCountryName']
                        except:
                            dataa['location'] = ''

                dataa['vanityname'] = vanityname
                try:
                    dataa['summary'] = prfl['summary']
                except:
                    dataa['summary'] = "NONE"
                try:
                    dataa['skills'] = prfl['skills']
                except:
                    pass
                try:
                    dataa['Nom'] = prfl['firstName'] + ' ' + prfl['lastName']
                except:
                    dataa['Nom'] = ""
                try:
                    dataa['Lien_Linkedin'] = 'https://www.linkedin.com/in/{}'.format(vanityname)
                except:
                    dataa['Lien_Linkedin'] = ""
                ###experience
                for i in prfl["experience"]:
                    try:
                        try:
                            if None not in (i["timePeriod"]["startDate"]["month"],
                                            i["timePeriod"]["startDate"]['year']):
                                timePeriod = ''
                            if i["timePeriod"]["startDate"]['month'] is None and \
                                    i["timePeriod"]["startDate"]['year'] is not None:
                                timePeriod = '{}'.format(i["timePeriod"]["startDate"]['year'])
                            if i["timePeriod"]["startDate"]['month'] is not None and \
                                    i["timePeriod"]["startDate"]['year'] is None:
                                timePeriod = '{}'.format(i["timePeriod"]["startDate"]['month'])
                            if i["timePeriod"]["startDate"]['month'] is not None and \
                                    i["timePeriod"]["startDate"]['year'] is not None:
                                timePeriod = '{}/{}'.format(i["timePeriod"]["startDate"]['month'],
                                                            i["timePeriod"]["startDate"]['year'])
                        except:
                            timePeriod = ''

                        try:
                            if i["timePeriod"]["endDate"]['month'] is None and \
                                    i["timePeriod"]["endDate"]['year'] is not None:
                                timePeriod += ' - {}'.format(i["timePeriod"]["endDate"]['year'])
                            if i["timePeriod"]["endDate"]['month'] is not None and \
                                    i["timePeriod"]["endDate"]['year'] is not None:
                                timePeriod += ' - {}'.format(i["timePeriod"]["endDate"]['month'])
                            if i["timePeriod"]["endDate"]['month'] is not None and \
                                    i["timePeriod"]["endDate"]['year'] is not None:
                                timePeriod += ' - {}/{}'.format(i["timePeriod"]["endDate"]['month'],
                                                                i["timePeriod"]["endDate"]['year'])
                        except:
                            pass

                        experience.append({
                            'title': i["title"],
                            'locationName': i["locationName"],
                            'description': i["description"],
                            'companyName': i["companyName"],
                            'timePeriod': timePeriod,
                        })

                    except:
                        pass
                ###skills
                try:
                    for t in prfl["skills"]:
                        skills.append(
                            {
                                'name': t["name"],
                            }
                        )

                except:
                    pass
                ###education
                for i in prfl['education']:
                    try:
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

                        education.append(
                            {
                                'degreeName': degreeName,
                                'schoolName': i['schoolName'],
                                'fieldOfStudy': fieldOfStudy,
                                'period': '{} - {}'.format(startdate, endate),
                            })
                    except:
                        pass
                #
                mydict = {"Nom": dataa["Nom"],
                          "vanityname": vanityname,
                          "summary": dataa["summary"],
                          "Lien_Linkedin": dataa["Lien_Linkedin"],
                          "industryName": dataa["industryName"],
                          "headline": dataa["headline"],
                          "experience": experience,
                          "education": education,
                          "skills": skills}
                break
            except:
                mydict = {"vanityname": 0}
                break

        return mydict,skills,education,experience


    def profile_compilation(self,return_dict):
        a, b, c, d = 0, 0, 0, 0
        experience = pd.DataFrame()
        skills = pd.DataFrame()
        education = pd.DataFrame()
        profiles = pd.DataFrame()
        for vanityname in self.pl:
            try:

                profil = self.profile_lookup(vanityname)
                print('pl')
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
                        'id': vanityname,
                        'sector': self.industr,
                        'Nom': profil['firstName'] + ' ' + profil['lastName'],
                        'headline': profil['headline'],
                        'location': location,
                        'Lien Linkedin': ' https://www.linkedin.com/in/{}'.format(vanityname)
                    }, ignore_index=True
                )
                print(profiles)

                for i in profil['experience']:
                    try:
                        endate = ''
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
                        startDate = ''
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
                            'degreeName': degreeName,
                            'schoolName': i['schoolName'],
                            'fieldOfStudy': fieldOfStudy,
                            'startdate': startdate,
                            'endDate': endate,
                        }, ignore_index=True
                    )




            except:
                pass
            print('waiting....')

            # sleep(random.randint(70,100))

        return_dict[[{'experience':experience},{'education':education},{'profiles':profiles},{'skills':skills},]] = [{'experience':experience},{'education':education},{'profiles':profiles},{'skills':skills},]
        return return_dict
