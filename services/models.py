from django.db import models

class Service(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Название услуги",
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        verbose_name="URL услуги"
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    price_from = models.PositiveIntegerField(
        verbose_name="Цена от, BYN",
    )
    duration_minutes = models.PositiveIntegerField(
        default=60,
        verbose_name="Продолжительность в минутах",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Ссылка на изображение",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["id"]

    def __str__(self):
        return self.title
# Create your models here.
