import time

from celery import shared_task


@shared_task
def fetch_and_save_stock_history():
    print("start fetch_and_save_stock_history")
    time.sleep(30)
    # raise Exception("This is a custom exception message.")
    print("end fetch_and_save_stock_history")
    # response = requests.get("https://api.example.com/books")  # 替换为你的第三方接口
    # if response.status_code == 200:
    #     books_data = response.json()
    #     for book in books_data:
    #         Book.objects.create(
    #             title=book["title"],
    #             author=book["author"],
    #             published_date=book["published_date"],
    #         )
