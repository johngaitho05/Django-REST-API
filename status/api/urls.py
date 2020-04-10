from django.urls import path
from .views import *

urlpatterns = [
    path('', StatusGeneralAPIView.as_view()),
    path('list', StatusAPIView.as_view()),
    path('<int:id>', StatusDetailAPIView.as_view()),

]
