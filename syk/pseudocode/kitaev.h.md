# kitaev.h — Python Pseudocode

Output classes for writing 2-point function results.

```python
class TwoPointOutput:
    """Abstract base for writing 2-point correlator data."""
    def write(self, T: float, t: float, correlator: complex):
        raise NotImplementedError
    def close(self):
        raise NotImplementedError

class TwoPointFileOutput(TwoPointOutput):
    """Writes 2-point correlator data to a file."""
    def __init__(self, filename: str):
        self.file = open(filename, 'w')
        self.file.write("# T t Re(<c*(t)c(0)>) Im(<c*(t)c(0)>) |<c*(t)c(0)>|^2\n")

    def write(self, T: float, t: float, correlator: complex):
        self.file.write(
            f"{T}\t{t}\t{correlator.real}\t{correlator.imag}"
            f"\t{abs(correlator)**2}\n"
        )

    def close(self):
        self.file.close()

class TwoPointNullOutput(TwoPointOutput):
    """Discards all output (null sink)."""
    def write(self, T, t, correlator):
        pass
    def close(self):
        pass
```
