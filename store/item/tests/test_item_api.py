from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Item
from item.serializers import ItemSerializer


'''
Public은 상품-R
Private
    - User는 상품은 R
    - Staff는 CRUD
'''

ITEM_URL = reverse('item:item-list')

def detail_url(item_id):
    return reverse('item:item-detail', args=[item_id])

def create_item(**params):
    defaults = {
        'name': 'Sample Item',
        'price': 1000,
        'description': 'sample item'
    }
    
    defaults.update(**params)
    
    item = Item.objects.create(**defaults)
    return item

class PublicAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
    def test_retrieve_item(self):
        '''Item 목록 가져오기'''
        create_item()
        create_item()
        
        res = self.client.get(ITEM_URL)
        
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        

class PrivateAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(self.user)        
   
    def test_retrieve_item(self):
        '''Item 목록 가져오기'''
        create_item()
        create_item()
        
        res = self.client.get(ITEM_URL)
        
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)    
    
    def test_create_item_by_staff(self):
        '''관리자로 Item 생성'''
        self.user.is_staff = True
        self.user.save()
        
        payload = {
            'name': 'Sample item',
            'price': 1000,
            'description': 'Sample'
        }
        
        res = self.client.post(ITEM_URL, payload)
        item = Item.objects.get(id=res.data['id'])
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for k,v in payload.items():
            self.assertEqual(getattr(item, k), v)
        
    def test_create_item_by_user_invalid(self):
        '''이용자로 Item 생성 시 오류'''
        payload = {
            'name': 'Sample item',
            'price': 1000,
            'description': 'Sample'
        }
        
        res = self.client.post(ITEM_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_partial_update_item_by_staff(self):
        '''관리자로 Item 부분 업데이트'''
        self.user.is_staff = True
        self.user.save()
        
        item = create_item()
        orig_name = item.name
        orig_desc = item.description
        
        payload = {
            'price': 2000,
        }
        
        url = detail_url(item.id)
        res = self.client.patch(url, payload)
        
        item.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(item.price, payload['price'])
        self.assertEqual(item.name, orig_name)
        self.assertEqual(item.description, orig_desc)

    
    def test_partial_update_item_by_user_invalid(self):
        '''이용자로 Item 부분 업데이트 시 오류'''
        item = create_item()
        orig_price = item.price
        
        payload = {
            'price': 2000,
        }
        
        url = detail_url(item.id)
        res = self.client.patch(url, payload)
        
        item.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(item.price, orig_price)
    
    def test_full_update_item_by_staff(self):
        '''관리자로 Item 전체 업데이트'''
        self.user.is_staff = True
        self.user.save()
        
        item = create_item()
        
        payload = {
            'name': 'Sample item 2',
            'price': 20000,
            'description': 'sample description 2'
        }
        
        url = detail_url(item.id)
        res = self.client.put(url, payload)
        
        item.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        for k,v in payload.items():
            self.assertEqual(getattr(item, k), v)
    
    def test_full_update_by_user_invalid(self):
        '''이용자로 Item 전체 업데이트 시 오류'''
        item = create_item()
        
        payload = {
            'name': 'Sample item 2',
            'price': 20000,
            'description': 'sample description 2'
        }
        
        url = detail_url(item.id)
        res = self.client.put(url, payload)
        
        item.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
        for k,v in payload.items():
            self.assertNotEqual(getattr(item, k), v)        
    
    def test_delete_item_by_staff(self):
        '''관리자로 Item 삭제'''
        self.user.is_staff = True
        self.user.save()
        
        item = create_item()
        
        url = detail_url(item.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_item_by_user_invalid(self):
        '''이용자로 Item 삭제 시 오류'''
        item = create_item()
        
        url = detail_url(item.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)