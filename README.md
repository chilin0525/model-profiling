# model-profiling

* The NVIDIA Container Toolkit 
    * [Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
    * [Github repo NVIDIA nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

|model name|model time|gpu type|MAX HtoD|MAX DtoD|NAX DtoH|other
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|googlenet-9-RTX_2060|7.135825|['GeForce RTX 2060 (0)']|5.133472 ms|0.042272 ms|0.001343 ms|0.140415 ms|
|resnet50-v1-7-RTX_2060|22.124697|['GeForce RTX 2060 (0)']|17.334518 ms|0.064512 ms|0.001952 ms|0.206175 ms|
|resnet101-v1-7-RTX_2060|47.378596|['GeForce RTX 2060 (0)']|37.170621 ms|0.064223 ms|0.001888 ms|0.183999 ms|
|googlenet-RTX_2060|7.135536|['GeForce RTX 2060 (0)']|5.012895 ms|0.041728 ms|0.001312 ms|0.140030 ms|
|resnet50-RTX_2060|22.005743|['GeForce RTX 2060 (0)']|16.875376 ms|0.071296 ms|0.001920 ms|0.253855 ms|
|resnet101-RTX_2060|46.448275|['GeForce RTX 2060 (0)']|35.891924 ms|0.071136 ms|0.002272 ms|0.253214 ms|
|googlenet-9-GTX_1080_Ti|7.940634|['GeForce GTX 1080 Ti (1)']|6.394525 ms|0.033953 ms|0.001152 ms|0.092323 ms|
|resnet50-v1-7-GTX_1080_Ti|22.649471|['GeForce GTX 1080 Ti (1)']|19.444384 ms|0.042178 ms|0.002496 ms|0.097476 ms|
|resnet101-v1-7-GTX_1080_Ti|49.527455|['GeForce GTX 1080 Ti (1)']|41.710450 ms|0.052930 ms|0.001728 ms|0.097284 ms|
|googlenet-GTX_1080_Ti|7.846166|['GeForce GTX 1080 Ti (1)']|6.194164 ms|0.033729 ms|0.001152 ms|0.064675 ms|
|resnet50-GTX_1080_Ti|22.328749|['GeForce GTX 1080 Ti (1)']|18.804197 ms|0.059074 ms|0.001568 ms|0.123749 ms|
|resnet101-GTX_1080_Ti|48.357397|['GeForce GTX 1080 Ti (1)']|41.087828 ms|0.057858 ms|0.001568 ms|0.123461 ms|
