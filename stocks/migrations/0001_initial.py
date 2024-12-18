# Generated by Django 5.1.2 on 2024-10-23 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StockHistoryQfq",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trading_date", models.DateField(verbose_name="交易日")),
                (
                    "stock_code",
                    models.CharField(max_length=20, verbose_name="股票代码"),
                ),
                ("opening_price", models.FloatField(verbose_name="开盘价")),
                ("closing_price", models.FloatField(verbose_name="收盘价")),
                ("highest_price", models.FloatField(verbose_name="最高价")),
                ("lowest_price", models.FloatField(verbose_name="最低价")),
                (
                    "trading_volume",
                    models.BigIntegerField(verbose_name="成交量(单位:手)"),
                ),
                ("trading_amount", models.FloatField(verbose_name="成交额(单位:元)")),
                ("price_range", models.FloatField(verbose_name="振幅(单位:%)")),
                (
                    "price_change_percentage",
                    models.FloatField(verbose_name="涨跌幅(单位:%)"),
                ),
                (
                    "price_change_amount",
                    models.FloatField(verbose_name="涨跌额(单位:元)"),
                ),
                ("turnover_rate", models.FloatField(verbose_name="换手率(单位:%)")),
            ],
        ),
    ]
