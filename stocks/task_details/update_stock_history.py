import akshare as ak
from datetime import date, datetime

from django.db import transaction
from django.utils import timezone

from stocks.models import StockHistoryBfq, StockHistoryQfq, StockHistoryHfq, TradingDate


def run():
    print("start fetch_and_update_stock_history")

    today = date.today()
    try:
        trading_date = TradingDate.objects.get(date=today)
        if trading_date.type == "TRADING_DAY":
            print(f"今天是交易日(fetch_and_update_stock_history): {today}")
            _do_task()
        else:
            print(f"今天是非交易日: {today}")
    except TradingDate.DoesNotExist:
        print("今天的日期在数据库中不存在，无法判断。")

    print("end fetch_and_update_stock_history")


def _do_task():
    stock_history_bfq_instances = []
    stock_history_qfq_instances = []
    # stock_history_hfq_instances = []
    current_df = ak.stock_zh_a_spot_em()
    for current_row in current_df.itertuples(index=False):
        stock_code = current_row[1]
        naive_datetime = datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime)
        date_string = aware_datetime.strftime("%Y%m%d")

        stock_history_bfq_instances.extend(
            _get_stock_history_bfq_instances(stock_code, date_string)
        )
        stock_history_qfq_instances.extend(
            _get_stock_history_qfq_instances(stock_code, date_string)
        )
        # stock_history_hfq_instances.extend(
        #     _get_stock_history_hfq_instances(stock_code, date_string)
        # )
    with transaction.atomic():  # 使用事务管理
        StockHistoryBfq.objects.bulk_create(stock_history_bfq_instances)
        StockHistoryQfq.objects.bulk_create(stock_history_qfq_instances)
        # StockHistoryHfq.objects.bulk_create(stock_history_hfq_instances)


def _get_stock_history_bfq_instances(stock_code, date_string):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=date_string,
        end_date=date_string,
        adjust="",
    )
    instances = [
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
    ]
    return instances


def _get_stock_history_qfq_instances(stock_code, date_string):
    history_df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=date_string,
        end_date=date_string,
        adjust="qfq",
    )
    instances = [
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
    ]
    return instances


# def _get_stock_history_hfq_instances(stock_code, date_string):
#     history_df = ak.stock_zh_a_hist(
#         symbol=stock_code,
#         period="daily",
#         start_date=date_string,
#         end_date=date_string,
#         adjust="hfq",
#     )
#     instances = [
#         StockHistoryHfq(
#             trading_date=history_row[0],
#             stock_code=history_row[1],
#             opening_price=history_row[2],
#             closing_price=history_row[3],
#             highest_price=history_row[4],
#             lowest_price=history_row[5],
#             trading_volume=history_row[6],
#             trading_amount=history_row[7],
#             price_range=history_row[8],
#             price_change_percentage=history_row[9],
#             price_change_amount=history_row[10],
#             turnover_rate=history_row[11],
#         )
#         for history_row in history_df.itertuples(index=False)
#     ]
#     return instances
