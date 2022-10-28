from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/item/', include('item.urls')),
    path('api/order/', include('order.urls')),
]
