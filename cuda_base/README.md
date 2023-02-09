Docker image only for testing if GPU support is enabled inside Golem VM.

## Docker build
- You need to first build `maugnorbert/docker_golem_cuda_base` image to be able to build this image.

## Ready image 
Available at http://gpu-on-golem.s3.eu-central-1.amazonaws.com/golem_cuda_base-d9981476ceecb823bfc3b076f93c65eea608e19dce306b6dc1f6a0ff.gvmi

Hash: d9981476ceecb823bfc3b076f93c65eea608e19dce306b6dc1f6a0ff


## Checking 
While in the runtime (using `ya-runtime-dbg`), run `lspci -vnn` and check if GPU is visible on the list. 



