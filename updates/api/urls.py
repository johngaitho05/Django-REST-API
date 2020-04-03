from django.urls import path, include
from .views import (
    UpdateModelAPIListView
    # UpdateModelAPIDetailView
)

urlpatterns = [
    path('', UpdateModelAPIListView.as_view()),
    # path('<int:id>', UpdateModelAPIDetailView.as_view())
]
