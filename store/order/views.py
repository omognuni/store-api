from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

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
        '''주문을 생성한 사용자 저장'''
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        '''이용자와 관리자 queryset 분리'''
        if self.request.user.is_staff:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(user=self.request.user.id)
        return queryset
            