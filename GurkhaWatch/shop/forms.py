from django import forms
from .models import ReviewRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']


class AddToCart(forms.Form):
    add_to_cart = forms.IntegerField()

    def __init__(self, site_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['add_to_cart'] = forms.IntegerField(widget=forms.NumberInput(
            attrs={'class': 'py-1 font-bold text-sm text-center bg-secondary text-primary outline-none rounded-md transition-all duration-200'}))
        self.fields['add_to_cart'] = forms.IntegerField(widget=forms.NumberInput(
            attrs={'id': 'item-cart-count'}))
        self.fields['add_to_cart'] = forms.IntegerField(widget=forms.NumberInput(
            attrs={'type': 'number'}))
        self.fields['add_to_cart'] = forms.IntegerField(widget=forms.NumberInput(
            attrs={'step': '1'}))
        self.fields['add_to_cart'] = forms.IntegerField(widget=forms.NumberInput(
            attrs={'value': '1'}))
