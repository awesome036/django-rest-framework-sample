from django.shortcuts import render

# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .models import User, Entry
from .serializer import UserSerializer, EntrySerializer, HistorySerializer # 追加しました

# FilterSetを継承したフィルタセット(設定クラス)を作る
class EntryFilter(filters.FilterSet):
    class Meta:
      model = Entry
      fields = ['author', 'title', 'status']

    def get_authors(self, queryset, name, value):
        author_str = value.strip("[""]")
        authors = author_str.split(",")
        return queryset.filter(author__in=authors)

    # フィルタの定義
    author = filters.CharFilter(method='get_authors')
    title = filters.CharFilter(lookup_expr='contains')
    status = filters.CharFilter(lookup_expr='exact') # ENUM型はcharでfilterする


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_class = EntryFilter

    # 追加しました
    @action(detail=False, methods=['get'])
    def history(self, request, pk=None):
        serializer = HistorySerializer(data=request.GET)

        if serializer.is_valid():
          queryset_filter = EntryFilter(serializer.data, queryset=Entry.objects.all())
          total_qs = queryset_filter.qs.count()
          history = EntrySerializer(queryset_filter.qs, many=True)

          data = {
            "messages": history.data,
            "total": total_qs
          }

          return Response(data, status=status.HTTP_200_OK)

        else:
          data = {
              "error_code": 4001,
              "error_message": "Invalid request",
              "validation": [
                serializer.errors
              ] 
          }

          return Response(data, status=status.HTTP_400_BAD_REQUEST)
