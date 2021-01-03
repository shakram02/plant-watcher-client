#!/bin/python3

import pandas as pd
import json
import paho.mqtt.client as mqtt
import os


MQTT_BROKER = "174.138.103.162"
MQTT_TOPIC = "/hello_world"
MQTT_PORT = 3882
data_frame = pd.DataFrame(columns=[
                          "timestamp",
                          "uuid",
                          "data.air.humidity",
                          "data.air.temp",
                          "data.soil.temp",
                          "data.soil.humidity"]
                          )


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata: pd.DataFrame, msg):
    global data_frame

    data = json.loads(str(msg.payload, "UTF-8"))
    updates = pd.json_normalize(data)

    data_frame = data_frame.append(updates)
    cls()
    print(data_frame)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, port=MQTT_PORT)  # connect to MQTT broke

    client.loop_forever()


if __name__ == "__main__":
    main()
