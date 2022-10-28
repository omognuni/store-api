from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from core.models import Item

from item import serializers
from item.permissions import ReadOnly

class ItemViewSet(viewsets.ModelViewSet):
    '''Item API View'''
    serializer_class = serializers.ItemSerializer
    queryset = Item.objects.all()
    authenitcation_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser | ReadOnly]
    