# Generated by Django 5.1.2 on 2024-10-30 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0004_stockhistorybfq_delete_stockhistory_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TradingDay",
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
                ("date", models.DateField(unique=True)),
                (
                    "day_type",
                    models.CharField(
                        choices=[
                            ("TRADING_DAY", "交易日"),
                            ("NON_TRADING_DAY", "非交易日"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
            options={
                "verbose_name": "交易日期",
                "verbose_name_plural": "交易日期",
            },
        ),
        migrations.AlterField(
            model_name="realtimestock",
            name="highest_price",
            field=models.FloatField(verbose_name="最高"),
        ),
        migrations.AlterField(
            model_name="realtimestock",
            name="lowest_price",
            field=models.FloatField(verbose_name="最低"),
        ),
        migrations.AlterField(
            model_name="realtimestock",
            name="today_opening_price",
            field=models.FloatField(verbose_name="今开"),
        ),
        migrations.AlterField(
            model_name="realtimestock",
            name="yesterday_closing_price",
            field=models.FloatField(verbose_name="昨收"),
        ),
    ]