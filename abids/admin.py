from django.contrib import admin

# Register your models here.
from abids.models import Auction, Competitor

admin.site.register(Auction)
admin.site.register(Competitor)
