from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        "Название категории",
        max_length=256,
    )
    slug = models.SlugField(
        "Slug категории",
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField(
        "Название жанра",
        max_length=256,
    )
    slug = models.SlugField(
        "Slug жанра",
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.TextField(
        "Название произведения",
    )
    year = models.IntegerField(
        "Год выпуска",
    )
    description = models.TextField(
        "Описание",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        verbose_name="Жанры",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["-id"]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Жанр",
        related_name="genre_title",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        related_name="title_genre",
    )

    def __str__(self):
        return f"{self.genre} {self.title}"

    class Meta:
        verbose_name = "Связь жанра и произведения"
        verbose_name_plural = "Связи жанра и произведения"


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Статья",
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор отзыва",
        related_name="reviews",
    )
    score = models.IntegerField(
        "Оценка",
    )
    text = models.TextField(
        "Содержание отзыва",
    )
    pub_date = models.DateTimeField(
        "Дата отзыва",
        auto_now_add=True,
    )

    def __str__(self):
        return f"Ревью на {self.title}, автор {self.author}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_title_author"
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
    )
    text = models.TextField(
        "Содержание отзыва",
    )
    pub_date = models.DateTimeField(
        "Дата комментария",
        auto_now_add=True,
    )

    def __str__(self):
        return f"Комментарий к отзыву {self.review}, автор {self.author}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
