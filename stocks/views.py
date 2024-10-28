import time
from django.http import JsonResponse
from datetime import date
import pandas as pd
from django.core.cache import cache
from io import BytesIO

from .models import StockHistoryBfq, StockHistoryQfq, StockHistoryHfq
from .tasks import fetch_and_save_stock_history


def fetch_stock_history(request):
    if (
        not StockHistoryBfq.objects.exists()
        and not StockHistoryQfq.objects.exists()
        and not StockHistoryHfq.objects.exists()
    ):
        task = fetch_and_save_stock_history.delay()  # 异步调用任务
        return JsonResponse({"task_id": task.id, "status": "Task is being processed!"})
    return JsonResponse({"status": "no task need to process!"})


def get_stock_history_from_db(request):
    start_time = time.time()  # 记录开始时间
    dataset = get_2023_stock_history()
    end_time = time.time()  # 记录结束时间
    execution_time = end_time - start_time  # 计算执行时间
    print(f"Function executed in: {execution_time:.5f} seconds")
    check_dataset_size(dataset)
    check_dataset_memory_usage(dataset)
    save_dataset_to_cache("2023_stock_history", dataset)
    return JsonResponse({"status": "Task is done!"})


def get_stock_history_from_cache(request):
    start_time = time.time()  # 记录开始时间
    dataset = load_dataset_from_cache("2023_stock_history")
    end_time = time.time()  # 记录结束时间
    execution_time = end_time - start_time  # 计算执行时间
    print(f"Function executed in: {execution_time:.5f} seconds")
    check_dataset_size(dataset)
    check_dataset_memory_usage(dataset)
    return JsonResponse({"status": "Task is done!"})


def get_2023_stock_history():
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    queryset = StockHistoryQfq.objects.filter(
        trading_date__range=[start_date, end_date]
    )
    data = list(queryset.values())
    dataset = pd.DataFrame(data)
    return dataset


def check_dataset_size(dataset):
    # 查看DataFrame的大小
    size = dataset.shape  # 返回一个元组 (行数, 列数)
    print(f"Dataset size: {size[0]} rows, {size[1]} columns")


def check_dataset_memory_usage(dataset):
    memory_usage = dataset.memory_usage(deep=True)
    print(f"Memory usage of each column:\n{memory_usage}")
    print(f"Total memory usage: {memory_usage.sum()} bytes")
    total_memory_usage_bytes = memory_usage.sum()
    total_memory_usage_mb = total_memory_usage_bytes / (1024 * 1024)
    print(f"Total memory usage: {total_memory_usage_mb:.2f} MB")


# 将DataFrame保存到Redis缓存
def save_dataset_to_cache(key, dataset):
    # 使用BytesIO创建一个字节流
    buffer = BytesIO()
    # 将DataFrame序列化为字节串并写入字节流
    dataset.to_pickle(buffer)
    # 获取字节流的内容
    dataset_bytes = buffer.getvalue()
    # 将字节串存储到Redis缓存
    cache.set(key, dataset_bytes)


# 从Redis缓存中读取DataFrame
def load_dataset_from_cache(key):
    dataset_bytes = cache.get(key)
    if dataset_bytes:
        # 使用BytesIO读取字节串
        buffer = BytesIO(dataset_bytes)
        return pd.read_pickle(buffer)  # 反序列化为DataFrame
    return None
