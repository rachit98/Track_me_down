from django.db import models
from .utils import get_link_data
# Create your models here.

class Link(models.Model):
    name = models.CharField(max_length=220,blank=True)
    url = models.URLField()
    phno = models.CharField(max_length=13,blank=True)
    mail = models.EmailField(max_length=250,blank=True)
    trigger = models.FloatField(blank=True,default=0)
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    rating = models.CharField(max_length=20,blank=True)
    total = models.IntegerField(blank=True,default=0)
    negative = models.IntegerField(blank=True,default=0)
    positive = models.IntegerField(blank=True,default=0)
    neutral = models.IntegerField(blank=True,default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('price_difference','-created')

    def save(self,*args,**kwargs):
        name, price, rating, total, negative, positive, neutral  = get_link_data(self.url)
        #print(rating)
        old_price = self.current_price
        if self.current_price:
            if price!=old_price:
                diff = price - old_price
                self.price_difference = round(diff,2)
                self.old_price = old_price
               
        else:
            self.old_price = 0
            self.price_difference = 0
        
        self.name = name
        self.current_price = price
        self.rating = rating
        self.total = total
        self.negative = negative
        self.positive = positive
        self.neutral = neutral
        #self.top_reviews = top_reviews
        
        super().save(*args,**kwargs)