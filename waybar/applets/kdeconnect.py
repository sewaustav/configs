import os
import re

output = os.popen("kdeconnect-cli -a").read()
match = re.search(r"([a-f0-9]{32})", output)
if match:
    device_id = match.group(1)
    print(device_id)
