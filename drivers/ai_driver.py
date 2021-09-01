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
        self._laptime_list = []
        self._current_segment = 0
        self._optimizer = torch.optim.SGD(self._net.parameters(), lr=0.2)

        self._segment_count = 64
        self._discount_factor = 0.01

    def get_controls(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with PIL.Image.fromarray(frame) as im:
            tensor = transform(im).to(device)
            tensor = tensor[None, :, :, :]

            results = self._net.forward(tensor)

            return (float(results.data[0, 0]), float(results.data[0, 1]))

    def add_laptime(self, laptime):
        self._laptime_list.append(laptime)

        if len(self._laptime_list) > 4:
            self._laptime_list.pop(0)

        print('saving')
        torch.save(self._net.state_dict(), "model.dat")

    def get_avg_laptime(self):
        if not self._laptime_list:
            return 0

        return sum(self._laptime_list) / len(self._laptime_list)

    def set_track_segment(self, segment):
        self._current_segment = segment

    def get_estimate_laptime_remaining(self, lap_start):
        return (
            self.get_avg_laptime() * float(self._segment_count - self._current_segment) / float(self._segment_count)
        )

    def _loss(self, inv_reward, inv_value):
        result = torch.add(inv_reward, inv_value * self._discount_factor)
        result.requires_grad = True

        return result

    def reinforce(self, inv_reward, inv_value):
        loss = self._loss(inv_reward, inv_value)

        self._optimizer.zero_grad()
        loss.backward()
        self._optimizer.step()