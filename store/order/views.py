from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Order

from order.permissions import IsAdminOrCRUOnly
from order import serializers

class OrderViewSet(viewsets.ModelViewSet):
    '''Order API View'''
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    authenitcation_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrCRUOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)