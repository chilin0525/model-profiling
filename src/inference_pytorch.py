import numpy as np
import torch
import torchvision
from PIL import Image
from matplotlib import pyplot as plt
from torchvision import transforms
import sys
import os
import torch.nn.functional as F

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
      		std=[0.229, 0.224, 0.225])
])


def write_result(label, output, filename):
    _, index = torch.sort(output, descending=True)
    percentage = F.softmax(output)
    result_torch = [(label[i], percentage[i].item()*100) for i in index[:5]]

    sys.stdout = open("inference_result/pytorch/"+filename, "w+")
    for j in result_torch:
        print("%-25s | %08.5f" % (j[0], j[1])+"%")
    sys.stdout.close()


def main():

    # load ImageNet 1000 label
    with open("ImageNet_label") as f:
        label = [i.split("'")[1] for i in f.readlines()]

    try:
        model_name = "./pretrained_model/pytorch/" + sys.argv[1]
        file_name = sys.argv[2] + "-" + sys.argv[4]
        gpu_idx = sys.argv[3]
    except IndexError:
        print("Index error")
        print("You should input model name as CLI arguments")

    if gpu_idx=="0":
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
    print("FROM inference_pytorch.py: 50, GPU device: ",device)

    img = Image.open('cat.png')
    img = transform(img)
    img = torch.unsqueeze(img, 0)
    img = img.to(device)

    gpu_model = torch.load(str(model_name)+".pt")
    gpu_model.to(device)

    print("="*50)

    output = gpu_model(img)
    output = output.squeeze()
    write_result(label, output, file_name)


if __name__=="__main__":
    main()
