from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class Store(models.Model):
    itad_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        verbose_name="ITAD shop id"
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    website = models.URLField(verbose_name="Сайт")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class Game(models.Model):
    title = models.CharField(max_length=1000, verbose_name="Название")
    itad_plain = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        verbose_name="ITAD plain",
        blank=True
    )
    itad_id = models.UUIDField(max_length=36, unique=True, null=True)
    release_date = models.DateField(null=True, blank=True, verbose_name="Дата выхода")
    developer = models.CharField(max_length=512, blank=True, verbose_name="Разработчик")
    publisher = models.CharField(max_length=512, blank=True, verbose_name="Издатель")

    image_url = models.URLField(blank=True, verbose_name="Обложка")

    lowest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lowest_price_currency = models.CharField(max_length=3, default="USD", null=True, blank=True)

    genres = models.CharField(
        max_length=512,
        blank=True,
        verbose_name="Жанры (через запятую)"
    )

    def __str__(self):
        return self.title

    def get_current_price(self):
        return (
            PriceHistory.objects
            .filter(game=self)
            .order_by("discount_price")
            .select_related("store")
            .first()
        )

    def get_lowest_price(self):
        return (
            PriceHistory.objects
            .filter(game=self)
            .order_by("discount_price")
            .select_related("store")
            .first()
        )

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

class PriceHistory(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="prices",
        verbose_name="Игра"
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="prices",
        verbose_name="Магазин"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Обычная цена"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена со скидкой"
    )
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        verbose_name="Скидка (%)"
    )
    is_history_low = models.BooleanField(null=True, verbose_name="Исторический минимум")

    currency = models.CharField(
        max_length=3,
        choices=[
            ("USD", "Доллар"),
            ("EUR", "Евро"),
            ("RUB", "Рубль"),
        ],
        default="EUR",
        verbose_name="Валюта"
    )

    store_url = models.URLField(
        blank=True,
        verbose_name="Ссылка на магазин"
    )

    recorded_at = models.DateTimeField(
        verbose_name="Время записи"
    )

    def __str__(self):
        return f"{self.game.title} — {self.store.name}: {self.discount_price} {self.currency}"

    class Meta:
        verbose_name = "История цены"
        verbose_name_plural = "История цен"
        ordering = ["-recorded_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["game", "store", "recorded_at"],
                name="unique_price_snapshot"
            )
        ]

        indexes = [
            models.Index(fields=["game", "store"]),
            models.Index(fields=["discount_price"]),
        ]

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class WaitList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="waitlist_items")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="waitlisted_by")
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Желаемая цена")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")
        verbose_name = "Вейтлист"
        verbose_name_plural = "Вейтлисты"

    def __str__(self):
        return f"{self.user.email} -> {self.game.title}"