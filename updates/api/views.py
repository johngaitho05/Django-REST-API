import json
from .utils import is_json
from updates.api.mixins import CSRFExemptMixin
from apiproject.mixins import HttpResponseMixin
from django.views.generic import View
from django.http import HttpResponse
from updates.models import Update as UpdateModel
from updates.forms import UpdateModelForm


# def get_object(id=None):
#     qs = UpdateModel.objects.filter(id=id)
#     if qs.count() == 1:
#         return qs.first()
#     return None
#
#
# class UpdateModelAPIDetailView(HttpResponseMixin, CSRFExemptMixin, View):
#
#     def get(self, request, id, *args, **kwargs):
#         obj = get_object(id)  # checks if the object with the passed Id exists
#         if obj is None:
#             error_data = json.dumps({"message": "Update not found"})
#             return self.render_to_response(error_data, status=404)
#         json_data = obj.serialize()
#         return HttpResponse(json_data, content_type="application/json")
#
#     def post(self, request, id, *args, **kwargs):
#         json_data = json.dumps({"Message": "Not allowed, please use 'api/updates/' endpoint"})
#         return self.render_to_response(json_data, status=403)
#
#     def put(self, request, id, *args, **kwargs):
#         obj = get_object(id)
#
#         if obj is None:
#             error_data = json.dumps({"message": "Update not found"})
#             return self.render_to_response(error_data, status=404)
#         old_obj = json.loads(obj.serialize())
#         if is_json(request.body):
#             new_obj = json.loads(request.body)
#             for key in new_obj.keys():
#                 if key in old_obj:
#                     old_obj[key] = new_obj[key]
#             form = UpdateModelForm(old_obj)
#             if form.is_valid():
#                 form.save(commit=True)
#                 obj_data = json.dumps(old_obj)
#                 return self.render_to_response(obj_data, status=201)
#             if form.errors:
#                 data = json.dumps(form.errors)
#                 return self.render_to_response(data, status=400)
#             data = {"Message": "Not allowed"}
#             return self.render_to_response(data, status=406)
#         error_message = json.dumps({"message": "Invalid data sent. Please send valid JSON data"})
#         return self.render_to_response(error_message,status=400)
#
#     def delete(self, request, id, *args, **kwargs):
#         obj = get_object(id)
#         if obj is None:
#             error_data = json.dumps({"message": "Update not found"})
#             return self.render_to_response(error_data, status=404)
#         obj.delete()
#         message = json.dumps({"message": "Success. One item deleted."})
#         return self.render_to_response(message)


class UpdateModelAPIListView(HttpResponseMixin, CSRFExemptMixin, View):
    # All CRUD operations being performed at one ENDPOINT ('api/updates/')

    is_json = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queryset = UpdateModel.objects.all()

    def get_object(self, id=None):
        if id is None:
            return
        qs = self.queryset.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        passed_id = data.get('id', None)
        if passed_id:
            obj = self.get_object(id=passed_id)  # checks if the object with the passed Id exists
            if obj is None:
                error_data = json.dumps({"message": "Object not found"})
                return self.render_to_response(error_data, status=404)
            json_data = obj.serialize()
            return HttpResponse(json_data, content_type="application/json")
        data = self.queryset.serialize()
        return self.render_to_response(data)

    def post(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_message = json.dumps({"message": "Invalid data sent. Please send valid JSON data"})
            return self.render_to_response(error_message, status=400)
        data = json.loads(request.body)
        form  = UpdateModelForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = {"Message": "Not allowed"}
        return self.render_to_response(data, status=406)

    def put(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_message = json.dumps({"message": "Invalid data sent. Please send valid JSON data"})
            return self.render_to_response(error_message, status=400)
        new_obj = json.loads(request.body)
        passed_id = new_obj.get('id', None)
        if not passed_id:
            error_message = json.dumps({"id":"This field is required to update an item"})
            return self.render_to_response(error_message, status=400)
        obj = self.get_object(id=passed_id)
        if obj is None:
            error_data = json.dumps({"message": "Object not found"})
            return self.render_to_response(error_data, status=404)
        old_obj = json.loads(obj.serialize())
        if is_json(request.body):
            for key in new_obj.keys():
                if key in old_obj:
                    old_obj[key] = new_obj[key]
            form = UpdateModelForm(old_obj)
            if form.is_valid():
                form.save(commit=True)
                obj_data = json.dumps(old_obj)
                return self.render_to_response(obj_data, status=201)
            if form.errors:
                data = json.dumps(form.errors)
                return self.render_to_response(data, status=400)
            data = {"Message": "Not allowed"}
            return self.render_to_response(data, status=406)
        error_message = json.dumps({"message": "Invalid data sent. Please send valid JSON data"})
        return self.render_to_response(error_message, status=400)

    def delete(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_message = json.dumps({"message": "Invalid data sent. Please send valid JSON data"})
            return self.render_to_response(error_message, status=400)
        data = json.loads(request.body)
        passed_id = data.get('id')
        if not passed_id:
            error_message = json.dumps({"id": "This field is required to delete an item "})
            return self.render_to_response(error_message, status=400)
        to_delete = self.get_object(id=passed_id)
        if not to_delete:
            error_data = json.dumps({"message": "Object not found"})
            return self.render_to_response(error_data, status=404)
        to_delete.delete()
        message = json.dumps({"message": "Success. One item deleted."})
        return self.render_to_response(message)










