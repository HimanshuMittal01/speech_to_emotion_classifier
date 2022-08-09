'''
 @author    : Himanshu Mittal
 @contact   : https://www.linkedin.com/in/himanshumittal13/
 @created on: 09-08-2022 10:02:51
'''

import torch

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
n_classes = 16

cnn_model = torch.nn.Sequential(
    torch.nn.Conv2d(1, 32, 3, 2), # [?,1,128,320] -> [?,32,63,159]
    torch.nn.BatchNorm2d(32),
    torch.nn.ReLU(),
    torch.nn.Conv2d(32, 64, 3, 2), # [?,32,63,159] -> [?,64,31,79]
    torch.nn.BatchNorm2d(64),
    torch.nn.ReLU(),
    torch.nn.MaxPool2d(2), # [?,64,31,79] -> [?,64,15,39]
    torch.nn.Conv2d(64, 128, 3, 2), # [?,64,15,39] -> [?,128,7,19]
    torch.nn.BatchNorm2d(128),
    torch.nn.ReLU(),
    torch.nn.MaxPool2d(2), # [?,128,7,19] -> [?,128,3,9]
    torch.nn.Flatten(),
    torch.nn.Linear(128*3*9, n_classes)
)

# cnn_model = cnn_model.to(device)
