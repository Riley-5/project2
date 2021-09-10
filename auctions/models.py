from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = (
        ('H', 'Home'),
        ('G', 'Garden'),
        ('S', 'Sport'),
        ('T', 'Toy'),
        ('E', 'Electronics'),
        ('F', 'Fashion')
    )

    title = models.CharField(max_length = 255)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    image_url = models.URLField(blank= True, null = True)
    category = models.CharField(max_length = 1, choices = CATEGORIES)
    active = models.BooleanField(default = True)
    on_watchlist = models.BooleanField(default = False)

    def __str__(self):
        return self.title + " | " + str(self.owner)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.listing.title + " | " + self.body

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bids")
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    bid = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return str(self.owner) + ": " + str(self.bid)

class Watchlist(models.Model):
    listing = models.ManyToManyField(Listing)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{str(self.user)}'s watchlist"