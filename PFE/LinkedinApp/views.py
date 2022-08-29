from django.contrib.auth.decorators import login_required
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


@csrf_exempt
@login_required(login_url="/login/")
def recherche(request):
    context = {
        'page_name': 'recherche'
    }
    return render(request, 'rech.html', context)


@csrf_exempt
@login_required(login_url="/login/")
def index(request):
    secteurs = []
    skills = []
    villes = []

    mongo = mongo_manager()
    myquery = {}
    data = mongo.find_many(myquery).limit(100)
    table = pd.DataFrame()
    for x in data:
        try:
            secteurs.append(x["industryName"])
            villes.append(x["location"])
            for i in x['skills']:
                skills.append(i['name'])

            table = table.append({
                'vanityname': x["vanityname"],
                'industryName': x["industryName"],
                'Nom': x["Nom"],
                'location': x["location"],
                'Lien_Linkedin': x["Lien_Linkedin"],
                'headline': x["headline"],
                'total_experience': x["total_experience"],
                'skills': x["skills"],
            }, ignore_index=True)
            skill = 'Recrutement IT'
            for index, row in table.iterrows():
                for i in row['skills']:
                    if i['name'] == skill:
                        print('found :',i['name'])
        except:
            pass
    secteurs = list(dict.fromkeys(secteurs))
    villes = list(dict.fromkeys(villes))
    skills = list(dict.fromkeys(skills))
    table_json = converter_to_json(table)
    if request.method == 'POST':
        secteur = request.POST['secteur']
        ville = request.POST['ville']
        competence = request.POST['competence']


        # industry + city filter
        if secteur == '' and ville == '':
            myquery = {}
        if secteur == '' and ville != '':
            myquery = {'location':ville}
        if secteur != '' and ville == '':
            myquery = {'industryName':secteur}
        if secteur != '' and ville != '':
            myquery = {"$and":[{'industryName':secteur},{'location':ville}]}
        data = mongo_manager().find_many(myquery)

        table = pd.DataFrame()
        for x in data:
            table = table.append({
                'vanityname': x["vanityname"],
                'industryName': x["industryName"],
                'Nom': x["Nom"],
                'location': x["location"],
                'Lien_Linkedin': x["Lien_Linkedin"],
                'headline': x["headline"],
                'total_experience': x["total_experience"],
                'skills': x["skills"],
            }, ignore_index=True)

        # skills filter
        if competence != '':
            for inde, row in table.iterrows():
                t = 0
                for i in row['skills']:
                    if i['name'] == competence:
                        t = t + 1
                print('t : ', t)
                if t == 0:
                    table = table.drop(inde)
            print(table)
        table_json = converter_to_json(table)
        context = {
            'secteurs': secteurs,
            'villes': villes,
            'skills': skills,
            'data': table_json,
            'page_name': 'index',
        }

        return render(request, 'index.html', context)
    else:
        context = {
            'secteurs': secteurs,
            'villes': villes,
            'skills': skills,
            'data': table_json,
            'page_name': 'index',
        }
        return render(request, 'index.html', context)


@csrf_exempt
@login_required(login_url="/login/")
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
            if obj.count() == 0:
                mongo_manager().insert(data=dataa)
            else:
                mongo_manager().update(query=myquery, data=dataa)
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


@csrf_exempt
@login_required(login_url="/login/")
def table_search_ajax(request):
    if request.method == 'POST':

        vanityname = request.POST['vanityname']
        myquery = {'vanityname': vanityname}
        data = mongo_manager().find_many(myquery)
        dataa = data[0]

        context = {
            'dataa': data[0],
            'experience': data[0]['experience'],
            'skills': data[0]['skills'],
            'education': data[0]['education']

        }
        return render(request, 'result.html', context)
    else:
        return HttpResponse(content='method not allowed ', status=400)


@csrf_exempt
@login_required(login_url="/login/")
def mass_search(request):
    if request.method == 'POST':
        sector = request.POST.get('sector')
        keyword = request.POST.get('keyword')

        d_m = ddg_manager('site:linkedin.com allinurl:["/in/"]', 'ma-ma')

        keyword += ' Morocco'
        results = d_m.search(keyword, sector, 200)

        v_n = d_m.parse('https://www.linkedin.com/in/', results)
        v_n = list(dict.fromkeys(v_n))
        nb_add = 0
        nb_found = 0
        try:
            for i in v_n:
                try:
                    dataa, skills, education, experience = l_m.profile_lookup(vanityname=i)
                    if dataa['vanityname'] != 0:
                        obj = Linkedin_Profils.objects.filter(vanityname=dataa['vanityname'])
                        myquery = {"vanityname": dataa['vanityname']}
                        nb_found = nb_found + 1
                        if obj.count() >= 1:
                            mongo_manager().update(query=myquery, data=dataa)
                        else:
                            nb_add = nb_add + 1
                            mongo_manager().insert(data=dataa)
                    else:
                        pass
                except:
                    pass

                res = {"nb_add": nb_add, 'nb_found': nb_found,'success': 'done', }
            return JsonResponse(res, safe=False)
        except:
            return JsonResponse(res,safe=False)
    else:
        res = {"nb_add": 0, 'nb_found': 0, 'success': 'error', }
        return JsonResponse(res,safe=False)