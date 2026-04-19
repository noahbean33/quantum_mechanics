# helper_cuda.h — Python Pseudocode

NVIDIA CUDA SDK helper: error string lookup and error-checking macros for CUDA Runtime, Driver, cuBLAS, cuSPARSE, cuFFT, cuSOLVER, cuRAND, and NPP APIs.

```python
# This is a vendor-provided utility header from NVIDIA's CUDA SDK samples.
# It maps CUDA/cuBLAS/cuSPARSE/etc. error codes to human-readable strings
# and provides error-checking wrapper macros.

def cuda_get_error_string(error_code: int) -> str:
    """
    Return human-readable string for any CUDA runtime, driver, cuBLAS,
    cuSPARSE, cuFFT, cuSOLVER, cuRAND, or NPP error code.
    Maps ~200+ error codes to their symbolic names.
    """
    ERROR_MAP = {
        0: "cudaSuccess",
        1: "cudaErrorMissingConfiguration",
        2: "cudaErrorMemoryAllocation",
        # ... (large mapping of all CUDA error codes)
    }
    return ERROR_MAP.get(error_code, "<unknown>")

def check_cuda_errors(result, func_name: str, file: str, line: int):
    """
    If result is nonzero, print error and exit.
    Equivalent to: checkCudaErrors(val) macro.
    """
    if result != 0:
        print(f"CUDA error at {file}:{line} code={result}"
              f"({cuda_get_error_string(result)}) \"{func_name}\"")
        exit(1)

def check_cublas_errors(result, func_name: str, file: str, line: int):
    """Same as check_cuda_errors but for cuBLAS return codes."""
    if result != 0:
        print(f"cuBLAS error at {file}:{line} code={result}"
              f"({cuda_get_error_string(result)}) \"{func_name}\"")
        exit(1)

def check_cusparse_errors(result, func_name: str, file: str, line: int):
    """Same as check_cuda_errors but for cuSPARSE return codes."""
    if result != 0:
        print(f"cuSPARSE error at {file}:{line} code={result}"
              f"({cuda_get_error_string(result)}) \"{func_name}\"")
        exit(1)

# Usage (C++ macro equivalents):
# checkCudaErrors(cudaMalloc(...))     → check_cuda_errors(...)
# checkCublasErrors(cublasCreate(...)) → check_cublas_errors(...)
# getLastCudaError("msg")             → check last CUDA error with message
```
