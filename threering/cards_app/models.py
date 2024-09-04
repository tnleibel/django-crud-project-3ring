from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Card(models.Model):
    name = models.CharField(max_length=100)
    supertype = models.CharField(max_length=50)
    types = models.CharField(max_length=25)
    set = models.CharField(max_length=50)
    rarity = models.CharField(max_length=25)
    image = models.CharField(max_length=100)
    is_owned = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('card-detail', kwargs={ 'card_id': self.id })
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_binder = models.ManyToManyField(Card)
    favorite_cards = models.ManyToManyField(Card)

    def __str__(self):
        return self.user.username

