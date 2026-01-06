from django.contrib import admin
from .models import Game, Store, PriceHistory


admin.site.register(Game)
admin.site.register(Store)
admin.site.register(PriceHistory)