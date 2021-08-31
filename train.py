from numpy import mod
import torch
from torchvision import transforms
from dataset_readers.file_dataset import FileDataSet
import torch.nn.functional as F
from tqdm import tqdm
import os
from network_model import create_network

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose([transforms.Resize((160, 120)),
                                transforms.ToTensor()])

train_data = FileDataSet(transform=transform)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=32)

net = create_network()
optimizer = torch.optim.SGD(net.parameters(), lr=0.0002)
loss_func = torch.nn.MSELoss()

if os.path.exists("model.dat"):
    net.load_state_dict(torch.load("model.dat"))

for t in tqdm(range(200)):
    min_loss = 1000

    for train_features, train_labels in tqdm(train_loader):
        train_features = train_features.to(device)
        train_labels = train_labels.to(device)

        prediction = net(train_features)
        loss = loss_func(prediction.float(), train_labels.float())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        min_loss = min(float(loss), min_loss)

    print("loss={loss}".format(loss=min_loss))
    torch.save(net.state_dict(), "model.dat")