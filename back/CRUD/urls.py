from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comment_manage), # 조회,생성용
    path('comments/<int:comment_pk>/', views.comment_manage), # 수정,삭제 용
]