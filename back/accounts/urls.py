from django.urls import path
from . import views
from .views import UserProfileUpdateView
urlpatterns = [
    path('<str:username>/info/', views.user_info, name='user-info'),
    path('<int:user_pk>/articles/',views.get_user_articles,name='user_article'),#유저가 쓴 글 갖고오기
    path('<int:user_pk>/comments/',views.get_user_comments),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile-update')
]
