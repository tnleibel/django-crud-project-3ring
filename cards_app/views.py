from django.shortcuts import render, redirect
from . import forms
from .forms import SearchForm
import constants, requests, logging
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
    search_form = forms.SearchForm()
    
    if request.method == 'GET':
        
        user = UserProfile.objects.get(user=request.user)
        return render(request, 'cards/index.html', { 'user': user, 'search_form': search_form })        

    elif request.method =='POST':
        name = request.POST.get('name')
        supertype = request.POST.get('supertype')
        types = request.POST.get('types', [])
        set = request.POST.get('set')
        rarity = request.POST.get('rarity')
        image_large = request.POST.get('image_large')
        image_small = request.POST.get('image_small')

        card = Card.objects.create(
            name = name,
            supertype = supertype,
            types = types,
            set = set,
            rarity = rarity,
            image_large = image_large,
            image_small = image_small,
            is_owned = False,
            is_wanted = False,
            )
        card.save()
        
        user = UserProfile.user
        UserProfile.objects.get(user=request.user).card_binder.add(card)
        
        return redirect('card-index')

@login_required
def card_detail(request, card_id):
    search_form = forms.SearchForm()

    card = Card.objects.get(id=card_id)
    user = UserProfile.user
    favorite_cards = UserProfile.objects.get(user=request.user).favorite_cards.all()

    return render(request, 'cards/detail.html', {
        'card': card,
        'favorite_cards': favorite_cards,
        'search_form': search_form,
    })

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

@login_required
def add_favorite(request, card_id):
    error_message = ''
    card = Card.objects.get(id=card_id)
    user = UserProfile.user

    if UserProfile.objects.get(user=request.user).favorite_cards.count() < 5:
        UserProfile.objects.get(user=request.user).favorite_cards.add(card)
        return redirect('card-index')
    
    else:
        error_message = 'Your favorites are full, remove a card and try again.'
        return redirect('card-detail', {
            'error_message': error_message
        })

@login_required
def remove_favorite(request, card_id):
    card = Card.objects.get(id=card_id)
    user = UserProfile.user

    UserProfile.objects.get(user=request.user).favorite_cards.remove(card)
    return redirect('card-index')

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

class CardUpdate(LoginRequiredMixin, UpdateView):
    model = Card
    fields = ['is_owned', 'is_wanted']

class CardDelete(LoginRequiredMixin, DeleteView):
    model = Card
    success_url='/binder/'



    