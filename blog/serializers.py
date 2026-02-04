from rest_framework import serializers
from .models import Category, Post
import markdown


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    content_html = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'author_name',
            'category', 'category_name', 'content', 'content_html',
            'excerpt', 'status', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['author']

    def get_content_html(self, obj):
        return markdown.markdown(obj.content, extensions=['extra', 'codehilite'])

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
