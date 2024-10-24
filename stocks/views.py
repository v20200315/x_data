from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from django.http import JsonResponse
from .tasks import fetch_and_save_stock_history


def start_fetch_stock_history(request):
    task = fetch_and_save_stock_history.delay()  # 异步调用任务
    return JsonResponse({"task_id": task.id, "status": "Task is being processed!"})


class CheckTaskStatus(APIView):
    @staticmethod
    def get(request, task_id):
        task_result = AsyncResult(task_id)

        if task_result.state == "PENDING":
            # 任务尚未完成
            response = {"state": task_result.state, "status": "Pending..."}
        elif task_result.state != "FAILURE":
            # 任务已完成
            response = {
                "state": task_result.state,
                "result": task_result.result,  # 获取任务结果
            }
        else:
            # 任务失败
            response = {
                "state": task_result.state,
                "error": str(task_result.info),  # 获取错误信息
            }

        return Response(response)
