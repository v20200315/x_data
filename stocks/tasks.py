from celery import shared_task

from stocks.task_details import (
    init_stock_history,
    update_stock_history,
    real_time_stock,
)


@shared_task
def fetch_and_save_stock_history():
    init_stock_history.run()


@shared_task
def fetch_and_update_stock_history():
    update_stock_history.run()


@shared_task
def fetch_and_save_real_time_stock():
    real_time_stock.run()
