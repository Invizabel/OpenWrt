import ipaddress
import os
import re
import subprocess
import TheSilent.dolphin_scanner as dolphin
import TheSilent.melon_scanner as melon
import TheSilent.puppy_requests as puppy
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

        try:
            print(f"getting full path to web page on {ip}")
            history = puppy.history("http://{ip}")
            if len(history) > 0:
                with open(f"logs/devices.txt", "a") as file:
                    for mal in history:
                        file.write(str(ip) + " " + mal + "\n")

                print(f"running sqlmap on {ip}")
                sqlmap_output = subprocess.getoutput(f"sqlmap --url={history[-1]} --random-agent --level=5 --risk=3 --batch --flush-session -o --fingerprint")
                with open(f"logs/devices.txt", "a") as file:
                    file.write(str(ip) + " " + sqlmap_output + "\n")

                print(f"running melon scanner on {ip}")
                melon_output = melon.melon_scanner("{history[-1]}")
                with open(f"logs/devices.txt", "a") as file:
                    for mal in melon_ouput:
                        file.write(str(ip) + " " + mal + "\n")

            else:
                print(f"{ip} supports http/s but no web page was found")
                with open(f"logs/devices.txt", "a") as file:
                    file.write(f"{ip} supports http/s but no web page was found" + "\n")

        except:
            print(f"{ip} doesn't support http/s")
            with open(f"logs/devices.txt", "a") as file:
                file.write(f"{ip} doesn't support http/s" + "\n") 

elf()
clear()
print("all scans are complete")
