from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

from stocks.models import TradingDate, StockHistoryQfq


class Command(BaseCommand):
    help = "Initialize TradingDay data from 1990-01-01 to 2024-10-30"

    def handle(self, *args, **kwargs):
        start_date = datetime(1990, 12, 19)
        end_date = datetime(2024, 10, 29)
        current_date = start_date

        # 获取所有交易日的集合
        trading_dates = set(
            StockHistoryQfq.objects.values_list("trading_date", flat=True)
        )

        while current_date <= end_date:
            day_type = (
                "TRADING_DAY"
                if current_date.date() in trading_dates
                else "NON_TRADING_DAY"
            )

            # if current_date.date() in trading_dates:
            #     day_type = "TRADING_DAY"
            # else:
            #     # 如果不在交易日集合中，检查是否为周六或周日
            #     if current_date.weekday() in [5, 6]:  # 5是周六，6是周日
            #         day_type = "NON_TRADING_DAY"
            #     else:
            #         day_type = "TRADING_DAY"  # 平日但不是在交易日集合，则标记为交易日

            TradingDate.objects.get_or_create(
                date=current_date, defaults={"type": day_type}
            )
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("成功初始化TradingDay数据！"))
