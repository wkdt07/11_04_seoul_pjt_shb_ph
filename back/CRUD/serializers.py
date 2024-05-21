from rest_framework import serializers

from .models import Article,Comment

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields=('id','title','content','user')
        

class ArticleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model=Article
        fields='__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'
        read_only_fields = ('user','article')
