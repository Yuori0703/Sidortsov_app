from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Locked, Review, PricePerKm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот адрес электронной почты уже используется.")
        return email


class ReviewFormStep1(forms.Form):
    lock_object = forms.ChoiceField(choices=Locked.AVAILABLE_LOCK_OBJECT)
    service = forms.ChoiceField(choices=Locked.AVAILABLE_SERVICE)


class ReviewFormStep2(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['character', 'rating', 'comment']


class ServiceRequestForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Locked.objects.all(), label='Услуга')
    quantity = forms.IntegerField(min_value=1, label='Количество')
    distance = forms.IntegerField(min_value=0, label='Расстояние от города (в км)')


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)