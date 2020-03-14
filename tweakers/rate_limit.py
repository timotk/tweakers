import time


class rate_limit:
    def __init__(self, func):
        self.func = func
        self.last_called = 0
        self.wait_time = 10

    def __call__(self, *args, **kwargs):
        now = time.perf_counter()
        diff = now - self.last_called
        if diff < self.wait_time:
            sleep_time = self.wait_time - diff
            print(f"Rate limited: Waiting for {sleep_time} seconds...")
            time.sleep(sleep_time)

        result = self.func(*args, **kwargs)
        self.last_called = time.perf_counter()
        return result
