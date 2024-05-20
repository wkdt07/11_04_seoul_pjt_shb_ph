from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comment_manage), # 조회,생성용
    path('comments/<int:comment_pk>/', views.comment_manage), # 수정,삭제 용
    # path('get_accounts/<str:username>/info/', views.user_info, name='user-info'),
    # # 다른 URL 패턴들
    # path('get_accounts/<int:user_pk>/articles/',views.get_user_articles,name='user_article'),#유저가 쓴 글 갖고오기
    # path('get_accounts/<int:user_pk>/comments/',views.get_user_comments)
]
