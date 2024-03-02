from django.urls import path
from . import views

app_name = 'common'

urlpatterns= [
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('signup/', views.signup, name='signup'),
	path('common/mypage', views.mypage, name='mypage'),
	path('verification/', views.verification, name='verification'),
	path('find_username/', views.find_username_by_email, name='find_username'),
]
