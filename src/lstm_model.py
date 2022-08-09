'''
 @author    : Himanshu Mittal
 @contact   : https://www.linkedin.com/in/himanshumittal13/
 @created on: 09-08-2022 10:01:25
'''

import torch

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
n_classes = 16

class GetLSTMFeatures(torch.nn.Module):
    def __init__(self, mode, batch_first=True) -> None:
        super().__init__()
        self.mode = mode
        self.batch_first = batch_first
    def forward(self, x):
        output, (hn, cn) = x
        if self.mode=="full":
            return output
        return output[:,-1,:] if self.batch_first else output[-1,:,:]

lstm_model = torch.nn.Sequential(
    torch.nn.LSTM(input_size=20, hidden_size=64, num_layers=3, dropout=0.2, batch_first=True),
    GetLSTMFeatures(mode="last"),
    torch.nn.Linear(in_features=64, out_features=32),
    torch.nn.ReLU(),
    torch.nn.Linear(in_features=32, out_features=n_classes)
)

# lstm_model = lstm_model.to(device)
