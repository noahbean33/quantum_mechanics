# helper_string.h — Python Pseudocode

NVIDIA CUDA SDK helper: command-line argument parsing and file path searching.

```python
import os

def string_remove_delimiter(delimiter: str, s: str) -> int:
    """Return index of first character in s that is not the delimiter."""
    i = 0
    while i < len(s) and s[i] == delimiter:
        i += 1
    return i if i < len(s) - 1 else 0

def get_file_extension(filename: str) -> str:
    """Return the file extension (after last '.')."""
    _, ext = os.path.splitext(filename)
    return ext

def check_cmd_line_flag(argv: list, flag: str) -> bool:
    """Check if --flag or -flag is present in argv."""
    for arg in argv[1:]:
        stripped = arg.lstrip('-')
        if '=' in stripped:
            stripped = stripped[:stripped.index('=')]
        if stripped.lower() == flag.lower():
            return True
    return False

def get_cmd_line_argument_int(argv: list, flag: str) -> int:
    """Get integer value of --flag=value from argv."""
    for arg in argv[1:]:
        stripped = arg.lstrip('-')
        if stripped.lower().startswith(flag.lower()):
            rest = stripped[len(flag):]
            if rest.startswith('='):
                return int(rest[1:])
            elif rest == '':
                return 0
    return 0

def get_cmd_line_argument_float(argv: list, flag: str) -> float:
    """Get float value of --flag=value from argv."""
    for arg in argv[1:]:
        stripped = arg.lstrip('-')
        if stripped.lower().startswith(flag.lower()):
            rest = stripped[len(flag):]
            if rest.startswith('='):
                return float(rest[1:])
    return 0.0

def get_cmd_line_argument_string(argv: list, flag: str) -> str:
    """Get string value of --flag=value from argv."""
    for arg in argv[1:]:
        stripped = arg.lstrip('-')
        if stripped.lower().startswith(flag.lower()):
            rest = stripped[len(flag):]
            if rest.startswith('='):
                return rest[1:]
    return None

def sdk_find_file_path(filename: str, executable_path: str = None) -> str:
    """
    Search for a file in a large set of standard CUDA SDK search paths
    relative to the executable. Returns the first path found, or None.
    """
    search_paths = [
        "./", "./data/", "./src/", "./common/", "./common/data/",
        "../", "../data/", "../src/", "../../", "../../data/",
        # ... many more relative paths up to 5 levels
    ]
    for path in search_paths:
        full = os.path.join(path, filename)
        if os.path.isfile(full):
            return full
    return None
```
