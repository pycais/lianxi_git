from django.contrib.auth.models import User
from rest_framework import serializers
from .models import VideoStatus


class VideoClippingStatus(serializers.Serializer):
    video_name = serializers.CharField(required=True, max_length=500)
    video_name2 = serializers.CharField(required=False, max_length=50, allow_null=True)
    file_path = serializers.CharField(required=True, max_length=100)
    file_path2 = serializers.CharField(required=False, max_length=100, allow_null=True)
    task_id = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.CharField(required=False, max_length=50, allow_null=True)
    result = serializers.CharField(required=False, max_length=500, allow_null=True)
    runtime = serializers.FloatField(required=False, allow_null=True)
    traceback = serializers.CharField(required=False, max_length=1000, allow_null=True)
    children = serializers.CharField(required=False, max_length=500, allow_null=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return VideoStatus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.video_name = validated_data.get('video_name', instance.video_name)
        instance.video_name2 = validated_data.get('video_name2', instance.video_name2)
        instance.file_path = validated_data.get('file_path', instance.file_path)
        instance.file_path2 = validated_data.get('file_path2', instance.file_path2)
        instance.task_id = validated_data.get('task_id', instance.task_id)
        instance.status = validated_data.get('status', instance.status)
        instance.result = validated_data.get('result', instance.result)
        instance.runtime = validated_data.get('runtime', instance.runtime)
        instance.traceback = validated_data.get('traceback', instance.traceback)
        instance.children = validated_data.get('children', instance.children)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.update_time = validated_data.get('update_time', instance.update_time)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
