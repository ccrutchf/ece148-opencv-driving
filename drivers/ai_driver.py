from .driver import Driver
from network_model import create_network, device
import torch
from torchvision import transforms
import PIL
import cv2

transform = transforms.Compose([transforms.Resize((160, 120)),
                                transforms.ToTensor()])

class AiDriver(Driver):
    def __init__(self):
        self._net = create_network()
        self._net.load_state_dict(torch.load("model.dat"))

    def get_controls(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with PIL.Image.fromarray(frame) as im:
            tensor = transform(im).to(device)
            tensor = tensor[None, :, :, :]

            results = self._net.forward(tensor)

            return (float(results.data[0, 0]), float(results.data[0, 1]) * 1.2)