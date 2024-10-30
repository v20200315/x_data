from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

from stocks.models import TradingDate, StockHistoryQfq


class Command(BaseCommand):
    help = "Initialize TradingDay data from 1990-01-01 to 2024-10-30"

    def handle(self, *args, **kwargs):
        start_date = datetime(2024, 10, 30)
        end_date = datetime(2024, 12, 31)
        current_date = start_date

        while current_date <= end_date:

            if current_date.weekday() in [5, 6]:  # 5是周六，6是周日
                day_type = "NON_TRADING_DAY"
            else:
                day_type = "TRADING_DAY"

            TradingDate.objects.get_or_create(
                date=current_date, defaults={"type": day_type}
            )
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("成功初始化TradingDay数据！"))
