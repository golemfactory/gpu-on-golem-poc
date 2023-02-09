Docker image only for testing if GPU support is enabled inside Golem VM.

## Docker build
- You need to first build `maugnorbert/docker_golem_cuda_base` image to be able to build this image.

## Checking 
While in the runtime (using `ya-runtime-dbg`), run `lspci -vnn` and check if GPU is visible on the list. 



