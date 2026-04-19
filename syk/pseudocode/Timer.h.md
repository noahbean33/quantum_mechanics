# Timer.h — Python Pseudocode

Simple timer class for benchmarking.

```python
import time

class Timer:
    def __init__(self):
        self.begin = time.time()

    def reset(self):
        self.begin = time.time()

    def seconds(self) -> float:
        return time.time() - self.begin

    def msecs(self) -> float:
        return self.seconds() * 1000.0

    def print(self, title=""):
        print(f"{title}That took {self.seconds():.1f} seconds")

    def print_msec(self, title_or_iterations=None):
        if isinstance(title_or_iterations, int):
            ms = self.msecs()
            print(f"That took {ms} msec ({ms / title_or_iterations} msec / iteration)")
        else:
            title = title_or_iterations or ""
            print(f"{title}That took {self.msecs()} msec")
```
