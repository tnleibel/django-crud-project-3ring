from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='Search for a card here...', max_length=100)