from django.shortcuts import render

# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Entry
from .serializer import UserSerializer, EntrySerializer

# FilterSetを継承したフィルタセット(設定クラス)を作る
class EntryFilter(filters.FilterSet):

    def get_authors(self, queryset, name, value):
        author_str = value.strip("[""]")
        authors = author_str.split(",")
        print(authors)
        return queryset.filter(author__in=authors)

    # フィルタの定義
    author = filters.CharFilter(method='get_authors')
    title = filters.CharFilter(lookup_expr='contains')
    status = filters.NumberFilter(lookup_expr='exact')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_class = EntryFilter

class EntryList(APIView):
    def get(self, request):
        entry = Entry.objects.all()
        filter_class = EntryFilter
        serializer = EntrySerializer(entry, many=True)
        return Response({"messages": serializer.data}, status=status.HTTP_200_OK)

    def post(self):
        pass