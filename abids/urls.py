from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^auctions$', views.auctions, name='auctions'),
        url(r'^auction/(?P<auction_id>\d+)/$', views.auction, name='auction'),
        
        url(r'^new_auction$', views.new_auction, name='new_auction'),
        url(r'^edit_auction(?P<auction_id>\d+)/$', views.edit_auction, name='edit_auction'),

        
        ]
