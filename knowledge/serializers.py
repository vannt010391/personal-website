from rest_framework import serializers
from .models import Topic, KnowledgeEntry, Resource
import markdown


class TopicSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    subtopics_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'description', 'parent', 'parent_name', 'subtopics_count', 'created_at']

    def get_subtopics_count(self, obj):
        return obj.subtopics.count()


class KnowledgeEntrySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    content_html = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeEntry
        fields = [
            'id', 'user', 'user_name', 'title', 'slug', 'topic', 'topic_name',
            'entry_type', 'content', 'content_html', 'summary', 'source_url',
            'tags', 'tags_list', 'is_favorite', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

    def get_content_html(self, obj):
        return markdown.markdown(obj.content, extensions=['extra', 'codehilite', 'toc'])

    def get_tags_list(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ResourceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id', 'user', 'user_name', 'title', 'resource_type', 'topic', 'topic_name',
            'url', 'author', 'status', 'notes', 'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
