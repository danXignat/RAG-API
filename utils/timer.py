import time
import asyncio
from functools import wraps

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        execution_time = end - start
        print( f"{execution_time:.4f} seconds")
        return result
    
    return wrapper

def atimer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        
        time_taken = end_time - start_time
        print(f"{time_taken:.4f} seconds.")
        return result
    return wrapper