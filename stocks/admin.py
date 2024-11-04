from django.contrib import admin

from stocks.models import (
    StockHistoryBfq,
    StockHistoryQfq,
    StockHistoryHfq,
    RealTimeStock,
    TradingDate,
)


class RealTimeStockAdmin(admin.ModelAdmin):
    list_display = (
        "trading_date_time",
        "stock_code",
        "stock_name",
        "latest_price",
        "price_change_percentage",
        "price_change_amount",
        "trading_volume",
        "trading_amount",
        "price_range",
        "highest_price",
        "lowest_price",
        "today_opening_price",
        "yesterday_closing_price",
        "volume_ratio",
        "turnover_rate",
        "pe_ratio",
        "pb_ratio",
        "total_market_capitalization",
        "circulating_market_capitalization",
        "increasing_rate",
        "five_minutes_price_change",
        "sixty_days_price_change_percentage",
        "year_to_date_price_change_percentage",
        "created_at",
    )
    search_fields = ["stock_code"]  # 允许根据stock_code查询
    ordering = [
        "stock_code",
        "-trading_date_time",
    ]  # 默认排序：stock_code正序，trading_date逆序


admin.site.register(RealTimeStock, RealTimeStockAdmin)


class StockHistoryBfqAdmin(admin.ModelAdmin):
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
        "created_at",
    )
    search_fields = ["stock_code"]  # 允许根据stock_code查询
    ordering = [
        "-trading_date",
        "stock_code",
    ]  # 默认排序：stock_code正序，trading_date逆序


admin.site.register(StockHistoryBfq, StockHistoryBfqAdmin)


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
        "created_at",
    )
    search_fields = ["stock_code"]  # 允许根据stock_code查询
    ordering = [
        "-trading_date",
        "stock_code",
    ]  # 默认排序：stock_code正序，trading_date逆序


admin.site.register(StockHistoryQfq, StockHistoryQfqAdmin)


class StockHistoryHfqAdmin(admin.ModelAdmin):
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
        "created_at",
    )
    search_fields = ["stock_code"]  # 允许根据stock_code查询
    ordering = [
        "stock_code",
        "-trading_date",
    ]  # 默认排序：stock_code正序，trading_date逆序


admin.site.register(StockHistoryHfq, StockHistoryHfqAdmin)


class TradingDateAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "type",
    )
    ordering = [
        "-date",
    ]


admin.site.register(TradingDate, TradingDateAdmin)
