from django.urls import path
from user.views import *

urlpatterns = [
    path('cart/', cart_detail, name='cart'),
    path('add/<int:book_id>/', cart_add, name='cart_add'),
    path('remove/<int:book_id>/', cart_remove, name='cart_remove'),
    path('update/', cart_update, name='cart_update'),


    path('login/', login_views, name='login'),
    path('register/', register_views, name='register'),
    path('logout/', logout_views, name='logout'),
    path('verify_email/<int:user_id>/', verify_email, name='verify_email'),

    path('account/', account_views, name='account'),

    path('password-reset/', password_reset_views, name='password_reset_views'),
    path('password-reset/<int:user_id>/', password_reset_verify, name='password_reset_verify'),
    path('password-reset-confirm/<int:user_id>/', password_reset_confirm, name='password_reset_confirm'),

]
