from rest_framework import serializers

from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id', 'item', 'created_at', 'total_price','quantity','status']
        read_only_fields = ['id', 'created_at', 'total_price']