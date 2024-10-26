from django.contrib import admin

from stocks.models import StockHistory, StockHistoryQfq, StockHistoryHfq


class StockHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(StockHistory)


class StockHistoryQfqAdmin(admin.ModelAdmin):
    list_display = (
        "trading_date",
        "stock_code",
        "opening_price",
        "closing_price",
        "highest_price",
        "lowest_price",
        "trading_volume",
        "trading_amount",
        "price_range",
        "price_change_percentage",
        "price_change_amount",
        "turnover_rate",
    )
    search_fields = ["stock_code"]  # 允许根据stock_code查询
    ordering = [
        "stock_code",
        "-trading_date",
    ]  # 默认排序：stock_code正序，trading_date逆序


admin.site.register(StockHistoryQfq, StockHistoryQfqAdmin)


class StockHistoryHfqAdmin(admin.ModelAdmin):
    pass


admin.site.register(StockHistoryHfq)
