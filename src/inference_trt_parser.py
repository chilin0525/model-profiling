import re
import sys

def parsing(file_name):
    with open(file_name, "r") as f:
        data = f.read().split('\n')
    layers = []
    for i in data:
        if(re.findall("\d+.\d+ms", i) != []):
            layers.append(i)
            print("%12s, %s" % (re.findall("\d+.\d+ms", i)[0], re.split("\d+.\d+ms", i)[0]))


def main():
    try:
        filename = sys.argv[1]
        parsing(filename)
    except IndexError:
        print("Index error")
        print("check CLI argv")


if __name__=="__main__":
    main()
