import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from time import sleep
from linkedin_api import Linkedin
from bs4 import BeautifulSoup
import nltk
import spacy
from .models import linkedin_account, Linkedin_Profils
from .scripts.linkd_api import linkedin_manager
import os
from PFE.settings import BASE_DIR
from collections import Counter
from .scripts.duckduckgo import ddg_manager
from .scripts.mongo_lib import mongo_manager

########link###########################
accounts = linkedin_account.objects.all()
accounts_list = []
for account in accounts:
    ac_dict = {}
    ac_dict['username'] = account.email
    ac_dict['password'] = account.password
    accounts_list.append(ac_dict)

l_m = linkedin_manager(accounts=accounts_list)
#############################################

def converter_to_json(result_dataframe):
    # Converting result to json
    json_recordss = result_dataframe.reset_index().to_json(orient='records')
    data_result_all = []
    data_result_all = json.loads(json_recordss)
    return data_result_all

# essential entity models downloads
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')


def index(request):
    profiles = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx', index_col=0, sheet_name="profiles")
    experience = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx', index_col=0, sheet_name="experience")
    education = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx', index_col=0, sheet_name="education")
    skills = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx', index_col=0, sheet_name="skills")
    secteurs = profiles['sector'].drop_duplicates().tolist()
    titres = profiles['headline'].drop_duplicates().tolist()
    villes = profiles['location'].dropna().drop_duplicates().tolist()
    diplomes = education['degreeName'].drop_duplicates().tolist()
    context = {
        'secteurs': secteurs,
        'villes': villes,
        'titres': titres,
        'diplomes': diplomes
    }
    return render(request, 'index.html', context)


def recherche(request):
    return render(request, 'rech.html')


@csrf_exempt
def compute(request):
    keyword = request.POST.get("keyword")
    industr = request.POST.get("Cat_services")

    context = {
    }
    return render(request, 'result.html', context)


@csrf_exempt
def id_search_ajax(request):
    if request.method == 'POST':
        v_n = request.POST.get('username')
        d_m = ddg_manager('site:linkedin.com allinurl:["/in/"]', 'ma-ma')
        id = d_m.find_between_r(v_n, "https://www.linkedin.com/in/", "").replace('/', '')

        dataa,skills,education,experience = l_m.profile_lookup(vanityname=id)
        if dataa['vanityname'] != 0:
            obj = Linkedin_Profils.objects.filter(vanityname=dataa['vanityname'])
            print(obj.count())
            myquery = {"vanityname": dataa['vanityname']}
            if obj.count() > 1:
                mongo_manager().update(query=myquery, data=dataa)
            else:
                mongo_manager().insert(data=dataa)
        else:
            pass

        context = {
            'dataa': dataa,
            'experience': experience,
            'skills': skills,
            'education': education

        }

        return render(request, 'result.html', context)
    else:
        return HttpResponse(content='method not allowed ', status=400)



def sector_list(request):
    sectors = []
    [sectors.append(pr.sector) for pr in Linkedin_Profils.objects.all() if pr.sector not in sectors]
    if len(sectors) > 0:
        return JsonResponse(sectors, safe=False)
    else:
        return HttpResponse(content='no  sectors in the db search using ddg keyword', status=200)


@csrf_exempt
def mass_search(request):
    if request.method == 'POST':
        sector = request.POST.get('sector')
        keyword = request.POST.get('keyword')

        d_m = ddg_manager('site:linkedin.com allinurl:["/in/"]', 'ma-ma')

        keyword += ' Morocco'
        results = d_m.search(keyword, sector, 50)

        v_n = d_m.parse('https://www.linkedin.com/in/', results)
        v_n = list(dict.fromkeys(v_n))
        nb_add = 0
        nb_found = 0
        print(v_n)
        try:
            for i in v_n:
                try:
                    dataa, skills, education, experience = l_m.profile_lookup(vanityname=i)

                    obj = Linkedin_Profils.objects.filter(vanityname=dataa['vanityname'])
                    print(obj.count())
                    myquery = {"vanityname": dataa['vanityname']}
                    if obj.count() >= 1:
                        nb_found = nb_found + 1
                        mongo_manager().update(query=myquery, data=dataa)
                    else:
                        nb_add = nb_add + 1
                        mongo_manager().insert(data=dataa)
                except:
                    pass

                res = {"nb_add": nb_add, 'nb_found': nb_found,'success': 'done', }
            return JsonResponse(res, safe=False)
        except:
            return JsonResponse(res,safe=False)
    else:
        res = {"nb_add": 0, 'nb_found': 0, 'success': 'error', }
        return JsonResponse(res,safe=False)