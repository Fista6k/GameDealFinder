from django.contrib import admin
from .models import Game, Store, PriceHistory, WaitList, User
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active")

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lowest_price", "lowest_price_currency", "itad_id")
    search_fields = ("title",)
    list_filter = ("lowest_price_currency",)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "website", "itad_id")
    search_fields = ("name",)

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "store", "discount_price", "price", "discount_percent", "recorded_at", "is_history_low")
    search_fields = ("game__title", "store__name")
    list_filter = ("store", "is_history_low")

@admin.register(WaitList)
class WaitListAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "game", "target_price", "is_notified", "notified_at")
    search_fields = ("user__email", "game__title")
    list_filter = ("is_notified",)
