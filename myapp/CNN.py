import torch
from PIL import Image
from torch import nn
from torchvision import transforms


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=(3, 3), padding=2),
            nn.MaxPool2d(kernel_size=(3, 3)),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=(3, 3), padding=2),
            nn.MaxPool2d(kernel_size=(3, 3)),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3), padding=2),
            nn.MaxPool2d(kernel_size=(3, 3)),
            nn.Flatten(),
            nn.Linear(175680, 64),
            nn.Linear(64, 7)
        )

    def forward(self, x):
        x = self.model(x)
        return x


def pic(path):
    img = Image.open(path)
    resize = transforms.Resize((1200, 1639))
    img = resize(img)
    totensor = transforms.ToTensor()
    img = totensor(img)
    img = torch.reshape(img, (1, 3, 1200, 1639))
    cnn = CNN()
    cnn.load_state_dict(torch.load('D:\python\Detection_system\myapp\cizhuan_9.pth'))
    out = cnn(img)
    result = out.argmax(1).tolist()[0]
    # out = out.tolist()[0]
    # probability = {}
    # denominator = 0
    # for i in out:
    #     if i < 0:
    #         denominator += 0
    #     else:
    #         denominator += i
    # for target, value in enumerate(out):
    #     if value < 0:
    #         probability[target] = 0
    #     else:
    #         probability[target] = value / denominator
    return result
