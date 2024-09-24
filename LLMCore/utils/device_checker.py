def check_device():
    """
    检测当前可用的设备和后端，返回设备类型和设备列表。
    """
    import platform
    import sys
    import torch

    device_info = {}

    # CPU Information
    uname = platform.uname()
    device_info['CPU'] = {}
    device_info['CPU']['Architecture'] = uname.machine

    # Determine CPU Brand and Processor Name
    if sys.platform == 'win32':
        processor_name = platform.processor()
        if 'intel' in processor_name.lower():
            device_info['CPU']['Brand'] = 'Intel'
        elif 'amd' in processor_name.lower():
            device_info['CPU']['Brand'] = 'AMD'
        else:
            device_info['CPU']['Brand'] = 'Others'
        device_info['CPU']['Processor'] = processor_name
    elif sys.platform == 'darwin':
        try:
            import subprocess
            processor_name = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).strip().decode()
            if 'intel' in processor_name.lower():
                device_info['CPU']['Brand'] = 'Intel'
            elif 'apple' in processor_name.lower():
                device_info['CPU']['Brand'] = 'Apple Silicon'
            else:
                device_info['CPU']['Brand'] = 'Others'
            device_info['CPU']['Processor'] = processor_name
        except Exception:
            device_info['CPU']['Brand'] = 'Others'
            device_info['CPU']['Processor'] = 'Unknown'
    elif sys.platform == 'linux':
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            import re
            m = re.search(r'model name\s+:\s+(.+)', cpuinfo)
            if m:
                processor_name = m.group(1)
                if 'intel' in processor_name.lower():
                    device_info['CPU']['Brand'] = 'Intel'
                elif 'amd' in processor_name.lower():
                    device_info['CPU']['Brand'] = 'AMD'
                else:
                    device_info['CPU']['Brand'] = 'Others'
                device_info['CPU']['Processor'] = processor_name
            else:
                device_info['CPU']['Brand'] = 'Others'
                device_info['CPU']['Processor'] = 'Unknown'
        except Exception:
            device_info['CPU']['Brand'] = 'Others'
            device_info['CPU']['Processor'] = 'Unknown'
    else:
        device_info['CPU']['Brand'] = 'Others'
        device_info['CPU']['Processor'] = 'Unknown'

    # GPU Information
    device_info['GPU'] = {}
    device_info['Available Devices'] = []

    # Check for NVIDIA CUDA GPUs
    if torch.cuda.is_available():
        device_info['GPU']['CUDA'] = True
        num_cuda_devices = torch.cuda.device_count()
        device_info['GPU']['CUDA Device Count'] = num_cuda_devices
        device_info['GPU']['CUDA Devices'] = []
        for i in range(num_cuda_devices):
            gpu_name = torch.cuda.get_device_name(i)
            device_info['GPU']['CUDA Devices'].append({'Device Index': i, 'Name': gpu_name})
            device_info['Available Devices'].append(f'cuda:{i}')
    else:
        device_info['GPU']['CUDA'] = False

    # Check for Apple Silicon MPS
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device_info['GPU']['MPS'] = True
        device_info['Available Devices'].append('mps')
    else:
        device_info['GPU']['MPS'] = False

    # Check for AMD ROCm GPUs
    if hasattr(torch.version, 'hip') and torch.version.hip is not None:
        device_info['GPU']['ROCm'] = True
        num_rocm_devices = torch.cuda.device_count()
        device_info['GPU']['ROCm Device Count'] = num_rocm_devices
        device_info['GPU']['ROCm Devices'] = []
        for i in range(num_rocm_devices):
            gpu_name = torch.cuda.get_device_name(i)
            device_info['GPU']['ROCm Devices'].append({'Device Index': i, 'Name': gpu_name})
            device_info['Available Devices'].append(f'rocm:{i}')
    else:
        device_info['GPU']['ROCm'] = False

    # Always include CPU
    device_info['Available Devices'].append('cpu')

    return device_info


# 使用示例
if __name__ == "__main__":
    DEVICE_INFO = check_device()
    print(DEVICE_INFO)