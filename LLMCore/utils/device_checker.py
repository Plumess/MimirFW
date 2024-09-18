import torch

def check_device():
    """
    检测当前可用的设备和后端，返回设备类型和设备列表。
    """
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        device_type = 'cuda'
        devices = [f'cuda:{i}' for i in range(num_gpus)]
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device_type = 'mps'
        devices = ['mps']
    else:
        device_type = 'cpu'
        devices = ['cpu']

    return {'device_type': device_type, 'devices': devices}