import torch
import torch.nn.functional as F

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden, device=device)
        self.predict = torch.nn.Linear(n_hidden, n_output, device=device)

    def forward(self, x):
        x = torch.flatten(x, 1)

        x = F.relu(self.hidden(x)) # activation function
        x = self.predict(x)
        return x

def create_network():
    return Net(n_feature=160*120*3, n_hidden=100, n_output=2) # network structure
    