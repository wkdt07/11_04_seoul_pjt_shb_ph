from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserInfoSerializer
from CRUD.models import Article,Comment
from CRUD.serializers import ArticleSerializer,CommentSerializer

User = get_user_model() # 유저 모델 전체 다 갖고 옴

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    serializer = UserInfoSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_articles(request, user_pk):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    articles = Article.objects.filter(user=user.pk)
    if not articles.exists():
        return Response({"message": "No articles found for this user."}, status=200)
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_comments(request, user_pk):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    comments = Comment.objects.filter(user=user.pk)
    if not comments.exists():
        return Response({"message": "No comments found for this user."}, status=200)


    # comments = Comment.objects.filter(user=user)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)