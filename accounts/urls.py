from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import login_view

urlpatterns = [
    path('login', login_view),

]