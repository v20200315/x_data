from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apis.views import CheckTaskStatus
from samples.views import BookViewSet
from stocks.views import (
    fetch_stock_history,
    get_stock_history_from_db,
    get_stock_history_from_cache,
)

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("fetch_stock_history/", fetch_stock_history, name="fetch_stock_history"),
    path(
        "get_stock_history_from_db/",
        get_stock_history_from_db,
        name="get_stock_history_from_db",
    ),
    path(
        "get_stock_history_from_cache/",
        get_stock_history_from_cache,
        name="get_stock_history_from_cache",
    ),
    path(
        "check_task/<str:task_id>/",
        CheckTaskStatus.as_view(),
        name="check_task_status",
    ),
]
