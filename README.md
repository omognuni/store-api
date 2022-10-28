### 온라인 스토어

### ERD
<img src='/images/ERD.png'>

### User
- 이용자
  -  login x 혹은 admin 권한 x
- 관리자
  -  login 혹은 admin 권한

### 주문내역(Order)
 - 조회, 생성, 수정, 삭제
 - 주문 내역 전체 조회 
   - orders/order
   - 관리자일 경우 전체
   - 이용자일 경우 이용자 것만 조회
 - 주문 내역 개별 조회
   - orders/order/<int:order_id>

### 상품(Item)
 - items/item
 - 관리자
   - 조회, 생성, 수정, 삭제
 - 이용자
   - 조회
 
- 결제 관리
  - order의 status로 결제대기, 결제완료, 결제취소 표시
  

### 이슈
- User api 테스트에서 get_user_model().objects.create_user() 로 생성한 유저로
- 토큰을 받으려고 하면 user.authenticate() 함수에서 none이 반환됨