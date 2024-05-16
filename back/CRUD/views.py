from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
# Create your views here.
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleListSerializer,ArticleSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
  
  # 출력
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles,many=True)
        return Response(serializer.data)
    
    # create
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def article_detail(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    
    # 단일 확인 
    if request.method=='GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        return Response(serializer.data)
    
    # 수정
    elif request.method=='PUT':
        serializer=ArticleSerializer(data=request.data,instance=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    # 삭제
    elif request.method=='DELETE':
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)