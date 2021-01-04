import json
import time

import requests

from huePyApi import Hue
from config import ip, hue_api_key, webhooks_api_key


def send_request(title, list, time):
    url = "https://maker.ifttt.com/trigger/add_reminder/with/key/" + webhooks_api_key
    data = {"value1": title, "value2": list, "value3": time}
    req = requests.post(url, data=data)

    print(req.text)


def getTimes():
    current_time = time.time()
    current_time_formatted = time.strftime('%H:%M', time.localtime(current_time))

    f = open("last_triggered.txt", "r")
    last_triggered = float(f.read())

    f = open("last_triggered.txt", "w")
    f.write(str(current_time))
    f.close()

    last_triggered_plus_four_hours = last_triggered + (4 * 60)

    return last_triggered, last_triggered_plus_four_hours, current_time_formatted


if __name__ == '__main__':
    hue = Hue.Hue(ip=ip, api_key=hue_api_key)
    temperature = hue.get_sensor(86).get_temperature()

    last_triggered, last_triggered_plus_four_hours, current_time_formatted = getTimes()
    temperature_limit = 2100

    if '06.00' <= current_time_formatted <= '21.30':
        if last_triggered < time.time():
            if temperature > temperature_limit:
                title = 'Temperature is {} °C'.format(temperature / 100)

                send_request(title, "Shortcuts", "now")
