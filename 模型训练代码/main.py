import json
import time

import torch
import os
from torch import nn
from PIL import Image, ImageFile
from torch.utils.data import Dataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms

json_path = 'data/tile_round1_train_20201231/train_annos.json'  # 测试数据集label地址
imgs_path = 'data/tile_round1_train_20201231/train_imgs'  # 测试数据集图片地址

# 读取json文件
with open(json_path) as message:
    train_message = json.load(message)


# 图片与label匹配函数
def Pipei(img_path):
    for i in train_message:
        if i['name'] == img_path:
            return i['category']


# 数据集
class MyData(Dataset):
    def __init__(self, imgs_path):
        self.imgs_path = imgs_path
        self.imgs_list = os.listdir(imgs_path)

    def __getitem__(self, idx):
        img_name = self.imgs_list[idx]
        img_path = os.path.join(self.imgs_path, img_name)
        totensor = transforms.ToTensor()
        img = Image.open(img_path)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img = img.resize((1639, 1200))
        img = totensor(img)
        label = Pipei(img_name)
        return img, label

    def __len__(self):
        return len(self.imgs_list)


# 神经网络
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


# 准备数据集
train_datas = MyData(imgs_path)
test_datas = MyData(imgs_path)

# 数据集长度
len_train = len(train_datas)
len_test = len(test_datas)

# 利用dataloader来加载数据集
train_dataloader = DataLoader(train_datas, batch_size=4)
test_dataloader = DataLoader(test_datas, batch_size=4)

# 创建网络模型
CNN = CNN()
CNN = CNN.cuda()

# 损失函数
loss_fn = nn.CrossEntropyLoss()
loss_fn = loss_fn.cuda()

# 优化器
learning_rate = 0.01
optimizer = torch.optim.SGD(CNN.parameters(), lr=learning_rate)

# 训练次数
total_train_step = 0
# 图片数量
pic_num = 0
# 正确数量
right_num = 0
# 训练轮数
epoch = 10
# 添加tensonboard
writer = SummaryWriter("logs_train")

for i in range(epoch):
    print("-----------第{}轮训练开始-------------".format(i + 1))

    # 训练步骤开始
    for data in train_dataloader:
        start_time = time.time()
        imgs, targets = data
        print(imgs.shape)
        imgs = imgs.cuda()
        targets = targets.cuda()
        outputs = CNN(imgs)
        print(outputs.argmax(1), targets)
        pic_num += 4
        right_num += (outputs.argmax(1) == targets).sum()
        print("正确率为{}".format(right_num / pic_num))
        loss = loss_fn(outputs, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_train_step += 1
        print("训练次数：{}，loss：{}".format(total_train_step, loss.item()))
        writer.add_scalar("train_loss", loss.item(), total_train_step)
        writer.add_scalar("accuracy", float(right_num / pic_num), total_train_step)
        end_time = time.time()
        print("本次训练用时{}".format(end_time - start_time))

    # 模型的保存
    torch.save(CNN.state_dict(), 'cizhuan_{}.pth'.format(i))
    print("模型已保存")
writer.close()
