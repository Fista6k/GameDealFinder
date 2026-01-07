from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    itad_plain = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="ITAD plain"
    )

    description = models.TextField(blank=True, verbose_name="Описание")
    release_date = models.DateField(null=True, blank=True, verbose_name="Дата выхода")
    developer = models.CharField(max_length=255, blank=True, verbose_name="Разработчик")
    publisher = models.CharField(max_length=255, blank=True, verbose_name="Издатель")

    image_url = models.URLField(blank=True, verbose_name="Обложка")

    genres = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Жанры (через запятую)"
    )
    platforms = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Платформы (windows, linux, mac)"
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


class Store(models.Model):
    itad_id = models.CharField(
        max_length=50,
        unique=True,
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
        verbose_name="Скидка (%)"
    )

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
        auto_now_add=True,
        verbose_name="Время записи"
    )

    def __str__(self):
        return f"{self.game.title} — {self.store.name}: {self.discount_price} {self.currency}"

    class Meta:
        verbose_name = "История цены"
        verbose_name_plural = "История цен"
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(fields=["game", "store"]),
            models.Index(fields=["discount_price"]),
        ]
