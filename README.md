# model-profiling

* The NVIDIA Container Toolkit 
    * [Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
    * [Github repo NVIDIA nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

|model name|model time|gpu type|HtoD|execution time|DtoD|DtoH|runtime|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|googlenet|6.055912 ms|['GeForce RTX 2060 (0)']|2.844639 ms|3.185160 ms|0.007648 ms|0.018465 ms|Pytorch|
|resnet50|18.424824 ms|['GeForce RTX 2060 (0)']|12.564461 ms|5.834091 ms|0.007647 ms|0.018625 ms|Pytorch|
|resnet101|30.756969 ms|['GeForce RTX 2060 (0)']|20.075831 ms|10.655089 ms|0.007519 ms|0.018530 ms|Pytorch|
|googlenet-9|7.135825 ms|['GeForce RTX 2060 (0)']|5.186143 ms|1.600915 ms|0.347424 ms|0.001343 ms|TensorRT|
|resnet50-v1-7|22.124697 ms|['GeForce RTX 2060 (0)']|17.387894 ms|3.511690 ms|1.223161 ms|0.001952 ms|TensorRT|
|resnet101-v1-7|47.378596 ms|['GeForce RTX 2060 (0)']|37.223101 ms|6.692185 ms|3.461422 ms|0.001888 ms|TensorRT|
|googlenet|7.135536 ms|['GeForce RTX 2060 (0)']|5.065822 ms|1.710677 ms|0.357725 ms|0.001312 ms|TensorRT|
|resnet50|22.005743 ms|['GeForce RTX 2060 (0)']|16.928080 ms|3.795649 ms|1.280094 ms|0.001920 ms|TensorRT|
|resnet101|46.448275 ms|['GeForce RTX 2060 (0)']|35.944787 ms|6.984081 ms|3.517135 ms|0.002272 ms|TensorRT|
|googlenet|9.082463 ms|['GeForce GTX 1080 Ti (1)']|4.440801 ms|4.616384 ms|0.007360 ms|0.017918 ms|Pytorch|
|resnet50|21.44728 ms|['GeForce GTX 1080 Ti (1)']|15.858027 ms|5.563778 ms|0.007297 ms|0.018178 ms|Pytorch|
|resnet101|38.115108 ms|['GeForce GTX 1080 Ti (1)']|27.639287 ms|10.451146 ms|0.007648 ms|0.017027 ms|Pytorch|
|googlenet-9|7.940634 ms|['GeForce GTX 1080 Ti (1)']|6.486625 ms|1.082441 ms|0.370416 ms|0.001152 ms|TensorRT|
|resnet50-v1-7|22.649471 ms|['GeForce GTX 1080 Ti (1)']|19.537028 ms|2.233684 ms|0.876263 ms|0.002496 ms|TensorRT|
|resnet101-v1-7|49.527455 ms|['GeForce GTX 1080 Ti (1)']|41.803510 ms|4.868540 ms|2.853677 ms|0.001728 ms|TensorRT|
|googlenet|7.846166 ms|['GeForce GTX 1080 Ti (1)']|6.286488 ms|1.175152 ms|0.383374 ms|0.001152 ms|TensorRT|
|resnet50|22.328749 ms|['GeForce GTX 1080 Ti (1)']|18.896681 ms|2.314972 ms|1.115528 ms|0.001568 ms|TensorRT|
|resnet101|48.357397 ms|['GeForce GTX 1080 Ti (1)']|41.180663 ms|4.258505 ms|2.916661 ms|0.001568 ms|TensorRT|

