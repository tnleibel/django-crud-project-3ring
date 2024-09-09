from django.shortcuts import render, redirect
from . import forms
import constants, requests, logging
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Card, UserProfile


api_key = constants.POKEMONTCG_API_KEY
logger = logging.getLogger(__name__)

def home(request):
    search_form = forms.SearchForm()

    return render(request, 'base.html', {'search_form': search_form})

@login_required
def card_index(request):
    
    
    if request.method == 'GET':
        
        user = UserProfile.objects.get(user=request.user)
        return render(request, 'cards/index.html', { 'user': user })        

    elif request.method =='POST':
        name = request.POST.get('name')
        supertype = request.POST.get('supertype')
        types = request.POST.get('types', [])
        set = request.POST.get('set')
        rarity = request.POST.get('rarity')
        image = request.POST.get('image')

        card = Card.objects.create(
            name = name,
            supertype = supertype,
            types = types,
            set = set,
            rarity = rarity,
            image = image,
            is_owned = False,
            )
        card.save()
        
        user = UserProfile.user
        UserProfile.objects.get(user=request.user).card_binder.add(card)
        
        return redirect('card-index')

def search(request):
    search_form = forms.SearchForm(request.GET)
    results = []

    header = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key,
    }

    if search_form.is_valid():
        search = search_form.cleaned_data['search']
        params = {
            'q': f'name:"{search}"'
        }
        response = requests.get(f"https://api.pokemontcg.io/v2/cards", headers=header, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', [])
        else:
            logger.error('API Request Failed with status code %d', response.status_code)
            
    return render(request, 'search/search_results.html', {'search_form': search_form, 'results': results})

def signup(request):
    error_message = ''
    if request.method =='POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            UserProfile.objects.create(user=request.user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up, please try again.'
    
    signup_form = UserCreationForm()
    context = {'signup_form': signup_form, 'error-message': error_message}
    return render(request, 'signup.html', context)

class Login(LoginView):
    template_name = 'login.html' 





    