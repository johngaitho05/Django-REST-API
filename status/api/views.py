import json
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics, mixins, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .utils import is_json
from status.models import Status
from rest_framework.response import Response
from .serializers import StatusSerializer

"""
Using separate endpoints for ListView and DetailView
efficient when you want your API to support file uploads

You can also use mixins such as CreateModelMixin  to customize
the operations that can be performed at the ListView endpoint
"""


class StatusAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    '''Modifying the ListView to supporting Searching by overwriting the get_queryset method'''

    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('keyword')
        if query is not None:
            qs = qs.filter(content__contains=query)
        return qs

    def perform_create(self, serializer):
        if serializer is not None:
            return serializer.save(user=self.request.user)
        return


"""
you can also use mixins such as UpdateModelMixin and DestroyModelMixin to customize
the operations that can be performed at the DetailView endpoint
"""


class StatusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    lookup_url_kwarg = 'id'

    def perform_update(self, serializer):
        if serializer is not None:
            return serializer.save(user=self.request.user)
        return


"""
One endpoint for all CRUD operations
efficient when we don't have file uploads
"""


class StatusGeneralAPIView(
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.ListAPIView,
):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = StatusSerializer
    passed_id = None

    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('keyword')
        if query is not None:
            qs = qs.filter(content__contains=query)
        return qs

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None

    def get_object(self):
        request = self.request
        passed_id = request.GET.get("id", None) or self.passed_id
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        if not passed_id and is_json(request.body):
            json_data = json.loads(request.body)
            passed_id = json_data.get('id', None)
        self.passed_id = passed_id
        if passed_id:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        if not passed_id and is_json(request.body):
            json_data = json.loads(request.body)
            passed_id = json_data.get('id', None)
        self.passed_id = passed_id
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        if not passed_id and is_json(request.body):
            json_data = json.loads(request.body)
            passed_id = json_data.get('id', None)
        self.passed_id = passed_id
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        if not passed_id and is_json(request.body):
            json_data = json.loads(request.body)
            passed_id = json_data.get('id', None)
        self.passed_id = passed_id
        return self.destroy(request, *args, **kwargs)
