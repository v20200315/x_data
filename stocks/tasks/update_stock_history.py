import akshare as ak
from celery import shared_task
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from stocks.models import StockHistoryBfq, StockHistoryQfq, StockHistoryHfq


@shared_task
def fetch_and_update_stock_history():
    print("start fetch_and_update_stock_history")
    current_df = ak.stock_zh_a_spot_em()
    stock_history_bfq_instances = []
    stock_history_qfq_instances = []
    stock_history_hfq_instances = []
    for current_row in current_df.itertuples(index=False):
        stock_code = current_row[1]
        naive_datetime = datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime)
        date_string = aware_datetime.strftime("%Y%m%d")

        _get_stock_history_bfq_instances(
            stock_history_bfq_instances, stock_code, date_string
        )
        _get_stock_history_qfq_instances(
            stock_history_qfq_instances, stock_code, date_string
        )
        _get_stock_history_hfq_instances(
            stock_history_hfq_instances, stock_code, date_string
        )

        with transaction.atomic():  # 使用事务管理
            StockHistoryBfq.objects.bulk_create(stock_history_bfq_instances)
            StockHistoryQfq.objects.bulk_create(stock_history_qfq_instances)
            StockHistoryHfq.objects.bulk_create(stock_history_hfq_instances)

    print("end fetch_and_update_stock_history")


def _get_stock_history_bfq_instances(instances, stock_code, date_string):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=date_string,
        end_date=date_string,
        adjust="",
    )
    instances.append(
        StockHistoryBfq(
            trading_date=history_row[0],
            stock_code=history_row[1],
            opening_price=history_row[2],
            closing_price=history_row[3],
            highest_price=history_row[4],
            lowest_price=history_row[5],
            trading_volume=history_row[6],
            trading_amount=history_row[7],
            price_range=history_row[8],
            price_change_percentage=history_row[9],
            price_change_amount=history_row[10],
            turnover_rate=history_row[11],
        )
        for history_row in history_df.itertuples(index=False)
    )


def _get_stock_history_qfq_instances(instances, stock_code, date_string):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=date_string,
        end_date=date_string,
        adjust="qfq",
    )
    instances.append(
        StockHistoryQfq(
            trading_date=history_row[0],
            stock_code=history_row[1],
            opening_price=history_row[2],
            closing_price=history_row[3],
            highest_price=history_row[4],
            lowest_price=history_row[5],
            trading_volume=history_row[6],
            trading_amount=history_row[7],
            price_range=history_row[8],
            price_change_percentage=history_row[9],
            price_change_amount=history_row[10],
            turnover_rate=history_row[11],
        )
        for history_row in history_df.itertuples(index=False)
    )


def _get_stock_history_hfq_instances(instances, stock_code, date_string):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=date_string,
        end_date=date_string,
        adjust="hfq",
    )
    instances.append(
        StockHistoryHfq(
            trading_date=history_row[0],
            stock_code=history_row[1],
            opening_price=history_row[2],
            closing_price=history_row[3],
            highest_price=history_row[4],
            lowest_price=history_row[5],
            trading_volume=history_row[6],
            trading_amount=history_row[7],
            price_range=history_row[8],
            price_change_percentage=history_row[9],
            price_change_amount=history_row[10],
            turnover_rate=history_row[11],
        )
        for history_row in history_df.itertuples(index=False)
    )
