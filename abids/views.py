from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from abids.models import Auction, Competitor
from abids.forms import AuctionForm, CompetitorForm

# Create your views here.

def index(request):
    """домашняя страница"""
    return render(request, 'abids/index.html')

def auctions(request):
    """список всех аукционов"""
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'abids/auctions.html', context)


def new_auction(request):
    """создание нового объявления"""
    if request.method != 'POST':
        #данные не отправлялись, создается пустая форма
        form = AuctionForm()

    else:
        #отправленные данные POST; обработать данные
        form = AuctionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('abids:auctions'))

    context = {'form': form}
    return render(request, 'abids/new_auction.html', context)

def auction(request, auction_id):
    """выводит отдельный аукцион и принимает ставки"""
    auction = Auction.objects.get(id=auction_id)
    bids = auction.competitor_set.all().order_by('pub_date')


    if request.method != 'POST':
        form = CompetitorForm()

    else:
        #отправленные данные POST; обрабатываем
        form = CompetitorForm(data=request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.auction = auction
            new_bid.save()
            return HttpResponseRedirect(reverse('abids:auction', args=[auction_id]))

    context = {'auction': auction, 'bids': bids, 'form': form}
    return render(request, 'abids/auction.html', context)
