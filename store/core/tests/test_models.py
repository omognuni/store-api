from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import datetime

from core.models import Item, Order

def create_user(username='testname', password='testpass'):
    return get_user_model().objects.create_user(username, password)

def create_item(name='testname', price='10000', description='test'):
    return Item.objects.create(name=name, price=price, description=description)


class ModelTest(TestCase):
    '''모델 생성 테스트'''    
    
    def test_create_user_model(self):
        '''유저 모델 생성 테스트'''
        username = 'testname'
        password = 'testpass'
        user = get_user_model().objects.create_user(username=username, password=password)
        
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        
    def test_create_superuser(self):
        '''superuser 생성 테스트'''
        username = 'testname'
        password = 'testpass'
        
        user = get_user_model().objects.create_superuser(username=username, password=password)
        
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_create_item_model(self):
        '''상품 모델 생성 테스트'''
        name = 'testitem'
        price = '10000'
        description ='test'
        
        item = Item.objects.create(name=name,price=price,description=description)
        
        self.assertEqual(str(item), item.name )
    
    def test_create_order_model(self):
        '''주문 모델 생성 테스트'''
        user = create_user()
        item = create_item(user)
        quantity = 1
        status = 'pending'
        price = item.price * quantity
        
        order = Order.objects.create(
            user=user,
            item=item,
            quantity=quantity,
            total_price=price,
            status=status
            )
        
        self.assertEqual(str(order), status)
        self.assertEqual(order.user, user)
        self.assertEqual(order.item, item)
        