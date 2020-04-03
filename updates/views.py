import json
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from apiproject.mixins import JSonResponseMixin
from .models import Update
from django.views.generic import View


def json_exmle_view(request):
    data = {
        "count": 1000,
        "content": "this is the content"
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        data = Update.objects.get(id=1).serialize()
        return HttpResponse(data, content_type='application/json')


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        data = Update.objects.all().serialize()
        return HttpResponse(data, content_type='application/json')