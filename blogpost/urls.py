from django.urls import path
from . import views

urlpatterns = [
    path(
        "categories/",
        views.CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "blogs/",
        views.BlogListView.as_view(),
        name="blog-list",
    ),
    path(
        "blog/<int:pk>/views/",
        views.ViewsUpdateView.as_view(),
        name="update-views",
    ),
    path(
        "blog/<int:id>/",
        views.BlogPostUpdateDeleteView.as_view(),
        name="blog-detail",
    ),
    path(
        "blog/",
        views.BlogPostCreateView.as_view(),
        name="create-blog",
    ),
    path(
        "fetchBlog/<int:id>/",
        views.BlogPostDetailsView.as_view(),
        name="fetchDetails",
    ),
]
