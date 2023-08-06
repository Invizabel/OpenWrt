# requiremets:
# TheSilent

import ipaddress
import os
import re
import subprocess
import TheSilent.dolphin_scanner as dolphin
from TheSilent.clear import clear

def elf():
    clear()
    if not os.path.exists("logs"):
        os.makedirs("logs")
    subnet_output = subprocess.getoutput("ip addr")
    subnet = re.findall("\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}/\d{2}", subnet_output)[0]
    for ip in ipaddress.IPv4Network(subnet, strict=False):
        print(f"running dolphin scanner on {ip}")
        dolphin_output = dolphin.dolphin_scanner(str(str(ip)))
        with open(f"logs/devices.txt", "a") as file:
            for mal in dolphin_output:
                file.write(str(ip) + " " + mal + "\n")

elf()
clear()
print("all scans are complete")
