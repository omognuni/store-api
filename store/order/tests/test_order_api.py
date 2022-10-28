from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from datetime import datetime

from core.models import Order, Item
from order.serializers import OrderSerializer


'''
Public은 X
Private
    - User는  CRU
    - Staff는 CRUD
'''

ORDER_URL = reverse('order:order-list')

def detail_url(order_id):
    return reverse('order:order-detail', args=[order_id])

def create_item(**params):
    defaults = {
        'name': 'Sample Item',
        'price': 1000,
        'description': 'sample item'
    }
    
    defaults.update(**params)
    
    item = Item.objects.create(**defaults)
    return item

def create_order(user, **params):
    item = create_item()
    
    defaults = {
        'item': item,
        'quantity':1,
        'status': 'pending'
    }
    defaults.update(**params)
    return Order.objects.create(user=user,  **defaults)

class PrivateAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(self.user)        
   
    def test_retrieve_order_created_by_user(self):
        ''' 이용자가 만든 order만 가져오기'''
        create_order(user=self.user)
        create_order(user=self.user)
        new_user = get_user_model().objects.create_user(username='testuser2', password='testpass')
        create_order(user=new_user)
        create_order(user=new_user)
        
        res = self.client.get(ORDER_URL)
        
        orders = Order.objects.filter(user=self.user.id)
        serializer = OrderSerializer(orders, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
    
    def test_retrieve_all_order_by_staff(self):
        '''관리자로 모든 Order 목록 가져오기'''
        self.user.is_staff = True
        self.user.save()
        
        create_order(user=self.user)
        create_order(user=self.user)
        new_user = get_user_model().objects.create_user(username='testuser2', password='testpass')
        create_order(user=new_user)
        create_order(user=new_user)
        
        res = self.client.get(ORDER_URL)
        
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
        self.assertEqual(res.data, serializer.data)
        
    def test_create_order_by_staff(self):
        '''관리자로 Order 생성'''
        self.user.is_staff = True
        self.user.save()
        
        item = create_item()
        payload = {
            'item': item.id,
            'quantity': 2,
            'status': 'pending',
        }
        
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data['id'])

        for k,v in payload.items():
            if k == 'item':
                self.assertEqual(getattr(order,k), item)
            else:
                self.assertEqual(getattr(order, k), v)
        
    def test_create_order_by_user(self):
        '''이용자로 Order 생성'''
        item = create_item()
        
        payload = {
            'item': item.id,
            'quantity': 2,
            'status': 'pending',
        }
        
        res = self.client.post(ORDER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        order = Order.objects.get(id=res.data['id'])
        for k,v in payload.items():
            if k == 'item':
                self.assertEqual(getattr(order,k), item)
            else:
                self.assertEqual(getattr(order, k), v)
    
    def test_partial_update_item_by_staff(self):
        '''관리자로 Order 부분 업데이트'''
        self.user.is_staff = True
        self.user.save()
        
        item = create_item()
        order = create_order(user=self.user, item=item)
        orig_item = order.item
        orig_quantity = order.quantity
        
        payload = {
            'status': 'complete',
        }
        
        url = detail_url(order.id)
        res = self.client.patch(url, payload)
        
        order.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(orig_item, order.item)
        self.assertEqual(orig_quantity, order.quantity)
        self.assertEqual(order.status, payload['status'])
    
    def test_partial_update_item_by_user(self):
        '''이용자로 Order 부분 업데이트'''
        item = create_item()
        order = create_order(user=self.user, item=item)
        orig_item = order.item
        orig_quantity = order.quantity
        
        payload = {
            'status': 'complete',
        }
        
        url = detail_url(order.id)
        res = self.client.patch(url, payload)
        
        order.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(orig_item, order.item)
        self.assertEqual(orig_quantity, order.quantity)
        self.assertEqual(order.status, payload['status'])
    
    def test_full_update_item_by_staff(self):
        '''관리자로 Order 전체 업데이트'''
        self.user.is_staff = True
        self.user.save()
        
        item = create_item()
        order = create_order(user=self.user, item=item)
        new_item = create_item()
        payload = {
            'item': new_item.id,
            'quantity': 4,            
            'status': 'complete',
        }
        
        url = detail_url(order.id)
        res = self.client.patch(url, payload)
        
        order.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        for k,v in payload.items():
            if k == 'item':
                self.assertEqual(getattr(order,k), new_item)
            else:
                self.assertEqual(getattr(order, k), v)
    
    def test_full_update_by_user(self):
        '''이용자로 Order 전체 업데이트'''
        item = create_item()
        order = create_order(user=self.user, item=item)
        new_item = create_item()
        payload = {
            'item': new_item.id,
            'quantity': 4,            
            'status': 'complete',
        }
        
        url = detail_url(order.id)
        res = self.client.patch(url, payload)
        
        order.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        for k,v in payload.items():
            if k == 'item':
                self.assertEqual(getattr(order,k), new_item)
            else:
                self.assertEqual(getattr(order, k), v)
    
    def test_delete_item_by_staff(self):
        '''관리자로 Order 삭제'''
        self.user.is_staff = True
        self.user.save()
        
        order = create_order(user=self.user)
        
        url = detail_url(order.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_item_by_user_invalid(self):
        '''이용자로 Order 삭제 시 오류'''
        order = create_order(user=self.user)
        
        url = detail_url(order.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)