from django.views import generic, View
from django.shortcuts import render, redirect
from .models import Locked, Review, PricePerKm
from django import forms
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import RegisterForm
from django.urls import reverse_lazy
from .forms import ReviewFormStep2, ReviewFormStep1, ServiceRequestForm, ContactForm
from django.db.models import Avg

def index(request):

    return render(request, "index.html")


class OpenCar(generic.ListView):
    model = Locked
    template_name = 'UnLock/open_car.html'


class OpenDoor(generic.ListView):
    model = Locked
    template_name = 'UnLock/open_door.html'


class OpenGarage(generic.ListView):
    model = Locked
    template_name = 'UnLock/open_garage.html'


class OpenSafe(generic.ListView):
    model = Locked
    template_name = 'UnLock/open_safe.html'


class Replace(generic.ListView):
    model = Locked
    template_name = 'UnLock/replace.html'


class Installation(generic.ListView):
    model = Locked
    template_name = 'UnLock/installation.html'


class Repair(generic.ListView):
    model = Locked
    template_name = 'UnLock/repair.html'


class PriceAll(generic.ListView):
    model = Locked
    template_name = 'UnLock/price_all.html'


class Lock(generic.ListView):
    model = Locked
    template_name = 'UnLock/lock.html'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['lock_object', 'service','character', 'rating', 'comment']
        widgets = {
            'lock_object': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'character': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CreateReview(View):
    def get(self, request):
        if 'lock_object' in request.GET and 'service' in request.GET:
            form = ReviewFormStep2()
            form.fields['character'].queryset = Locked.objects.filter(lock_object=request.GET['lock_object'], service=request.GET['service'])
        else:
            form = ReviewFormStep1()
        return render(request, 'UnLock/create_review.html', {'form': form})

    def post(self, request):
        form = ReviewFormStep2(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')
        return render(request, 'UnLock/create_review.html', {'form': form})


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'UnLock/review_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Review.objects.annotate(avg_rating=Avg('rating')).select_related('user')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('home')


def service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            quantity = form.cleaned_data['quantity']
            distance = form.cleaned_data['distance']

            price_per_km_obj = PricePerKm.objects.first()
            if price_per_km_obj is not None:
                price_per_km = price_per_km_obj.price
            else:
                price_per_km = 0
            service_price = service.price * quantity
            distance_price = price_per_km * distance
            total_price = service_price + distance_price

            return render(request, 'UnLock/service_request.html', {'form': form, 'service_price': service_price, 'distance_price': distance_price, 'total_price': total_price})

    else:
        form = ServiceRequestForm()
    return render(request, 'UnLock/service_request.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
           return render(request, 'UnLock/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'UnLock/contact.html', {'form': form})


class AboutUsView(generic.TemplateView):
    model = Locked
    template_name = 'UnLock/about_us.html'