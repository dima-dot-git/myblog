from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Subscribe(models.Model):
    email = models.EmailField(max_length=50, verbose_name="Пошта")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пошта"
        verbose_name_plural = "Пошта"


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опысс")
    published_data = models.DateTimeField(auto_created=True, verbose_name="Дата")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name="Заголовок")
    posts = models.ManyToManyField(Post, verbose_name="Пости")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} {self.date}"

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"


class PostsPhoto(models.Model):
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(verbose_name="Зображення", upload_to="Posts_Photos")

    class Meta:
        verbose_name = "Зображення"
        verbose_name_plural = "Зображення"

class Profile_WER(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="user_avatar")

    def __str__(self):
        return self.user.username
