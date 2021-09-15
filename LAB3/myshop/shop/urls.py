from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
              # path('register',views.register,name='register'),
               path('login/', loginPage, name='login'),
               path('register/', registerPage, name='register'),
               path('logout/', logoutPage, name='logout'),
               path('<slug:category_slug>/', product_list, name='product_list_by_category'),
               path('<int:id>/<slug:slug>/', product_detail, name='product_detail'),
               path('api/energetics/', APIProductList.as_view()),
               path('api/<int:pk>/', APIProductDetail.as_view()),
               path('', product_list, name='product_list'),

               ]
