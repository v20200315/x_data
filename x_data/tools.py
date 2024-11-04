import time
import pickle
from django.core.cache import cache
from functools import wraps


def execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()  # 记录结束时间
        execution_duration = end_time - start_time  # 计算执行时间
        print(f"执行时间: {execution_duration:.4f}秒")  # 打印执行时间
        return result  # 返回函数结果

    return wrapper


def get_stock_history_from_cache(key):
    if cache.get(key) is None:
        return None
    dataset = pickle.loads(cache.get(key))
    return dataset


def save_stock_history_to_cache(key, dataset):
    cache.set(key, pickle.dumps(dataset), timeout=None)
