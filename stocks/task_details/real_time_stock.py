import akshare as ak
from datetime import date, datetime
from django.db import transaction
from django.utils import timezone

from stocks.models import RealTimeStock, TradingDate


def run():
    print("start fetch_and_save_real_time_stock")

    today = date.today()
    try:
        trading_date = TradingDate.objects.get(date=today)
        if trading_date.type == "TRADING_DAY":
            print(f"今天是交易日: {today}")
            _do_task()
        else:
            print(f"今天是非交易日: {today}")
    except TradingDate.DoesNotExist:
        print("今天的日期在数据库中不存在，无法判断。")

    print("end fetch_and_save_real_time_stock")


def _do_task():
    current_df = ak.stock_zh_a_spot_em()
    naive_datetime = datetime.now()
    aware_datetime = timezone.make_aware(naive_datetime)
    instances = [
        RealTimeStock(
            trading_date_time=aware_datetime,
            stock_code=current_row[1],
            stock_name=current_row[2],
            latest_price=current_row[3],
            price_change_percentage=current_row[4],
            price_change_amount=current_row[5],
            trading_volume=current_row[6],
            trading_amount=current_row[7],
            price_range=current_row[8],
            highest_price=current_row[9],
            lowest_price=current_row[10],
            today_opening_price=current_row[11],
            yesterday_closing_price=current_row[12],
            volume_ratio=current_row[13],
            turnover_rate=current_row[14],
            pe_ratio=current_row[15],
            pb_ratio=current_row[16],
            total_market_capitalization=current_row[17],
            circulating_market_capitalization=current_row[18],
            increasing_rate=current_row[19],
            five_minutes_price_change=current_row[20],
            sixty_days_price_change_percentage=current_row[21],
            year_to_date_price_change_percentage=current_row[22],
        )
        for current_row in current_df.itertuples(index=False)
    ]
    with transaction.atomic():  # 使用事务管理
        RealTimeStock.objects.bulk_create(instances)
