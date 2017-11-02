from django.db import models

# Create your models here.
class Auction(models.Model):

    title = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.PositiveIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Competitor(models.Model):

    auction = models.ForeignKey(Auction)
    bid = models.PositiveIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bid)

