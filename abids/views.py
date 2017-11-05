from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


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

def top_prices(request):
    top_prices = Auction.objects.order_by('-price')
    return render(request, 'abids/top_prices.html', {'top_prices': top_prices})

def top_bids(request):
    """выводит список самых популярных аукционов"""
    #создает словарь для id : len(bid)
    hardcore = {}
    # словарь для id : title
    hall_of_fame = {}
    auctions = Auction.objects.all()

    for auction in auctions:
        bids = auction.competitor_set.all()
        hardcore[auction.id] = len(bids)
    
    for k_auction_id, bids in sorted(hardcore.items(), key=lambda x: x[1], reverse=True):
        auction = Auction.objects.get(id=k_auction_id)
        hall_of_fame[k_auction_id] = auction.title

    #return HttpResponse(hall_of_fame)

    return render(request, 'abids/top_bids.html', {'hall_of_fame': hall_of_fame})

@login_required
def new_auction(request):
    """создание нового объявления"""
    #получаем id последней темы
    last_auction = Auction.objects.latest('id')
    last_auction.id += 1
    #отправленные данные POST; обработать данные
    if request.method == 'POST':
        form = AuctionForm(request.POST)

        if form.is_valid():
            new_auction = form.save(commit=False)
            # присваеваем запись пользователю
            new_auction.owner = request.user
            new_auction.save()
            return HttpResponseRedirect(reverse('abids:auction', args=[last_auction.id]))
    else:
        #данные не отправлялись, создается пустая форма
        form = AuctionForm()

    context = {'form': form}
    return render(request, 'abids/new_auction.html', context)



def edit_auction(request, auction_id):
    """редактирование аукциона"""
    auction = Auction.objects.get(id=auction_id)

    # проверка что редактируемая тема принадлежит ее создателю
    if auction.owner != request.user:
        raise Http404

    # отправка данных POST; обработать данные
    if request.method == 'POST':
        form = AuctionForm(instance=auction, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('abids:auction', args=[auction_id]))

    # исходный запрос; форма заполняется данными текущей записи
    else:
        form = AuctionForm(instance=auction)

    context = {'auction': auction, 'form': form}
    return render(request, 'abids/edit_auction.html', context)





def auction(request, auction_id):
    """выводит отдельный аукцион и принимает ставки"""
    auction = Auction.objects.get(id=auction_id)
    bids = auction.competitor_set.all().order_by('pub_date')

    # получаем последнюю ставку 
    # если не было ставок, то ставка это начальная цена
    if bids:
        last_bid = bids.last()
        last_bid = last_bid.bid
    else:
        last_bid = auction.price

    bid_step = last_bid - 1
    is_success = ''
        
    #проверяем POST
    if request.method != 'POST':
        form = CompetitorForm()

    else:
        #отправленные данные POST; обрабатываем
        form = CompetitorForm(data=request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)

            #проверяем что ставка меньше предыдущей
            if (new_bid.bid < last_bid) and (new_bid.bid > 0):

                new_bid.auction = auction
                new_bid.bid_owner = request.user
                new_bid.save()
                return HttpResponseRedirect(reverse('abids:auction', args=[auction_id]))
            else:
                form = CompetitorForm()
                is_success = "ставка не может быть больше: " + str(bid_step) + " либо меньше 1."

    context = {'auction': auction, 'bids': bids, 'form': form, 'bid_step': bid_step, 'is_success': is_success}
    return render(request, 'abids/auction.html', context)

