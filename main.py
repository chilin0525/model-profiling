import sys
import os 
from colors import bcolors


"""
build tensorRT engine for every ONNX model
"""


def build(models, prefix, gpu_name, gpu_idx):
    for model_name in models:
        build_command = \
            "python3 src/build_engine.py " + prefix + model_name \
            + " " + gpu_idx + " " + gpu_name \
            + " > log/build/" + prefix + model_name \
            + "-" + gpu_name + " 2>&1"
        print(bcolors.OKGREEN+" build " + bcolors.ENDC + model_name + ": ")
        print("       device: "+gpu_name+"("+gpu_idx+")")        
        print("       "+build_command)
        os.system(build_command)        


"""
Pytorch and ONNX pretrained model --> ONNX --> TensorRT engine --> TensorRT inference
inference command example: 
    nsys profile -f true -o net --export sqlite python3 src/inference.py resnet50-v1-7 > log/inference/res 2>&1
generate summary of trace reports:
    nsys stats -r gputrace net.qdrep -f json -o ./log/nsys/  --force-overwrite true
"""


def inference(models, prefix, gpu_name, gpu_idx):
    for model_name in models:
        # 1. do inference and save TensorRT verbose message to ./log/inference
        # 2. use nsys to generate message about kernel exection time and device message
        inference_command = "nsys profile -f true -o net --export sqlite python3 src/inference.py " + \
            prefix+model_name+" "+gpu_idx+ " " + gpu_name + \
            " > log/inference/"+prefix+model_name+"-"+gpu_name+" 2>&1"
        # to summerize nsys message and save to json file
        nsys_command = "nsys stats -r gputrace net.qdrep -f json -o ./log/nsys/"+ model_name + "-" + gpu_name +"  --force-overwrite true"
        print(bcolors.OKGREEN+" inference stage" + bcolors.ENDC)
        print("           model: "+model_name)
        print("           device: "+gpu_name+"("+gpu_idx+")")
        print("           inference command: "+inference_command)
        print("           tensorrt log path: ./log/inference/"+prefix+model_name)
        print("           nsys      command: "+ nsys_command)
        print("           nsys     log path: ./log/nsys/"+ model_name + "-" + gpu_name)
        os.system(inference_command)
        os.system(nsys_command)


"""
Pytorch Pretrained model --> Pytorch inference
execute command: 
    e.q. python3 src/inference_pytorch.py resnet50 a 0 gpu_name
    <python srcript> <model name> <inference result path> <gpu index: 0|1> <gpu_name>
"""


def pytorch_inference(models, gpu_name, gpu_idx):
    for model_name in models:
        inference_command = "nsys profile -f true -o net --export sqlite python3 src/inference_pytorch.py " + \
            model_name + " " + model_name + " " + gpu_idx + " " + gpu_name + \
            " > log/inference/pytorch/"+model_name+"-"+gpu_name+" 2>&1"
        nsys_command = "nsys stats -r gputrace net.qdrep -f json -o ./log/nsys/pytorch/" + \
            model_name + "-" + gpu_name + "  --force-overwrite true"

        print(bcolors.OKGREEN+" inference stage (pytorch runntime)" + bcolors.ENDC)
        print("           model: "+model_name)
        print("           device: "+gpu_name+"("+gpu_idx+")")
        print("           inference command: " + inference_command)
        print("           inference path   : log/inference/pytorch/"+model_name+"-"+gpu_name)
        print("           nsys      command: " + nsys_command)
        print("           nsys      path   : ./log/nsys/pytorch/"+model_name+"-"+gpu_name)
        os.system(inference_command)
        os.system(nsys_command)

"""
execute commnad:
    python3 ./src/nsys_parser.py ./log/nsys/googlenet_gputrace.json ./inference_time/nsys/googlenet_gpu_trace  showall
                                    <filename be parsed>                <result path>                         <command>          
command:
    onlyinference: show kernel and execution time without MEM copy (HtoD, DtoH, DtoD)
    showall      : show everything including kernel executing and Memory copy
output format:
    <execute time> ns  <kernel name>|<Memory operation>
"""


