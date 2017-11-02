from django import forms
from abids.models import Auction, Competitor

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'desc', 'price']
        labels = {'title': '', 'desc': '', 'price': ''}

class CompetitorForm(forms.ModelForm):
    class Meta:
        model = Competitor
        fields = ['bid']
        labels = {'bid': ''}
