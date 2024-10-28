from django.utils import timezone
from django.db import models


class RealTimeStock(models.Model):
    trading_date_time = models.DateTimeField(verbose_name="交易时间")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码")
    stock_name = models.CharField(max_length=60, verbose_name="股票名称")
    latest_price = models.FloatField(verbose_name="最新价")
    price_change_percentage = models.FloatField(verbose_name="涨跌幅(单位:%)")
    price_change_amount = models.FloatField(verbose_name="涨跌额(单位:元)")
    trading_volume = models.FloatField(verbose_name="成交量(单位:手)")
    trading_amount = models.FloatField(verbose_name="成交额(单位:元)")
    price_range = models.FloatField(verbose_name="振幅(单位:%)")
    highest_price = models.FloatField(verbose_name="最高价")
    lowest_price = models.FloatField(verbose_name="最低价")
    today_opening_price = models.FloatField(verbose_name="开盘价")
    yesterday_closing_price = models.FloatField(verbose_name="收盘价")
    volume_ratio = models.FloatField(verbose_name="量比")
    turnover_rate = models.FloatField(verbose_name="换手率(单位:%)")
    pe_ratio = models.FloatField(verbose_name="市盈率-动态")
    pb_ratio = models.FloatField(verbose_name="市净率")
    total_market_capitalization = models.FloatField(verbose_name="总市值(单位:元)")
    circulating_market_capitalization = models.FloatField(
        verbose_name="流通市值(单位:元)"
    )
    increasing_rate = models.FloatField(verbose_name="涨速")
    five_minutes_price_change = models.FloatField(verbose_name="5分钟涨跌(单位:%)")
    sixty_days_price_change_percentage = models.FloatField(
        verbose_name="60日涨跌幅(单位:%)"
    )
    year_to_date_price_change_percentage = models.FloatField(
        verbose_name="年初至今涨跌幅(单位:%)"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建日期")

    class Meta:
        verbose_name = "股票实时行情"
        verbose_name_plural = "股票实时行情"


class AbstractStockHistory(models.Model):
    trading_date = models.DateField(verbose_name="交易日")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码")
    opening_price = models.FloatField(verbose_name="开盘价")
    closing_price = models.FloatField(verbose_name="收盘价")
    highest_price = models.FloatField(verbose_name="最高价")
    lowest_price = models.FloatField(verbose_name="最低价")
    trading_volume = models.BigIntegerField(verbose_name="成交量(单位:手)")
    trading_amount = models.FloatField(verbose_name="成交额(单位:元)")
    price_range = models.FloatField(verbose_name="振幅(单位:%)")
    price_change_percentage = models.FloatField(verbose_name="涨跌幅(单位:%)")
    price_change_amount = models.FloatField(verbose_name="涨跌额(单位:元)")
    turnover_rate = models.FloatField(verbose_name="换手率(单位:%)")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建日期")

    class Meta:
        abstract = True


class StockHistoryBfq(AbstractStockHistory):
    class Meta:
        verbose_name = "股票历史记录(不复权)"
        verbose_name_plural = "股票历史记录(不复权)"


class StockHistoryQfq(AbstractStockHistory):

    class Meta:
        verbose_name = "股票历史记录(前复权)"
        verbose_name_plural = "股票历史记录(前复权)"


class StockHistoryHfq(AbstractStockHistory):

    class Meta:
        verbose_name = "股票历史记录(后复权)"
        verbose_name_plural = "股票历史记录(后复权)"
