#!/bin/python3
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import datetime as dt
import json
import os
import paho.mqtt.client as mqtt
import threading
from tinydb import TinyDB
from dotenv import load_dotenv

load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_PORT = int(os.getenv("MQTT_PORT"))

# Create figure for plotting
fig, ax = plt.subplots(nrows=1, ncols=2)
xs = []
air_temp = []
soil_temp = []
air_humidity = []
soil_humidity = []
is_updated = False
db_timestamp = dt.datetime.now().strftime('%d-%m-%y_%H:%M:%S')

db = TinyDB(f'db_{db_timestamp}.json',
            sort_keys=True, indent=4, separators=(',', ': '))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    global is_updated
    global db

    data = json.loads(str(msg.payload, "UTF-8"))
    print(data)
    readings = data['data']
    if readings["air"]["temp"]:
        air_temp.append(readings["air"]["temp"])

    if readings["soil"]["temp"]:
        soil_temp.append(readings["soil"]["temp"])

    if readings["air"]["humidity"]:
        air_humidity.append(readings["air"]["humidity"])

    if readings["soil"]["humidity"]:
        soil_humidity.append(readings["soil"]["humidity"])

    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    is_updated = True
    db.insert(data)


def add_point(i, xs, air_temp, soil_temp, air_humidity, soil_humidity):
    global is_updated
    if not is_updated:
        return

    xs = xs[-20:]
    air_temp = air_temp[-20:]
    soil_temp = soil_temp[-20:]
    air_humidity = air_humidity[-20:]
    soil_humidity = soil_humidity[-20:]

    # Draw x and y lists
    ax[0].clear()
    ax[0].plot(xs, air_temp)
    ax[0].plot(xs, soil_temp)
    ax[0].set_ylim([15, 25])
    ax[0].set_xticklabels(xs, rotation=45, ha='right')
    ax[0].set_title('Temperature')

    ax[1].clear()
    ax[1].plot(xs, air_humidity,)
    ax[1].plot(xs, soil_humidity)
    ax[1].set_ylim([50, 100])
    ax[1].set_xticklabels(xs, rotation=45, ha='right')
    ax[1].set_title('Humidity')
    is_updated = False


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, port=MQTT_PORT)  # connect to MQTT broke

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(
        fig, add_point, fargs=(xs, air_temp, soil_temp, air_humidity, soil_humidity), interval=1*3*1000)

    th = threading.Thread(target=client.loop_forever, daemon=True)
    th.start()
    plt.show()


if __name__ == "__main__":
    main()
