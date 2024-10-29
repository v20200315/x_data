import time
import pandas as pd
from io import BytesIO
from datetime import date
from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from x_data.tools import execution_time
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


@execution_time
@api_view(["GET"])
def get_stock_data(request, stock_code):
    # 获取可选的查询参数 start_date 和 end_date
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)

    # 根据股票代码从数据库中获取数据
    stock_data = StockHistoryQfq.objects.filter(stock_code=stock_code)

    if start_date:
        stock_data = stock_data.filter(trading_date__gte=start_date)
    if end_date:
        stock_data = stock_data.filter(trading_date__lte=end_date)

    if stock_data.exists():
        # 将查询结果转换为字典列表
        data = [
            {
                "trading_date": stock.trading_date,
                "opening_price": stock.opening_price,
                "closing_price": stock.closing_price,
                "highest_price": stock.highest_price,
                "lowest_price": stock.lowest_price,
                "trading_volume": stock.trading_volume,
                "trading_amount": stock.trading_amount,
                "price_range": stock.price_range,
                "price_change_percentage": stock.price_change_percentage,
                "price_change_amount": stock.price_change_amount,
                "turnover_rate": stock.turnover_rate,
            }
            for stock in stock_data
        ]
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "股票数据未找到"}, status=status.HTTP_404_NOT_FOUND)


def _get_stock_history_from_db(request):
    start_time = time.time()  # 记录开始时间
    dataset = _get_2023_stock_history()
    end_time = time.time()  # 记录结束时间
    execution_time = end_time - start_time  # 计算执行时间
    print(f"Function executed in: {execution_time:.5f} seconds")
    _check_dataset_size(dataset)
    _check_dataset_memory_usage(dataset)
    _save_dataset_to_cache("2023_stock_history", dataset)
    return JsonResponse({"status": "Task is done!"})


def _get_stock_history_from_cache(request):
    start_time = time.time()  # 记录开始时间
    dataset = _load_dataset_from_cache("2023_stock_history")
    end_time = time.time()  # 记录结束时间
    execution_time = end_time - start_time  # 计算执行时间
    print(f"Function executed in: {execution_time:.5f} seconds")
    _check_dataset_size(dataset)
    _check_dataset_memory_usage(dataset)
    return JsonResponse({"status": "Task is done!"})


def _get_2023_stock_history():
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    queryset = StockHistoryQfq.objects.filter(
        trading_date__range=[start_date, end_date]
    )
    data = list(queryset.values())
    dataset = pd.DataFrame(data)
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


# 将DataFrame保存到Redis缓存
def _save_dataset_to_cache(key, dataset):
    # 使用BytesIO创建一个字节流
    buffer = BytesIO()
    # 将DataFrame序列化为字节串并写入字节流
    dataset.to_pickle(buffer)
    # 获取字节流的内容
    dataset_bytes = buffer.getvalue()
    # 将字节串存储到Redis缓存
    cache.set(key, dataset_bytes)


# 从Redis缓存中读取DataFrame
def _load_dataset_from_cache(key):
    dataset_bytes = cache.get(key)
    if dataset_bytes:
        # 使用BytesIO读取字节串
        buffer = BytesIO(dataset_bytes)
        return pd.read_pickle(buffer)  # 反序列化为DataFrame
    return None


@execution_time
@api_view(["GET"])
def test(request):
    pass
