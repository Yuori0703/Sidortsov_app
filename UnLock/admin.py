from django.contrib import admin
from .models import Locked, Review, PricePerKm


@admin.register(Locked)
class LockedAdmin(admin.ModelAdmin):
    list_display = ['lock_object', 'service', 'character', 'price']
    list_filter = ['lock_object', 'service', 'character', 'price']
    search_fields = ['lock_object', 'service']
    prepopulated_fields = {'character': ('lock_object',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'character', 'rating', 'comment']
    list_filter = ['user', 'character', 'rating']
    search_fields = ['user__username', 'character__lock_object', 'comment']


admin.site.register(PricePerKm)