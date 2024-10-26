from django.http import JsonResponse

from .models import StockHistoryQfq
from .tasks import fetch_and_save_stock_history, fetch_and_update_stock_history


def start_fetch_stock_history(request):
    if StockHistoryQfq.objects.exists():
        task = fetch_and_update_stock_history.delay()  # 异步调用任务
    else:
        task = fetch_and_save_stock_history.delay()  # 异步调用任务
    return JsonResponse({"task_id": task.id, "status": "Task is being processed!"})
