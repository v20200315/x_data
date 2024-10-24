from django.contrib import admin

from stocks.models import StockHistory, StockHistoryQfq, StockHistoryHfq

admin.site.register(StockHistory)
admin.site.register(StockHistoryQfq)
admin.site.register(StockHistoryHfq)
