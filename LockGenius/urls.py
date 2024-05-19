from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from UnLock import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('UnLock/', include('UnLock.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
]




