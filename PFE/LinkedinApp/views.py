from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from time import sleep
from linkedin_api import Linkedin
from bs4 import BeautifulSoup
import nltk
import spacy
from .models import linkedin_account,Linkedin_Profils
from .scripts.linkd_api import linkedin_manager
import os
from PFE.settings import BASE_DIR
from collections import Counter

########link###########################
accounts=linkedin_account.objects.all()
accounts_list=[]
for account in accounts:
    ac_dict={}
    ac_dict['username']=account.email
    ac_dict['password']=account.password
    print(ac_dict)
    accounts_list.append(ac_dict)
l_m = linkedin_manager(accounts=accounts_list)
#############################################




#essential entity models downloads
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')






def index(request):

    profiles = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx',index_col=0, sheet_name="profiles")
    experience = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx',index_col=0, sheet_name="experience")
    education = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx',index_col=0, sheet_name="education")
    skills = pd.read_excel(f'{BASE_DIR}/LinkedinApp/data.xlsx',index_col=0, sheet_name="skills")
    secteurs = profiles['sector'].drop_duplicates().tolist()
    titres = profiles['headline'].drop_duplicates().tolist()
    villes = profiles['location'].dropna().drop_duplicates().tolist()
    diplomes = education['degreeName'].drop_duplicates().tolist()
    context = {
        'secteurs' : secteurs,
        'villes' : villes,
        'titres' : titres,
        'diplomes' : diplomes
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
        id=request.POST.get('username')
        prfl=l_m.profile_lookup(id)
        dataa={}
        l=[f.name for f in Linkedin_Profils._meta.get_fields()]
        for key,value in prfl.items():
            if key in l:
                dataa[key]=value
            else:
                pass


        dataa['vanityname']=prfl['firstName']+'|'+prfl['lastName']
        print('data:',dataa)
        obj,created=Linkedin_Profils.objects.get_or_create(**dataa)
        data=obj.__dict__
        del data['_state']


        return JsonResponse(data,safe=False)
    else :
        return HttpResponse(content='method not allowed ',status=400)

@csrf_exempt
def idsearch(request):

    context = {
    }




    return render(request, 'result.html', context)




def sector_list(request):
    sectors=[]
    [sectors.append(pr.sector) for pr in Linkedin_Profils.objects.all() if pr.sector not in sectors]
    if len(sectors)> 0:
        return JsonResponse(sectors, safe=False)
    else:
        return HttpResponse(content='no  sectors in the db search using ddg keyword',status=200)


@csrf_exempt
def mass_search(request):
    if request.method == 'POST':
        sector=request.POST.get('sector')
        try:
            os.system(f'python3 {BASE_DIR}/scripts/main.py {sector}')
        except Exception:
            print(Exception)
    else :
        return HttpResponse(content='method not allowed ',status=400)