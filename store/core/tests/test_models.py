from django.test import TestCase
from django.contrib.auth import get_user_model


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
        