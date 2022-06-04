from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from time import sleep
from linkedin_api import Linkedin
from bs4 import BeautifulSoup
from PFE.settings import BASE_DIR
import nltk
import spacy

# essential entity models downloads
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
def idsearch(request):
    username = request.POST.get("username")

    context = {
    }

    return render(request, 'result.html', context)