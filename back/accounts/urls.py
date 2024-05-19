from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/info/', views.user_info, name='user-info'),
    # 다른 URL 패턴들
    path('<int:user_pk>/articles/',views.get_user_articles,name='user_article'),#유저가 쓴 글 갖고오기
    path('<int:user_pk>/comments/',views.get_user_comments)
]
