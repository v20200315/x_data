# 存放一些待验证的方法
import pickle
import pandas as pd
from datetime import date
from django.core.cache import cache

from stocks.models import StockHistoryQfq
from x_data.tools import execution_time


@execution_time
def _get_stock_history_from_db():
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    queryset = StockHistoryQfq.objects.filter(
        trading_date__range=[start_date, end_date]
    )
    data = list(queryset.values())
    dataset = pd.DataFrame(data)
    _check_dataset_size(dataset)
    _check_dataset_memory_usage(dataset)
    cache.set("2023_stock_history", pickle.dumps(dataset), timeout=None)


@execution_time
def _get_stock_history_from_cache():
    dataset = pickle.loads(cache.get("2023_stock_history"))
    _check_dataset_size(dataset)
    _check_dataset_memory_usage(dataset)
    return dataset


def _check_dataset_size(dataset):
    # 查看DataFrame的大小
    size = dataset.shape  # 返回一个元组 (行数, 列数)
    print(f"Dataset size: {size[0]} rows, {size[1]} columns")


def _check_dataset_memory_usage(dataset):
    memory_usage = dataset.memory_usage(deep=True)
    print(f"Memory usage of each column:\n{memory_usage}")
    print(f"Total memory usage: {memory_usage.sum()} bytes")
    total_memory_usage_bytes = memory_usage.sum()
    total_memory_usage_mb = total_memory_usage_bytes / (1024 * 1024)
    print(f"Total memory usage: {total_memory_usage_mb:.2f} MB")
