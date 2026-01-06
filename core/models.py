from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    release_date = models.DateField(null=True, blank=True, verbose_name="Дата выхода")
    developer = models.CharField(max_length=255, blank=True, verbose_name="Разработчик")
    publisher = models.CharField(max_length=255, blank=True, verbose_name="Издатель")
    imageUrl = models.URLField(blank=True, verbose_name="Обложка")

    genres = models.CharField(max_length=255, blank=True, verbose_name="Жанры")
    platforms = models.CharField(max_length=255, blank=True, verbose_name="Платформы")

    steamAPIid = models.IntegerField(null=True, blank=True, verbose_name="Steam ID")

    def __str__(self):
        return self.title
    
    def getCurrentPrice(self):
        latestPrice = PriceHistory.objects.filter(game=self).order_by("-recordedAt").first()

        if latestPrice:
            return {
                "price": latestPrice.discountPrice,
                "currency": latestPrice.currency,
                "store": latestPrice.store,
                "discount": latestPrice.discountPercent
            }
        return None
    
    def getLowestPrice(self):
        lowest = PriceHistory.objects.filter(game=self, isLowest=True).first()
        return lowest

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", choices= [("steam", "Steam"), ("epic", "Epic Games"), ("gog", "GOG")])
    website = models.URLField(verbose_name="Сайт")
    
    api_endpoint = models.URLField(blank=True, verbose_name="API")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        if self.name == "steam":
            return "Steam"
        elif self.name == "epic":
            return "Epic Games"
        else:
            return "GOG"
    
    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
    
class PriceHistory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Игра")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Магазин")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Обычная цена")
    discountPrice = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Цена со скидкой")
    discountPercent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Скидка в %")
    currency = models.CharField(max_length=3, choices=[("USD", "Доллар"), ("EUR", "Евро"), ("RUB", "Рубль")], default="RUB", verbose_name="Валюта")
    recordedAt = models.DateTimeField(auto_now_add=True, verbose_name="Время записи")
    isLowest = models.BooleanField(default=False, verbose_name="Исторический минимум")

    def __str__(self):
        return f"{self.game.title} в {self.store}: {self.discountPrice}"
    
    class Meta:
        verbose_name = "История цены"
        verbose_name_plural = "История цен"

        ordering = ["-recordedAt"]