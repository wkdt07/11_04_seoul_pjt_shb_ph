from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
# Create your views here.
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from .models import Article,Comment
from .serializers import ArticleListSerializer,CommentSerializer,ArticleSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from accounts.models import User

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(data=request.data, instance=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'DELETE':
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_manage(request, article_pk=None, comment_pk=None):
    if article_pk:
        article = get_object_or_404(Article, pk=article_pk)
        comments = Comment.objects.filter(article=article)
    else:
        comments = Comment.objects.all()

    if request.method == 'GET':
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article=article, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT' and comment_pk is not None:
        try:
            comment = Comment.objects.get(pk=comment_pk, user=request.user)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE' and comment_pk is not None:
        try:
            comment = Comment.objects.get(pk=comment_pk, user=request.user)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def article_list(request):
  
#   # 출력
#     if request.method == 'GET':
#         articles = get_list_or_404(Article)
#         serializer = ArticleListSerializer(articles,many=True)
#         return Response(serializer.data)
    
#     # create
#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user)
#             return Response(serializer.data,status=status.HTTP_201_CREATED)

# @api_view(['GET','PUT','DELETE'])
# def article_detail(request,article_pk):
#     article = get_object_or_404(Article,pk=article_pk)
    
#     # 단일 확인 
#     if request.method=='GET':
#         serializer = ArticleSerializer(article)
#         print(serializer.data)
#         return Response(serializer.data)
    
#     # 수정
#     elif request.method=='PUT':
#         serializer=ArticleSerializer(data=request.data,instance=article)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
#     # 삭제
#     elif request.method=='DELETE':
#         if request.user == article.user:
#             article.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

# # @permission_classes([IsAuthenticated])
# # @api_view(['GET'])
# # def comment(request):
# #      # 단일 확인 
# #     # article = get_object_or_404(Article,pk=article_pk)
# #     if request.method=='GET':
# #         comments = Comment.objects.all()
# #         serializer = CommentSerializer(comments,many=True)
# #         print(serializer.data)
# #         return Response(serializer.data)

# @api_view(['POST', 'GET', 'DELETE', 'PUT'])
# @permission_classes([IsAuthenticated])
# def comment_manage(request, article_pk=None, comment_pk=None):
#     if article_pk:
#         article = Article.objects.get(pk=article_pk)
#         comments = Comment.objects.filter(article=article)
#     else:
#         comments = Comment.objects.all()

#     # 조회
#     if request.method == 'GET':
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
    
#     # 생성
#     elif request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(article=article, user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     # 수정
#     elif request.method == 'PUT':
#         comment = Comment.objects.get(pk=comment_pk, user=request.user)
#         serializer = CommentSerializer(comment, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     # 삭제
#     elif request.method == 'DELETE':
#         comment = Comment.objects.get(pk=comment_pk, user=request.user)
#         if request.user == comment.user:
#             comment.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_403_FORBIDDEN)
        