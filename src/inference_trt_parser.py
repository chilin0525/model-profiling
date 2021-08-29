import re
import sys

def parsing(file_name):
    with open(file_name, "r") as f:
        data = f.read().split('\n')
    layers = []
    total_time = 0.0
    for i in data:
        if(re.findall("\d+.\d+ms", i) != []):
            layers.append(i)
            total_time += (float(re.findall("\d+.\d+ms", i)[0].split("ms")[0]))
            print("%-12s, %s" % (re.findall("\d+.\d+ms", i)[0], re.split("\d+.\d+ms", i)[0]))

    print("="*50)
    print("summary:")
    print("total time: %f ms" % (total_time))

def main():
    try:
        filename = sys.argv[1]
        parsing(filename)
    except IndexError:
        print("Index error")
        print("check CLI argv")


if __name__=="__main__":
    main()
