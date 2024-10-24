from django.contrib import admin

from stocks.models import StockHistory, StockHistoryQfq, StockHistoryHfq


class StockHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(StockHistory)


class StockHistoryQfqAdmin(admin.ModelAdmin):
    pass


admin.site.register(StockHistoryQfq)


class StockHistoryHfqAdmin(admin.ModelAdmin):
    pass


admin.site.register(StockHistoryHfq)
