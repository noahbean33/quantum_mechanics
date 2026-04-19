# TSVFile.h — Python Pseudocode

Tab-separated file reader with optional bzip2 decompression.

```python
import bz2

class TSVFile:
    """
    A tab-separated file reader. First line is a header (discarded).
    Supports optional bzip2 decompression.

    Usage:
        f = TSVFile(filename)
        while not f.eof():
            i = f.read_int()
            ev = f.read_double()
            # ...
        f.close()
    """
    def __init__(self, filename: str):
        if ".bz2" in filename:
            self._file = bz2.open(filename, 'rt')
        else:
            self._file = open(filename, 'r')
        self._eof = False
        # Discard header line
        self._file.readline()

    def read_int(self) -> int:
        token = self._read_token()
        return int(token) if token is not None else 0

    def read_double(self) -> float:
        token = self._read_token()
        return float(token) if token is not None else 0.0

    def getline(self) -> str:
        return self._file.readline().rstrip('\n')

    def eof(self) -> bool:
        return self._eof

    def close(self):
        self._file.close()

    def _read_token(self):
        # Read next whitespace-delimited token
        token = ""
        while True:
            ch = self._file.read(1)
            if ch == '':
                self._eof = True
                return token if token else None
            if ch in (' ', '\t', '\n', '\r'):
                if token:
                    return token
            else:
                token += ch
```
