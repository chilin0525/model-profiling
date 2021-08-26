import pycuda.autoinit
from torchvision import transforms
from PIL import Image
import pycuda.driver as cuda
import tensorrt as trt
import torch
import numpy as np
import torch.nn.functional as F
import sys


TRT_LOGGER = trt.Logger(trt.Logger.VERBOSE)
trt_runtime = trt.Runtime(TRT_LOGGER)


def load_engine(trt_runtime, plan_path):
   with open(plan_path, 'rb') as f:
       engine_data = f.read()
   engine = trt_runtime.deserialize_cuda_engine(engine_data)
   return engine


def allocate_buffers(engine, batch_size, data_type):
   """
   This is the function to allocate buffers for input and output in the device
   args:
      engine      : The path to the TensorRT engine. 
      batch_size  : The batch size for execution time.
      data_type   : The type of the data for input and output, for example trt.float32. 
   
   return:
      h_input_1   : Input in the host.
      d_input_1   : Input in the device. 
      h_output_1  : Output in the host. 
      d_output_1  : Output in the device. 
      stream      : CUDA stream.
   """

   # Determine dimensions and create page-locked memory buffers (which won't be swapped to disk) to hold host inputs/outputs.
   h_input_1 = cuda.pagelocked_empty(
       batch_size * trt.volume(engine.get_binding_shape(0)), dtype=trt.nptype(data_type))
   h_output = cuda.pagelocked_empty(
       batch_size * trt.volume(engine.get_binding_shape(1)), dtype=trt.nptype(data_type))
   # Allocate device memory for inputs and outputs.
   d_input_1 = cuda.mem_alloc(h_input_1.nbytes)

   d_output = cuda.mem_alloc(h_output.nbytes)
   # Create a stream in which to copy inputs/outputs and run inference.
   stream = cuda.Stream()
   return h_input_1, d_input_1, h_output, d_output, stream


def load_images_to_buffer(pics, pagelocked_buffer):
   preprocessed = np.asarray(pics).ravel()
   np.copyto(pagelocked_buffer, preprocessed)


def do_inference(engine, pics_1, h_input_1, d_input_1, h_output, d_output, stream, batch_size):
   """
   This is the function to run the inference
   Args:
      engine      : Path to the TensorRT engine 
      pics_1      : Input images to the model.  
      h_input_1   : Input in the host         
      d_input_1   : Input in the device 
      h_output_1  : Output in the host 
      d_output_1  : Output in the device 
      stream      : CUDA stream
      batch_size  : Batch size for execution time
   
   Output:
      The list of output images

   """

   load_images_to_buffer(pics_1, h_input_1)

   with engine.create_execution_context() as context:

      """ copy data from host to device """
      cuda.memcpy_htod_async(d_input_1, h_input_1, stream)

      # Run inference.
      context.profiler = trt.Profiler()
      context.execute(batch_size=1, bindings=[int(d_input_1), int(d_output)])

      # Transfer predictions back from the GPU.
      cuda.memcpy_dtoh_async(h_output, d_output, stream)

      # Synchronize the stream
      stream.synchronize()

      # Return the host output.
      return h_output


def main():

    # load ImageNet 1000 label
    with open("ImageNet_label") as f:
        label = [i.split("'")[1] for i in f.readlines()]

    """load tensorRT engine"""
    try:
        trt_path = "./TRT_engine/"+sys.argv[1]+".plan"
    except IndexError:
        print("Index error")
        print("You should input model name as CLI arguments")

    resnet_trt = load_engine(trt_runtime, trt_path)

    host_input, device_input, host_output, device_output, stream = allocate_buffers(
        engine=resnet_trt,
        batch_size=1,
        data_type=trt.float32)

    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225])
    ])

    img = Image.open('cat.png')
    img = transform(img)
    img = torch.unsqueeze(img, 0)

    """ inference """
    output = do_inference(
        engine=resnet_trt,
        pics_1=img,
        h_input_1=host_input,
        d_input_1=device_input,
        h_output=host_output,
        d_output=device_output,
        stream=stream,
        batch_size=1,
    )

    output = torch.tensor(output)
    _, index = torch.sort(output, descending=True)
    percentage = F.softmax(output)

    
    sys.stdout = open("inference_result/"+sys.argv[1],"w+")
    result_trt = [(label[i], percentage[i].item()*100) for i in index[:5]]
    for j in result_trt:
        print("%-25s | %08.5f" % (j[0], j[1])+"%")
    sys.stdout.close()

if __name__=="__main__":
    main()
