from django.urls import path, include

urlpatterns = [
    path('api/', include('status.api.urls')),
]