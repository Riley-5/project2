from django import forms
from .models import *
from django.forms import TextInput, NumberInput, URLInput, ChoiceField, Select

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"
        exclude = ['active', 'owner', 'on_watchlist']
        category = forms.ChoiceField(choices = Listing.CATEGORIES)
        widgets = {
            'title': TextInput(attrs = {
                'class': "form-control",
                'placeholder': "Broom"
            }),
            
            'description': TextInput(attrs = {
                'class': "form-control",
                'placeholder': "The Ultimate Sweeper"
            }),

            'starting_price': NumberInput(attrs = {
                'class': "form-control",
                'placeholder': "$5.00"
            }),

            'image_url': URLInput(attrs = {
                'class': "form-control",
                'placeholder': "image.com"
            }),

            'category': Select(attrs = {
                'class': "form-control"
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['owner', 'listing']
        labels = {
            'body': ""
        }
        widgets = {
            'body': TextInput(attrs = {
                'placeholder': "Comment Here"
            })
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        exclude = ['owner', 'listing']
        labels = {
            'bid': ""
        }
        widgets = {
            'bid': NumberInput(attrs = {
                'placeholder': "Bid Here: $$"
            })
        }