def nsys_parsing(json_files, gpu_name, gpu_idx):
    for json_filename in json_files:
        command = "showall"
        src_path = "./log/nsys/"+json_filename+"-"+gpu_name
        target_path = "./inference_time/nsys/" + json_filename+"-"+gpu_name+"_gputrace"
        print(bcolors.OKGREEN+" parse nsys log: "+bcolors.ENDC, end="")
        print("%50s to %30s" % (src_path, target_path))
        os.system("python3 ./src/nsys_parser.py ./log/nsys/"+json_filename+"-"+gpu_name + \
                  "_gputrace.json ./inference_time/nsys/"+json_filename+"-"+gpu_name+"_gputrace " + command + \
                  " " + json_filename + " " + "TensorRT")


def nsys_pytorch_parsing(json_files, gpu_name, gpu_idx):
    for json_filename in json_files:
        command = "showall"
        src_path = "./log/nsys/pytorch/"+json_filename+"-"+gpu_name
        target_path = "./inference_time/nsys/pytorch/" + json_filename+"-"+gpu_name+"_gputrace"
        print(bcolors.OKGREEN+" parse nsys log: "+bcolors.ENDC, end="")
        print("%50s to %30s" % (src_path, target_path))
        os.system("python3 ./src/nsys_parser.py ./log/nsys/pytorch/"+json_filename+"-"+gpu_name +
                  "_gputrace.json ./inference_time/nsys/pytorch/"+json_filename+"-"+gpu_name+"_gputrace " + command + \
                  " " + json_filename + " " + "Pytorch")


"""
execute command: 
    python3 src/inference_trt_parser.py ./log/inference/ONNX/googlenet-9 > inference_time/TensorRT/googlenet-9
"""


def trt_inference_parsing(prefix, files, gpu_name, gpu_idx):
    for file_name in files:
        src_path = "./log/inference/" + prefix+file_name+"-"+gpu_name
        target_path = "inference_time/TensorRT/"+file_name+"-"+gpu_name
        print(bcolors.OKGREEN+" parse trt  log: "+bcolors.ENDC,end="")
        print("%50s to %30s" % (src_path, target_path))
        os.system("python3 src/inference_trt_parser.py ./log/inference/"+ \
                  prefix+file_name+"-"+gpu_name + " > inference_time/TensorRT/"+file_name+"-"+gpu_name)


def main():

    # set up your GPU info
    # Warning:  using multiple GPU, 
    #           You should to use cudaSetDevice() before calling the builder or deserializing the engine
    gpu= {
        "RTX_2060":"0",
        "GTX_1080_Ti":"1"
    }

    prefix_pytorch = "Pytorch/"
    prefix_onnx = "ONNX/"
    model_name_pytorch = ["googlenet", "resnet50", "resnet101"]
    model_name_onnx = ["googlenet-9", "resnet50-v1-7", "resnet101-v1-7"]
    
    for gpu_name,gpu_idx in gpu.items():
    
        build(model_name_pytorch, prefix_pytorch, gpu_name, gpu_idx)
        inference(model_name_pytorch, prefix_pytorch, gpu_name, gpu_idx)
        build(model_name_onnx, prefix_onnx, gpu_name, gpu_idx)
        inference(model_name_onnx, prefix_onnx, gpu_name, gpu_idx)

        pytorch_inference(model_name_pytorch, gpu_name, gpu_idx)
        nsys_pytorch_parsing(model_name_pytorch, gpu_name, gpu_idx)

        nsys_parsing(model_name_onnx, gpu_name, gpu_idx)
        nsys_parsing(model_name_pytorch, gpu_name, gpu_idx)

        trt_inference_parsing(prefix_onnx, model_name_onnx, gpu_name, gpu_idx)
        trt_inference_parsing(prefix_pytorch, model_name_pytorch, gpu_name, gpu_idx)


    os.system("rm net.qdrep")
    os.system("rm net.sqlite")

if __name__=="__main__":
    main()
