import sys
import os 
from colors import bcolors


"""
build tensorRT engine for every ONNX model
"""
def build(models,prefix):
    for model_name in models:
        print(bcolors.OKGREEN+" build " + bcolors.ENDC + model_name)
        build_command = "python3 src/build_engine.py " + prefix + model_name \
                        + " > log/build/" + prefix + model_name +" 2>&1"
        os.system(build_command)        


"""
inference command example: 
    nsys profile -f true -o net --export sqlite python3 src/inference.py resnet50-v1-7 > log/inference/res 2>&1
generate summary of trace reports:
    nsys stats -r gputrace net.qdrep -f json -o ./log/nsys/  --force-overwrite true
"""
def inference(models,prefix):
    for model_name in models:
        build_command = "nsys profile -f true -o net --export sqlite python3 src/inference.py " + \
            prefix+model_name+" > log/inference/"+prefix+model_name+" 2>&1"
        nsys_command = "nsys stats -r gputrace net.qdrep -f json -o ./log/nsys/"+model_name+"  --force-overwrite true"
        print(bcolors.OKGREEN+" inference " + bcolors.ENDC + model_name + ": " + build_command)
        os.system(build_command)
        print(bcolors.OKCYAN +" nsys summary: "+nsys_command)
        os.system(nsys_command)

"""
command:
    onlyinference: show kernel and execution time without MEM copy (HtoD, DtoH, DtoD)
    showall      : show everything including kernel executing and Memory copy
output format:
    <execute time> ns  <kernel name>|<Memory operation>
"""
def nsys_parsing(json_files):
    for json_filename in json_files:
        command = "onlyinference"
        print(bcolors.OKGREEN+" parse nsys "+bcolors.ENDC+json_filename)
        os.system("python3 ./src/nsys_parser.py ./log/nsys/"+json_filename+ \
                  "_gputrace.json ./inference_time/nsys/"+json_filename+"_gputrace " + command)


"""
example command: 
    python3 src/inference_trt_parser.py ./log/inference/ONNX/googlenet-9 > inference_time/TensorRT/googlenet-9
"""
def trt_inference_parsing(prefix, files):
    for file_name in files:
        print(bcolors.OKGREEN+" parse trt "+bcolors.ENDC+file_name)
        os.system("python3 src/inference_trt_parser.py ./log/inference/"+ \
                  prefix+file_name + " > inference_time/TensorRT/"+file_name)

def main():
    prefix_pytorch = "Pytorch/"
    prefix_onnx = "ONNX/"
    model_name_pytorch = ["googlenet", "resnet50", "resnet101"]
    model_name_onnx = ["googlenet-9", "resnet50-v1-7", "resnet101-v1-7"]
    
    build(model_name_pytorch, prefix_pytorch)
    inference(model_name_pytorch, prefix_pytorch)
    build(model_name_onnx,prefix_onnx)
    inference(model_name_onnx, prefix_onnx)
    
    nsys_parsing(model_name_onnx)
    nsys_parsing(model_name_pytorch)

    trt_inference_parsing(prefix_onnx, model_name_onnx)
    trt_inference_parsing(prefix_pytorch, model_name_pytorch)

if __name__=="__main__":
    main()
