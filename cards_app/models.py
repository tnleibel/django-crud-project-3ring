from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Card(models.Model):
    name = models.CharField(max_length=100)
    supertype = models.CharField(max_length=50)
    types = models.CharField(max_length=25)
    set = models.CharField(max_length=50)
    rarity = models.CharField(max_length=25)
    image_small = models.CharField(max_length=100)
    image_large = models.CharField(max_length=100)
    is_owned = models.BooleanField(default=False)
    is_wanted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('card-detail', kwargs={ 'card_id': self.id })
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_binder = models.ManyToManyField(Card, related_name='card_binder')
    favorite_cards = models.ManyToManyField(Card, related_name='favorite_cards')
    
    def __str__(self):
        return self.user.username

