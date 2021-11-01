from django import forms
from django.db import models
from django.forms import fields
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = ['first_name', 'last_name', 'phone_number', 'email',
                  'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_notes', 'postal_code']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'House number and street name'
        self.fields['address_line_2'].widget.attrs[
            'placeholder'] = 'Apartment, suite, unit, etc. (optional)'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter State'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'Enter Postal Code'
        self.fields['order_notes'].widget.attrs = {
            'placeholder': 'Notes about your order e.g. special notes for delivery',
            'rows': '4'
        }
        # this class name applies to every field of the given registration form
        for field in self.fields:
            if field == 'address_line_2':
                self.fields[field].widget.attrs['class'] = 'mt-2 py-1 px-2 bg-transparent border border-secondary2 rounded-md placeholder-secondary2 outline-none'
            else:
                self.fields[field].widget.attrs['class'] = 'py-1 px-2 bg-transparent border border-secondary2 rounded-md placeholder-secondary2 outline-none'
