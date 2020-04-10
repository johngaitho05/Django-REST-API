from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.json_exmle_view),
    path("cbdv",views.SerializedDetailView.as_view()),
    path("cblv",views.SerializedListView.as_view()),
    path('api/', include('updates.api.urls')),

]