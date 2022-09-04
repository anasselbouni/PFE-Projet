from linkedin_api import Linkedin
from LinkedinApp.models import Linkedin_Profils
from datetime import datetime
from dateutil import relativedelta


# Script pour obtenir les profiles
class linkedin_manager:
    def __init__(self, accounts=None, industr=None, pl=None, prx=None):
        self.accounts = accounts
        self.industr = industr
        self.pl = pl
        self.proxy = prx

    def profile_lookup(self, vanityname):

        for account in self.accounts:
            experience = []
            skills = []
            education = []
            dataa = {}
            try:
                ##### Extraction de profile
                li_us = str(account['username'])
                li_pa = str(account['password'])
                if self.proxy != None:
                    api = Linkedin(li_us, li_pa, proxies=self.proxy)
                else:
                    api = Linkedin(li_us, li_pa)

                prfl = api.get_profile(vanityname)

                ##### Nettoyage et préparation des données
                l = [f.name for f in Linkedin_Profils._meta.get_fields()]
                for key, value in prfl.items():
                    if key in l:
                        dataa[key] = value
                    else:
                        pass
                try:
                    dataa['city'] = "{} {}".format(prfl['geoLocationName'], prfl['geoCountryName']),
                except:
                    try:
                        dataa['city'] = "{}".format(prfl['geoLocationName']),
                    except:
                        try:
                            dataa['city'] = "{}".format(prfl['geoCountryName'])
                        except:
                            dataa['city'] = ''
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
                # experience
                exp_months = 0
                for i in prfl["experience"]:
                    try:
                        try:
                            if None not in (i["timePeriod"]["startDate"]["month"],
                                            i["timePeriod"]["startDate"]['year']):
                                startDate = {'year': 0, 'month': 0, }
                            if i["timePeriod"]["startDate"]['month'] is None and \
                                    i["timePeriod"]["startDate"]['year'] is not None:
                                startDate = {'year': i["timePeriod"]["startDate"]['year'], 'month': 0, }
                            if i["timePeriod"]["startDate"]['month'] is not None and \
                                    i["timePeriod"]["startDate"]['year'] is None:
                                startDate = {'year': 0, 'month': i["timePeriod"]["startDate"]['month'], }
                            if i["timePeriod"]["startDate"]['month'] is not None and \
                                    i["timePeriod"]["startDate"]['year'] is not None:
                                startDate = {'year': i["timePeriod"]["startDate"]['year'],
                                             'month': i["timePeriod"]["startDate"]['month'], }

                        except:
                            startDate = {'year': 0, 'month': 0, }

                        try:
                            if i["timePeriod"]["endDate"]['month'] is None and \
                                    i["timePeriod"]["endDate"]['year'] is not None:
                                endDate = {'year': i["timePeriod"]["endDate"]['year'], 'month': 0, }
                            if i["timePeriod"]["endDate"]['month'] is not None and \
                                    i["timePeriod"]["endDate"]['year'] is not None:
                                endDate = {'year': 0, 'month': i["timePeriod"]["endDate"]['month'], }
                            if i["timePeriod"]["endDate"]['month'] is not None and \
                                    i["timePeriod"]["endDate"]['year'] is not None:
                                endDate = {'year': i["timePeriod"]["endDate"]['year'],
                                           'month': i["timePeriod"]["endDate"]['month'], }
                        except:
                            endDate = {'year': 0, 'month': 0, }
                        d1 = '{}/{}/{}'.format(1, startDate['month'],
                                               startDate['year'])
                        d2 = '{}/{}/{}'.format(1, endDate['month'], endDate['year'])
                        start_date = datetime.strptime(d1, "%d/%m/%Y")
                        end_date = datetime.strptime(d2, "%d/%m/%Y")

                        delta = relativedelta.relativedelta(end_date, start_date)
                        exp_months = exp_months + (delta.years * 12) + delta.months
                        try:
                            locationName = i["locationName"]
                        except:
                            locationName = ''
                        try:
                            title = i["title"]
                        except:
                            title = ''
                        try:
                            description = i["description"]
                        except:
                            description = ''
                        try:
                            companyName = i["companyName"]
                        except:
                            companyName = ''
                        experience.append({
                            'title': title,
                            'locationName': locationName,
                            'description': description,
                            'companyName': companyName,
                            'endDate': endDate,
                            'startDate': startDate,
                        })


                    except Exception as e:
                        print(e)
                        pass

                years, months = divmod(exp_months, 12)
                total_experience = {'years': years, 'months': months}
                # skills
                try:
                    for t in prfl["skills"]:
                        skills.append(
                            {
                                'name': t["name"],
                            }
                        )

                except:
                    pass
                # education
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

                mydict = {"Nom": dataa["Nom"],
                          "vanityname": vanityname,
                          "summary": dataa["summary"],
                          "location": dataa['city'][0],
                          "Lien_Linkedin": dataa["Lien_Linkedin"],
                          "industryName": dataa["industryName"],
                          "headline": dataa["headline"],
                          "total_experience": total_experience,
                          "experience": experience,
                          "education": education,
                          "skills": skills}
                break
            except:
                mydict = {"vanityname": 0}
                break

        return mydict, skills, education, experience
