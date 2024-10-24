from django.urls import path, include
from rest_framework.routers import DefaultRouter

from samples.views import BookViewSet
from stocks.views import start_fetch_stock_history, CheckTaskStatus

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("stock_history/", start_fetch_stock_history, name="stock_history"),
    path(
        "check_task/<str:task_id>/",
        CheckTaskStatus.as_view(),
        name="check_task_status",
    ),
]
