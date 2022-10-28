from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication

from core.models import Order, Item

from order.permissions import IsAdminOrCRUOnly
from order import serializers

class OrderViewSet(viewsets.ModelViewSet):
    '''Order API View'''
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    authenitcation_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrCRUOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    
    def perform_create(self, serializer):
        '''주문을 생성한 사용자 저장'''
        validated_data = serializer.validated_data
        price = validated_data['item'].price
        total_price = price * validated_data['quantity']

        serializer.save(user=self.request.user, total_price=total_price)
        
    def get_queryset(self):
        '''이용자와 관리자 queryset 분리'''
        if self.request.user.is_staff:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(user=self.request.user.id)
        return queryset
            