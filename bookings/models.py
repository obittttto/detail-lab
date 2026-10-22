from django.db import models
from services.models import Service

class Booking(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        CONFIRMED = "confirmed", "Подтверждена"
        COMPLETED = "completed", "Выполнена"
        CANCELLED = "cancelled", "Отменена"

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Услуга",
    )
    client_name = models.CharField(
        max_length=100,
        verbose_name="Имя клиента",
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
    )
    car = models.CharField(
        max_length=150,
        verbose_name="Автомобиль",
    )
    preferred_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Желаемая дата",
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )
    telegram_user_id = models.BigIntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Telegram ID клиента",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заявки",
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} — {self.service.title}"

# Create your models here.
