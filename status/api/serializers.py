from rest_framework import serializers
from status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id','content', 'image']

    @staticmethod
    def validate_content(value):
        if len(value) > 240:
            raise serializers.ValidationError("Content is too long")
        return value

    def validate(self, data):
        content = data.get('content', None)
        if content == "":
            content = None
        image = data.get('image', None)
        if content is None and image is None:
            raise serializers.ValidationError("Content or image is required.")
        return data
