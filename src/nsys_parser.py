import json
import sys
import os


def nsys_parsing(file_name, result_path, command="showall", model_name="", runtime=""):
    with open(file_name,newline='') as jsonfile:
        data = json.load(jsonfile)
    tmp = sys.stdout    
    sys.stdout = open(result_path,"w+")

    total_time = 0.0
    gpu = []
    max_HtoD = 0
    max_DtoD = 0
    max_DtoH = 0
    other = 0.0
    if(command=="showall"):
        for i in data:
            total_time += i["Duration(nsec)"]
            if i["Name"] == "[CUDA memcpy HtoD]":
                max_HtoD += i["Duration(nsec)"]
            elif i["Name"] == "[CUDA memcpy DtoD]":
                max_DtoD += i["Duration(nsec)"]
            elif i["Name"] == "[CUDA memcpy DtoH]":
                max_DtoH += i["Duration(nsec)"]
            else:
                other += i["Duration(nsec)"]
            if i["Device"] not in gpu:
                gpu.append(i["Device"])
            print("%-10s ms, %s" % (str(i["Duration(nsec)"]/1000000.0), i["Name"]))
    
        tmp = sys.stdout
        sys.stdout = open("./inference_time/summary.md", "a+")
        # print("|%s|%s|%s|%s|%s|%s|%s|%s|" % ("model name", "model time","gpu type", "HtoD","execution time", "DtoD", "DtoH", "runtime"))
        # print("|:---:"*8+"|")
        print("|%s|%s ms|%s|%f ms|%f ms|%f ms|%f ms|%s|" % (model_name, str(total_time/1000000.0),
                                                            gpu, max_HtoD/1000000.0, other/1000000.0, max_DtoD/1000000.0, max_DtoH/1000000.0, runtime))
        sys.stdout = tmp

    elif(command=="onlyinference"):
        for i in data:
            if(i["Name"] != "[CUDA memcpy DtoD]" and i["Name"] != "[CUDA memset]" and           \
                i["Name"] != "[CUDA memcpy HtoD]" and i["Name"] != "[CUDA memcpy DtoH]"):
                print("%8s ns  %s" % (str(i["Duration(nsec)"]), i["Name"]))
    
    sys.stdout.close()
    sys.stdout = tmp

if __name__=="__main__":
    try:
        file_name = sys.argv[1]
        result_path = sys.argv[2]
        command = sys.argv[3]
        model_name = sys.argv[4]
        runtime = sys.argv[5]
        nsys_parsing(file_name, result_path, command, model_name, runtime)
    except IndexError:
        print("Index error")
        print("You should input model name as CLI arguments")

