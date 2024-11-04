from datetime import datetime, timedelta

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from x_data.tools import (
    execution_time,
    get_stock_history_from_cache,
    save_stock_history_to_cache,
)
from .models import StockHistoryBfq, StockHistoryQfq
from .tasks import (
    fetch_and_save_stock_history,
    fetch_and_save_real_time_stock,
    fetch_and_update_stock_history,
)
from .temps import _get_stock_history_from_db, _get_stock_history_from_cache


def fetch_stock_history(request):
    if not StockHistoryBfq.objects.exists() and not StockHistoryQfq.objects.exists():
        task = fetch_and_save_stock_history.delay()  # 异步调用任务
        return JsonResponse({"task_id": task.id, "status": "Task is being processed!"})
    return JsonResponse({"status": "no task need to process!"})


@api_view(["GET"])
def get_stock_data(request, stock_code):
    print("start get_stock_data")
    # 根据股票代码从数据库中获取数据
    stock_data = StockHistoryQfq.objects.filter(stock_code=stock_code).order_by(
        "-trading_date"
    )

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


@execution_time
@api_view(["GET"])
def get_all_stock_data_by_data_range(request):
    # 从请求中获取参数
    from_date = request.GET.get("from", None)
    to_date = request.GET.get("to", None)

    key = f"{from_date}_{to_date}_stock_history"
    cache_data = get_stock_history_from_cache(key)
    if cache_data is not None:
        return Response(cache_data, status=status.HTTP_200_OK)

    # 检查参数的有效性
    if not from_date and not to_date:
        # 如果没有提供任何日期，默认获取过去两个月的数据
        to_date = datetime.now().date()
        from_date = to_date - timedelta(days=60)
    elif (from_date and not to_date) or (not from_date and to_date):
        # 如果只提供了一个日期，返回错误
        return Response({"error": "必须同时提供 'from' 和 'to' 日期"}, status=400)

    try:
        # 将字符串日期转换为日期对象
        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        # 查询在日期区间内的所有股票数据
        stock_data = StockHistoryQfq.objects.filter(
            trading_date__range=(from_date, to_date)
        )

        # 将查询结果转为字典格式
        data = [
            {
                "trading_date": sd.trading_date,
                "stock_code": sd.stock_code,
                "opening_price": sd.opening_price,
                "closing_price": sd.closing_price,
                "highest_price": sd.highest_price,
                "lowest_price": sd.lowest_price,
                "trading_volume": sd.trading_volume,
                "trading_amount": sd.trading_amount,
                "price_range": sd.price_range,
                "price_change_percentage": sd.price_change_percentage,
                "price_change_amount": sd.price_change_amount,
                "turnover_rate": sd.turnover_rate,
            }
            for sd in stock_data
        ]

        save_stock_history_to_cache(key, data)

        return Response(data, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "日期格式不正确，应为 YYYY-MM-DD"}, status=400)


@api_view(["GET"])
def test(request):
    # _get_stock_history_from_db()
    # dataset = _get_stock_history_from_cache()
    # print(type(dataset))
    fetch_and_update_stock_history()
    return Response(status=status.HTTP_200_OK)
