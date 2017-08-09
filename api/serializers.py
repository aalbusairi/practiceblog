from rest_framework import serializers
from posts.models import Post

class PostListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
		view_name = "api:detail",
		lookup_field = "slug",
		lookup_url_kwarg = "post_slug"
		)
	class Meta:
		model = Post
		fields = ['title', 'author', 'slug', 'content','publish','detail']

class PostDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['id', 'author', 'title', 'slug', 'content','publish','draft']

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'content','publish','draft']				