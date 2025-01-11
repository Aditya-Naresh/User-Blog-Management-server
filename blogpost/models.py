from django.db import models
from django.utils.text import slugify
from authentication.models import User
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField(
        "image",
        null=True,
        blank=True,
    )
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def post_count(self):
        return BlogPost.objects.filter(category=self).count()


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = CloudinaryField(
        "image",
        null=True,
        blank=True,
    )
    content = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="posts",
    )
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "BlogPosts"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
