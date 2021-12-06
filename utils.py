import subprocess

def get_bluetooth_mac():

    command = "hciconfig"
    completed_process = subprocess.run(command, shell=True, text=True, capture_output=True)
    output = completed_process.stdout
    mac = output.split("Address: ")[1].split()[0]
    return mac


def get_bit(value, n):
    return ((value >> n & 1) != 0)

def set_bit(value, n):
    return value | (1 << n)

def clear_bit(value, n):
    return value & ~(1 << n)