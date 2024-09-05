from django.shortcuts import render
from . import forms
import constants, requests, logging
from django.http import HttpResponse

api_key = constants.POKEMONTCG_API_KEY
logger = logging.getLogger(__name__)

def home(request):
    form = forms.SearchForm()

    return render(request, 'base.html', {'form': form})

def search(request):
    form = forms.SearchForm(request.GET)
    results = []

    header = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key,
    }

    if form.is_valid():
        search = form.cleaned_data['search']
        params = {
            'q': f'name:"{search}"'
        }
        response = requests.get(f"https://api.pokemontcg.io/v2/cards", headers=header, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', [])
        else:
            logger.error('API Request Failed with status code %d', response.status_code)
            
    return render(request, 'search/search_results.html', {'form': form, 'results': results})
            

    