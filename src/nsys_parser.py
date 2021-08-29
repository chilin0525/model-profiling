import json
import sys
import os

def nsys_parsing(file_name, result_path , command="showall"):
    with open(file_name,newline='') as jsonfile:
        data = json.load(jsonfile)
    tmp = sys.stdout    
    sys.stdout = open(result_path,"w+")

    total_time = 0.0
    gpu = []
    max_HtoD = 0
    max_DtoD = 0
    max_DtoH = 0
    other = 0
    if(command=="showall"):
        for i in data:
            total_time += i["Duration(nsec)"]
            if i["Name"] == "[CUDA memcpy HtoD]":
                max_HtoD = max(i["Duration(nsec)"], max_HtoD)
            elif i["Name"] == "[CUDA memcpy DtoD]":
                max_DtoD = max(i["Duration(nsec)"], max_DtoD)
            elif i["Name"] == "[CUDA memcpy DtoH]":
                max_DtoH = max(i["Duration(nsec)"], max_DtoH)
            else:
                other = max(i["Duration(nsec)"],other)
            if i["Device"] not in gpu:
                gpu.append(i["Device"])
            print("%-10s ms, %s" % (str(i["Duration(nsec)"]/1000000.0), i["Name"]))
    
        tmp = sys.stdout
        sys.stdout = open("./inference_time/summary.md", "a+")
        # print("|%s|%s|%s|%s|%s|%s|%s" % ("model name", "model time","gpu type", "MAX HtoD", "MAX DtoD", "NAX DtoH","other"))
        # print("|:---:"*7+"|")
        print("|%s|%s|%s|%f ms|%f ms|%f ms|%f ms|" % (file_name.split("/")[3].split("_gputrace")[0], str(total_time/1000000.0),
                                                 gpu, max_HtoD/1000000.0, max_DtoD/1000000.0, max_DtoH/1000000.0, other/1000000.0))
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
        nsys_parsing(file_name, result_path,command)
    except IndexError:
        print("Index error")
        print("You should input model name as CLI arguments")

