import pyudev

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="input")

for device in iter(monitor.poll, None):
    if device.action in ("add", "remove"):
        print(device.action, device)
