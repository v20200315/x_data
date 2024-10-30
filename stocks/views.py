from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import StockHistoryBfq, StockHistoryQfq
from .tasks import fetch_and_save_stock_history
from .temps import _get_stock_history_from_db, _get_stock_history_from_cache


def fetch_stock_history(request):
    if not StockHistoryBfq.objects.exists() and not StockHistoryQfq.objects.exists():
        task = fetch_and_save_stock_history.delay()  # 异步调用任务
        return JsonResponse({"task_id": task.id, "status": "Task is being processed!"})
    return JsonResponse({"status": "no task need to process!"})


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


@api_view(["GET"])
def test(request):
    # _get_stock_history_from_db()
    dataset = _get_stock_history_from_cache()
    print(type(dataset))
    return Response(status=status.HTTP_200_OK)
