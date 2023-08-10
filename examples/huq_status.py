import time
import os
import json
from demo_opts import get_device
from luma.core.virtual import terminal
from ina219 import INA219, DeviceRangeError

SHUNT_OHMS = 0.1

def main():
    ina = INA219(SHUNT_OHMS)
    ina.configure()

    while True:
        routes = json.loads(os.popen("ip -j -4 route").read())

        for r in routes:
            if r.get("dev") == "wlan0" and r.get("prefsrc"):
                ip = r['prefsrc']
                continue

        print(f"IP Address: {ip}")
        term = terminal(device, animate=False)
        term.println(f"IP: {ip}")
        term.println(f"Bus V: {ina.voltage():>6.3f}V")
        try:
            term.println(f"Bus I: {ina.current():>6.3f}mA")
            term.println(f"Power: {ina.power():>6.3f}mW")
#            term.println("Shunt V: %.3fmV" % ina.shunt_voltage())
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print(e)


        term.flush()
        time.sleep(5)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
