from rest_framework import serializers
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):

    users_liked = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'creator', 'users_liked']
        extra_kwargs = {
            'users_liked': {'read_only': True}
        }
