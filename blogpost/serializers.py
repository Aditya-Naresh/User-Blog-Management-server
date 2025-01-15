from rest_framework import serializers
from .models import BlogPost, Category


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ["id", "name", "image", "post_count"]
        read_only_fields = ["id", "post_count"]

    def get_post_count(self, obj):
        return obj.post_count()


class BlogPostSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "user",
            "author",
            "title",
            "image",
            "content",
            "category",
            "category_name",
            "views",
            "date",
        ]
        read_only_fields = [
            "id",
            "category_name",
            "author",
            "user",
            "date",
            "views",
        ]

    def get_category_name(self, obj):
        return obj.category.name

    def get_author(self, obj):
        return obj.user.username

    def validate(self, attrs):
        if not attrs.get("title"):
            raise serializers.ValidationError(
                {
                    "title": "Title is required",
                }
            )
        if not attrs.get("content"):
            raise serializers.ValidationError(
                {
                    "content": "Content is required",
                }
            )

        if not attrs.get("category"):
            raise serializers.ValidationError(
                {
                    "category": "Category is required",
                }
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)
