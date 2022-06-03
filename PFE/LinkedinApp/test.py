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

experience = pd.DataFrame()
skills = pd.DataFrame()
education = pd.DataFrame()
profiles = pd.DataFrame()


profil={'summary': 'Enthusiastic and resourceful professional with 4+ years of experience in discovering, acquiring and evaluating talents for a company with 2000+ employees. Significantly improved recruitment strategies using innovative sourcing techniques. Provided valuable counseling on the entire hiring process in order to ensure that the best talents were selected.', 'industryName': 'Human Resources', 'lastName': 'Ait Taleb', 'locationName': 'Morocco', 'student': False, 'geoCountryName': 'Morocco', 'geoCountryUrn': 'urn:li:fs_geo:102787409', 'geoLocationBackfilled': False, 'elt': False, 'industryUrn': 'urn:li:fs_industry:137', 'firstName': 'Anas', 'entityUrn': 'urn:li:fs_profile:ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo', 'geoLocation': {'geoUrn': 'urn:li:fs_geo:106186529'}, 'geoLocationName': 'Casablanca-Settat', 'location': {'basicLocation': {'countryCode': 'ma'}}, 'headline': 'Talent Acquisition Partner', 'displayPictureUrl': 'https://media-exp1.licdn.com/dms/image/D4E35AQGXkqbGR3fazQ/profile-framedphoto-shrink_', 'profile_id': 'ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo', 'experience': [{'locationName': 'Casablanca et périphérie', 'entityUrn': 'urn:li:fs_position:(ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo,1873134499)', 'geoLocationName': 'Casablanca et périphérie', 'geoUrn': 'urn:li:fs_geo:90010262', 'companyName': 'Capgemini', 'timePeriod': {'startDate': {'month': 11, 'year': 2021}}, 'company': {'employeeCountRange': {'start': 10001}, 'industries': ['Information Technology and Services']}, 'title': 'Talent Acquisition Partner', 'region': 'urn:li:fs_region:(ma,9619)', 'companyUrn': 'urn:li:fs_miniCompany:157240', 'companyLogoUrl': 'https://media-exp1.licdn.com/dms/image/C4D0BAQFWzOAVgGjUUA/company-logo_'}, {'locationName': 'Marrakech, Marrakesh-Safi, Maroc', 'entityUrn': 'urn:li:fs_position:(ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo,1819419223)', 'geoLocationName': 'Marrakech, Marrakesh-Safi, Maroc', 'geoUrn': 'urn:li:fs_geo:101421689', 'companyName': 'Buddha-Bar Worldwide', 'timePeriod': {'endDate': {'month': 11, 'year': 2021}, 'startDate': {'month': 8, 'year': 2021}}, 'company': {'employeeCountRange': {'start': 1001, 'end': 5000}, 'industries': ['Restaurants']}, 'title': 'HR Manager', 'region': 'urn:li:fs_region:(ma,0)', 'companyUrn': 'urn:li:fs_miniCompany:11251859', 'companyLogoUrl': 'https://media-exp1.licdn.com/dms/image/C4D0BAQHmn0OB_ZJjdg/company-logo_'}, {'locationName': 'Casablanca, Casablanca-Settat, Maroc', 'entityUrn': 'urn:li:fs_position:(ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo,1683152462)', 'geoLocationName': 'Casablanca, Casablanca-Settat, Maroc', 'geoUrn': 'urn:li:fs_geo:102727945', 'companyName': 'SAHAM Assurance', 'timePeriod': {'endDate': {'month': 7, 'year': 2021}, 'startDate': {'month': 1, 'year': 2020}}, 'description': '• Recadrage des besoins en recrutement,\n• Définition de la stratégie de sourcing adéquate aux profils recherchés,\n• Chasse de tête via LinkedIn Recruiter, CVthèque, diffusion d’annonces,\n• Rédaction et publication des annonces de recrutement,\n• Tri des CV\n• Gestion des intérimaires/Stagiaires\n• Gestion des stagiaires et de la relation écoles.', 'company': {'employeeCountRange': {'start': 1001, 'end': 5000}, 'industries': ['Insurance']}, 'title': 'Chargé de développement RH', 'region': 'urn:li:fs_region:(ma,0)', 'companyUrn': 'urn:li:fs_miniCompany:5162198', 'companyLogoUrl': 'https://media-exp1.licdn.com/dms/image/C560BAQFLvx2Rb8_NMQ/company-logo_'}, {'locationName': 'Casablanca, Grand Casablanca, Morocco', 'entityUrn': 'urn:li:fs_position:(ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo,1345956728)', 'geoLocationName': 'Casablanca, Grand Casablanca, Morocco', 'companyName': 'SAHAM Assurance', 'timePeriod': {'endDate': {'month': 1, 'year': 2020}, 'startDate': {'month': 7, 'year': 2018}}, 'description': '• Recueil des besoins en formation à partir des évaluations annuelles\n• Harmonisation et préparation du plan de formation\n• Ciblage des prestataires et formateurs\n• Budgétisation des actions de formation\n• Pilotage et suivi du budget\n• Déploiement des actions de formation\n• Evaluation à chaud et à froid\n• Reportings(mensuel et annuel)\n• Gestion de la logistique de formation\n• Gestion et animation de la platefome E-Learning', 'company': {'employeeCountRange': {'start': 1001, 'end': 5000}, 'industries': ['Insurance']}, 'title': 'Chargé de formation', 'companyUrn': 'urn:li:fs_miniCompany:5162198', 'companyLogoUrl': 'https://media-exp1.licdn.com/dms/image/C560BAQFLvx2Rb8_NMQ/company-logo_'}, {'locationName': 'Marrakech', 'entityUrn': 'urn:li:fs_position:(ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo,1000733071)', 'geoLocationName': 'Marrakech', 'companyName': 'Royal Mansour Marrakech', 'timePeriod': {'endDate': {'month': 10, 'year': 2017}, 'startDate': {'month': 5, 'year': 2017}}, 'description': '• Gestion des congés / récupérations,\n• Création et gestion des dossiers du personnel,\n• Traitement et correction des anomalies de pointage ‘PRIMION’\n• Etablissement des états mensuels,\n• Gestion des expatriés ‘logement/carte séjour/anapec/etat des lieux’,\n• Administration du système de pointage et de gestion d’accès\n• Traitement des sanctions', 'company': {'employeeCountRange': {'start': 501, 'end': 1000}, 'industries': ['Hospitality']}, 'title': "Chargé d'administration RH", 'companyUrn': 'urn:li:fs_miniCompany:1684159', 'companyLogoUrl': 'https://media-exp1.licdn.com/dms/image/C4D0BAQE0WcUVEn7XVg/company-logo_'}], 'skills': [{'name': 'Management'}, {'name': 'Microsoft Office'}, {'name': 'Gestion de projet'}, {'name': 'Leadership'}, {'name': 'Microsoft Excel'}, {'name': 'Change Management'}, {'name': 'Recrutement'}, {'name': 'GPEC'}, {'name': 'Formation'}, {'name': 'Management des équipes'}, {'name': 'audit social'}, {'name': 'Gestion du changement'}, {'name': 'Ressources humaines (RH)'}], 'education': [{'entityUrn': 'urn:li:fs_education:(ACoAABSkxhsB78QV22BXD2Y2OpNfIQhDv8khyFo,221900264)', 'school': {'objectUrn': 'urn:li:school:3157072', 'entityUrn': 'urn:li:fs_miniSchool:3157072', 'active': True, 'schoolName': 'ENCG MARRAKECH', 'trackingId': '7kigvsEySaCOZYUV1d3Zlw==', 'logoUrl': 'https://media-exp1.licdn.com/dms/image/C4D0BAQGfrl2u2ACftQ/company-logo_'}, 'activities': 'Membre volontaire à l’opération DIR IDDIK De INWI.\n\nPrésident du Bureau des Etudiants de L’ENCGM 2012/2013/2014\n\nPrésident de l’association Marrakech challenge Cup.\n\nMembre au club social TouSolidaire de l’ENCGM.', 'grade': 'Assez bien', 'timePeriod': {'endDate': {'month': 11, 'year': 2016}, 'startDate': {'year': 2010}}, 'degreeName': 'Master', 'schoolName': 'ENCG MARRAKECH', 'fieldOfStudy': 'Management des ressources humaines', 'schoolUrn': 'urn:li:fs_miniSchool:3157072'}]}

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
vanityname = profil['firstName'] + ' ' + profil['lastName']
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
            'PersonID': vanityname,
            'degreeName': degreeName,
            'schoolName': i['schoolName'],
            'fieldOfStudy': fieldOfStudy,
            'startdate': startdate,
            'endDate': endate,
        }, ignore_index=True
    )

print(experience)

import pandas as pd
from openpyxl import load_workbook
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

