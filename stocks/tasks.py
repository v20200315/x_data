import akshare as ak
from celery import shared_task
from datetime import datetime
from django.db import transaction
from stocks.models import StockHistoryQfq


@shared_task
def fetch_and_save_stock_history():
    print("start fetch_and_save_stock_history")
    today_df = ak.stock_zh_a_spot_em()
    for today_row in today_df.itertuples(index=True):
        stock_code = today_row.代码
        now = datetime.now()
        date_string = now.strftime("%Y%m%d")
        history_df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date="19901219",
            end_date=date_string,
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
            for history_row in history_df.itertuples(index=True)
        ]
        with transaction.atomic():  # 使用事务管理
            StockHistoryQfq.objects.bulk_create(instances)
            print(f"done {stock_code}")

    print("end fetch_and_save_stock_history")


@shared_task
def fetch_and_update_stock_history():
    print("start fetch_and_update_stock_history")
    print("end fetch_and_update_stock_history")
