import akshare as ak
from celery import shared_task
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from stocks.models import StockHistoryBfq, StockHistoryQfq, StockHistoryHfq


@shared_task
def fetch_and_save_stock_history():
    print("start fetch_and_save_stock_history")
    current_df = ak.stock_zh_a_spot_em()
    for index, current_row in current_df.itertuples(index=False):
        stock_code = current_row.代码
        naive_datetime = datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime)
        date_string = aware_datetime.strftime("%Y%m%d")

        _fetch_and_save_stock_history_bfq(stock_code=stock_code, end_date=date_string)
        _fetch_and_save_stock_history_qfq(stock_code=stock_code, end_date=date_string)
        _fetch_and_save_stock_history_hfq(stock_code=stock_code, end_date=date_string)
        print(f"index: {index}, done stock_code: {stock_code}")

    print("end fetch_and_save_stock_history")


def _fetch_and_save_stock_history_bfq(
    stock_code, start_date="19901219", end_date="19991231"
):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="",
    )
    instances = [
        StockHistoryBfq(
            trading_date=history_row.日期,
            stock_code=history_row.股票代码,
            opening_price=history_row.开盘,
            closing_price=history_row.收盘,
            highest_price=history_row.最高,
            lowest_price=history_row.最低,
            trading_volume=history_row.成交量,
            trading_amount=history_row.成交额,
            price_range=history_row.振幅,
            price_change_percentage=history_row.涨跌幅,
            price_change_amount=history_row.涨跌额,
            turnover_rate=history_row.换手率,
        )
        for history_row in history_df.itertuples(index=False)
    ]
    with transaction.atomic():
        StockHistoryBfq.objects.bulk_create(instances)


def _fetch_and_save_stock_history_qfq(
    stock_code, start_date="19901219", end_date="19991231"
):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",
    )
    instances = [
        StockHistoryQfq(
            trading_date=history_row.日期,
            stock_code=history_row.股票代码,
            opening_price=history_row.开盘,
            closing_price=history_row.收盘,
            highest_price=history_row.最高,
            lowest_price=history_row.最低,
            trading_volume=history_row.成交量,
            trading_amount=history_row.成交额,
            price_range=history_row.振幅,
            price_change_percentage=history_row.涨跌幅,
            price_change_amount=history_row.涨跌额,
            turnover_rate=history_row.换手率,
        )
        for history_row in history_df.itertuples(index=False)
    ]
    with transaction.atomic():
        StockHistoryQfq.objects.bulk_create(instances)


def _fetch_and_save_stock_history_hfq(
    stock_code, start_date="19901219", end_date="19991231"
):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="hfq",
    )
    instances = [
        StockHistoryHfq(
            trading_date=history_row.日期,
            stock_code=history_row.股票代码,
            opening_price=history_row.开盘,
            closing_price=history_row.收盘,
            highest_price=history_row.最高,
            lowest_price=history_row.最低,
            trading_volume=history_row.成交量,
            trading_amount=history_row.成交额,
            price_range=history_row.振幅,
            price_change_percentage=history_row.涨跌幅,
            price_change_amount=history_row.涨跌额,
            turnover_rate=history_row.换手率,
        )
        for history_row in history_df.itertuples(index=False)
    ]
    with transaction.atomic():
        StockHistoryHfq.objects.bulk_create(instances)
