from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, BlogPost
from .serializers import CategorySerializer, BlogPostSerializer
from .permissions import IsOwnerUserOnly


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class BlogListView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().order_by("-views", "-date")
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class ViewsUpdateView(APIView):
    def patch(self, request, pk):
        blog = BlogPost.objects.get(pk=pk)
        blog.views += 1
        blog.save()
        return Response({"message": "Views updated successfully"})


class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]


class BlogPostUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerUserOnly]
    lookup_field = "id"


class BlogPostDetailsView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
