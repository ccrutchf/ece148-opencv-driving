from torch.utils.data import Dataset
import torch
import numpy as np
import os
import PIL
import pandas as pd

class FileDataSet(Dataset):
    def __init__(self, transform=None):
        self.transform = transform
        self.inputs_frame = pd.read_csv("data/inputs.csv")

    def __len__(self):
        return len(self.inputs_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join("data",
                                str(self.inputs_frame.iloc[idx, 0]) + ".jpg")
        image = PIL.Image.open(img_name)
        if self.transform:
            image = self.transform(image)

        inputs = self.inputs_frame.iloc[idx, 1:].to_numpy()

        return (image, inputs)