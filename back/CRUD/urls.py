from django.urls import path,include
from . import views

urlpatterns = [
  path('',views.article_list),
  path('<int:article_pk>/',views.article_detail),
  path('comments/',views.comment),
  path('<int:article_pk>/comments/',views.comment_create)
]
