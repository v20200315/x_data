from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apis.views import CheckTaskStatus
from samples.views import BookViewSet
from stocks.views import fetch_stock_history, get_stock_data, test

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("fetch_stock_history/", fetch_stock_history, name="fetch_stock_history"),
    # GET http://127.0.0.1:8000/api/stock/600519/?start_date=2024-01-01&end_date=2024-10-29
    path("stock/<str:stock_code>/", get_stock_data, name="get_stock_data"),
    path("test", test, name="test"),
    path(
        "check_task/<str:task_id>/",
        CheckTaskStatus.as_view(),
        name="check_task_status",
    ),
]
