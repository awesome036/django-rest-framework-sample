# coding: utf-8

from rest_framework import serializers
from django.core.validators import RegexValidator # 追加しました

from .models import User, Entry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'mail')


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('title', 'body', 'created_at', 'status', 'author')

# 追加しました
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('author', 'status')
    
    author_array_regex = RegexValidator(
      regex=r'^\[([0-9],?)+\]$',
      message = ("Sender id must be entered in the format: '[1,2,3]'.")
    )
    author = serializers.CharField(validators=[author_array_regex])