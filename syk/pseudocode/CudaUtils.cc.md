# CudaUtils.cc — Python Pseudocode

Implementation of CUDA utility functions. See `CudaUtils.h.md` for the full pseudocode.

```python
# All functions, classes, and methods defined in CudaUtils.h.md are implemented here.
# Key implementations:
#   - cuda_get_num_devices, cuda_get_device_memory, cuda_set_device, cuda_get_device
#   - cuda_print_device_properties: prints all GPU device info
#   - cublas_init: creates cuBLAS handle, sets pointer mode to device
#   - cusparse_init: creates cuSPARSE handle, sets pointer mode to device
#   - d_alloc_copy: cudaMalloc + cudaMemcpy H->D
#   - copy_matrix_host_to_device / copy_matrix_device_to_host: column-major memcpy
#   - d_alloc_copy_matrix: alloc + copy Eigen Mat to device
#   - CudaSparseMatrix: alloc CSR arrays, copy to device (sync or async)
#   - CudaHandles: creates cuBLAS + cuSPARSE handles, set_stream
#   - CudaResourceManager: thread-safe pool of handles/streams (uses mutex)
#   - CudaEvent / CudaEvents: create/record/wait/synchronize events
# See CudaUtils.h.md for the complete pseudocode.
```
