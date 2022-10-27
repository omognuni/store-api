from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Order

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
MYPAGE_URL = reverse('user:mypage')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class publicAPITest(TestCase):
    '''public user api 테스트'''
    
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        '''회원가입 테스트'''
        payload = {
            'username':'testname',
            'password':'testpass'
        }
        
        res = self.client.post(payload)
        
        user = get_user_model().objects.get(username=payload['username'])
        
        self.assertEqual(res.status, status.HTTP_201_CREATED)
        self.assertEqual(user.check_password(payload['password']))
        self.assertNotIn('password'. res.data)
        
    def test_password_too_short_error(self):
        """짧은 비밀번호 입력 시 에러 """
        payload = {
            'username': ' testname',
            'password': 'pw',
            'name': 'testname',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            username=payload['username']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''로그인 시 토큰 생성'''
        payload = {
            'username': ' testname',
            'password': 'testpass',
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """잘못된 계정 입력 시 토큰 미생성"""
        create_user(username='testname', password='testpass')
        payload = {
            'username': ' testname',
            'password': 'wrong',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """미인증 사용자가 사용자 상세 페이지 진입 시 오류"""
        res = self.client.get(MYPAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    