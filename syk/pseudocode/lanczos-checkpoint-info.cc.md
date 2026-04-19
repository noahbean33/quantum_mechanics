# lanczos-checkpoint-info.cc — Python Pseudocode

Print Lanczos checkpoint file info (number of completed steps / max steps).

```python
def main():
    """
    Usage: lanczos-checkpoint-info <checkpoint-file> [...]
    For each file, prints: filename: num_steps of max_steps steps
    """
    filenames = sys.argv[1:]

    if len(filenames) == 0:
        print("Usage: lanczos-checkpoint-info lanc-N40-run1-state ...")
        return 1

    for filename in filenames:
        num_steps, max_steps = CudaLanczos.get_state_info(filename)
        print(f"{filename}:  {num_steps} of {max_steps} steps")

    return 0

if __name__ == "__main__":
    main()
```
