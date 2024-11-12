from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apis.views import CheckTaskStatus
from samples.views import BookViewSet
from stocks.views import (
    fetch_stock_history,
    get_stock_data,
    test,
    get_all_stock_data_by_data_range,
    get_last_trading_date,
)

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("fetch_stock_history/", fetch_stock_history, name="fetch_stock_history"),
    # 根据日期区间获取股票的数据
    path(
        "stock/date_range/",
        get_all_stock_data_by_data_range,
        name="get_all_stock_data_by_data_range",
    ),
    # 根据股票数据的最后一个交易日
    path(
        "stock/last_trading_date/", get_last_trading_date, name="get_last_trading_date"
    ),
    # 获取特定股票的数据
    path("stock/<str:stock_code>/", get_stock_data, name="get_stock_data"),
    path("test", test, name="test"),
    path(
        "check_task/<str:task_id>/",
        CheckTaskStatus.as_view(),
        name="check_task_status",
    ),
]
