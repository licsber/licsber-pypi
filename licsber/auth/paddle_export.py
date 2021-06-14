import os

import paddle as pp

_now_path = os.path.dirname(__file__)
MODEL_NAME = 'final'
MODEL_PATH = os.path.join(_now_path, 'models', f"{MODEL_NAME}.pdopt")
PARAMS_PATH = os.path.join(_now_path, 'models', f"{MODEL_NAME}.pdparams")

CHANNEL, HEIGHT, WIDTH = (3, 34, 92)
CHAR_LIST = '12345678ABCDEFHKNPQXYZabcdefhknpxyz'
YZM_LENGTH = 4

CLASSIFY_NUM = len(CHAR_LIST) + 1
BATCH_SIZE = 5120
LEARNING_RATE = 0.0001
CHANNELS_BASE = 64


class Net(pp.nn.Layer):
    def __init__(self, is_infer: bool = False):
        super().__init__()
        self.is_infer = is_infer

        self.conv1 = pp.nn.Conv2D(in_channels=CHANNEL,
                                  out_channels=CHANNELS_BASE,
                                  kernel_size=3)
        self.bn1 = pp.nn.BatchNorm2D(CHANNELS_BASE)
        self.conv2 = pp.nn.Conv2D(in_channels=CHANNELS_BASE,
                                  out_channels=CHANNELS_BASE * 2,
                                  kernel_size=3,
                                  stride=2)
        self.bn2 = pp.nn.BatchNorm2D(CHANNELS_BASE * 2)
        self.conv3 = pp.nn.Conv2D(in_channels=CHANNELS_BASE * 2,
                                  out_channels=CHANNELS_BASE,
                                  kernel_size=1)
        self.linear = pp.nn.Linear(in_features=660,
                                   out_features=YZM_LENGTH + 4)
        self.lstm = pp.nn.LSTM(input_size=CHANNELS_BASE,
                               hidden_size=CHANNELS_BASE // 2,
                               direction='bidirectional',
                               time_major=True)
        self.linear2 = pp.nn.Linear(in_features=CHANNELS_BASE,
                                    out_features=CLASSIFY_NUM)

    def forward(self, ipt):
        x = self.conv1(ipt)
        x = pp.nn.functional.relu(x)
        x = self.bn1(x)
        x = self.conv2(x)
        x = pp.nn.functional.relu(x)
        x = self.bn2(x)
        x = self.conv3(x)
        x = pp.nn.functional.relu(x)
        x = pp.tensor.flatten(x, 2)
        x = self.linear(x)
        x = pp.nn.functional.relu(x)
        x = x.transpose([2, 0, 1])
        x = self.lstm(x)[0]
        x = self.linear2(x)

        if self.is_infer:
            x = x.transpose([1, 0, 2])
            x = pp.nn.functional.softmax(x)
            x = pp.argmax(x, axis=-1)
        return x


class CTCLoss(pp.nn.Layer):
    def forward(self, ipt, label):
        input_lengths = pp.full(shape=[BATCH_SIZE, 1], fill_value=YZM_LENGTH + 4, dtype='int64')
        label_lengths = pp.full(shape=[BATCH_SIZE, 1], fill_value=YZM_LENGTH, dtype='int64')
        loss = pp.nn.functional.ctc_loss(ipt, label, input_lengths, label_lengths, blank=len(CHAR_LIST))
        return loss


if __name__ == '__main__':
    inputs = pp.static.InputSpec(shape=[-1, CHANNEL, HEIGHT, WIDTH], dtype='float32', name='img')

    net = Net(is_infer=True)
    model_state_dict = pp.load(PARAMS_PATH)
    net.set_state_dict(model_state_dict)

    optimizer = pp.optimizer.Adam(learning_rate=LEARNING_RATE, parameters=net.parameters())
    opt_state_dict = pp.load(MODEL_PATH)
    optimizer.set_state_dict(opt_state_dict)

    net = pp.jit.to_static(net, input_spec=[inputs])
    pp.jit.save(net, 'models/inference')
