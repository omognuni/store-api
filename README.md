# 온라인 스토어

### 설치
- git clone 후 다음 명령어 실행
```
docker-compose up --build
```
- 테스트 결과 확인
```
docker-compose run --rm store sh -c 'python manage.py test'
```
- 테스트 코드는 각 app 들의 tests 폴더 참조
  - store/core/tests
  - store/item/tests
  - store/order/tests
  - store/user/tests

<img src='/images/test.PNG'>


### ERD
<img src='/images/ERD.png'>

### User
- 이용자
- 관리자
  -  staff 권한

| 내용 | Method | URL |
|------|---|---------|
|회원가입|POST| api/user/create|
|Token 인증|POST| api/user/token|

### 주문내역(Order)
 - 조회, 생성, 수정, 삭제
 - 주문 내역 조회 
   - 관리자일 경우 전체
   - 이용자일 경우 이용자가 만든 order만 조회
  
- 주문 내역 검색
  - 결제 상태로 주문 내역 검색 가능


| Method | URL |
|---|------| 
|GET| api/order/orders|
|POST| api/order/orders|
|PUT,PATCH| api/order/orders/order_id|
|DELETE| api/order/orders/order_id|
|query params| api/order/orders/?search=status|

### 상품(Item)
 - items/item
 - 관리자
   - 조회, 생성, 수정, 삭제
 - 이용자
   - 조회
  
  | Method | URL |
  |--------|--------| 
  |GET| api/item/items|
  |POST| api/item/items|
  |PUT,PATCH| api/item/items/item_id|
  |DELETE| api/item/items/item_id|
 

### 이슈
1.  User api 테스트에서 get_user_model().objects.create_user() 로 생성한 유저로 
  토큰을 받으려고 하면 user.authenticate() 함수에서 none이 반환됨
2. Token Authentication 적용 시 settings.py 에서 해당 코드 추가해야됨
```
REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
   ),
}
```
3. 깃허브 Readme에 이미지 안뜨는 버그 있어서 다음으로 해결

- 호스팅 한지 몇 분 밖에 안지났을 경우 조금 더 기다려 본다. 
소요시간 1분~10분, 그래도 안될 경우 아래 빈 커밋을 넣어준다.
```
$ git commit --allow-empty -m "Trigger rebuild"
$ git push
출처: https://eunhee-programming.tistory.com/164 [코드짜는 문과녀:티스토리]
```