import json
import sys

def nsys_parsing(file_name, result_path , command="showall"):
    with open(file_name,newline='') as jsonfile:
        data = json.load(jsonfile)
    tmp = sys.stdout    
    sys.stdout = open(result_path,"w+")
    if(command=="showall"):
        for i in data:
            print(i)
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

