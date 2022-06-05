from linkedin_api import Linkedin
import pandas as pd
import random
from time import sleep

class linkedin_manager:
    def __init__(self,accounts,industr,vanityname):
        self.accounts=accounts
        self.industr=industr
        self.vanityname=vanityname

    def profile_lookup(self):
        vanityname=self.vanityname
        profil={'has not been lookup':vanityname}
        for account in self.accounts:
            try:
                li_us=account['email']
                li_pa=account['password']
                api = Linkedin(li_us, li_pa)
                profil = api.get_profile(vanityname)
                break
            except:
                pass

        return profil


    def profile_compilation(self,profilesnames,return_dict):
        a, b, c, d = 0, 0, 0, 0
        experience = pd.DataFrame()
        skills = pd.DataFrame()
        education = pd.DataFrame()
        profiles = pd.DataFrame()
        for vanityname in profilesnames:
            try:
                profil = self.profile_lookup()
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
                        'sector': self.industr,
                        'Nom': profil['firstName'] + ' ' + profil['lastName'],
                        'headline': profil['headline'],
                        'location': location,
                        'Lien Linkedin': ' https://www.linkedin.com/in/{}'.format(vanityname)
                    }, ignore_index=True
                )

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
                            'PersonID': vanityname,
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

            # sleep(random.randint(100,200))

        return_dict[[{'experience':experience},{'education':education},{'profiles':profiles},{'skills':skills},]] = [{'experience':experience},{'education':education},{'profiles':profiles},{'skills':skills},]

