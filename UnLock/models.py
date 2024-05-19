from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Locked(models.Model):
    AVAILABLE_LOCK_OBJECT = (
        ('car', 'авто'),
        ('door', 'дверь'),
        ('garage', 'гараж'),
        ('safe', 'сейф'),
        ('door_lock', 'дверной замок'),
    )
    lock_object = models.CharField(max_length=20, choices=AVAILABLE_LOCK_OBJECT, blank=True, default='door_lock', help_text='Вид объекта')
    AVAILABLE_SERVICE = (
        ('replace', 'замена'),
        ('repair', 'ремонт'),
        ('open_lock', 'вскрытие'),
        ('install', 'установка'),
        ('hacking', 'взлом'),
        ('additional_services', 'дополнительные услуги'),
        ('repair_dop', 'доп-ремонт'),
    )
    service = models.CharField(max_length = 25, choices=AVAILABLE_SERVICE, blank= True, help_text = 'Вид услуги')
    character = models.TextField(verbose_name = "Услуга", help_text="Введите услугу")
    price = models.IntegerField( default = '7',)
    price_per_km = models.DecimalField(max_digits=6, decimal_places=2, default = '1')


    class Meta:
        ordering = ["lock_object"]
        indexes = [
        models.Index(fields=['lock_object']),
        ]

    def __str__(self):

        return f'({self.lock_object} : {self.character})'

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])


class PricePerKm(models.Model):
    price = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f'Цена за километр: {self.price} рублей'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lock_object = models.CharField(max_length=20, choices=Locked.AVAILABLE_LOCK_OBJECT, blank=True, default='door_lock', help_text='Вид объекта')
    service = models.CharField(max_length=25, choices=Locked.AVAILABLE_SERVICE, blank=True, help_text='Вид услуги')
    character = models.ForeignKey(Locked, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text = "Введите оценку от 1 до 5")
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.lock_object} - {self.service} - {self.rating}'


