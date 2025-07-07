import time
import functools
from collections import deque

def log_calls(file_path="log.txt"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with open(file_path, "a") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Called {func.__name__} with args={args}, kwargs={kwargs}\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def rate_limit(max_calls_per_minute):
    interval = 60
    calls = deque()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            while calls and current_time - calls[0] > interval:
                calls.popleft()

            if len(calls) < max_calls_per_minute:
                calls.append(current_time)
                return func(*args, **kwargs)
            else:
                print("Rate limit exceeded. Try again later.")
        return wrapper
    return decorator # This is to return the decorator function so it can be outputted 

@log_calls()
@rate_limit(max_calls_per_minute=3)
def process_request(user_input):
    print(f"Processing request: {user_input}")

if __name__ == "__main__":
    for i in range(5):
        process_request(f"Request #{i+1}")
        time.sleep(10)  
# This crates the timestamp for the code