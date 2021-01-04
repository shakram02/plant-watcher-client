#!/bin/python3
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import datetime as dt
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


# Create figure for plotting
fig, ax = plt.subplots(nrows=1, ncols=2)
xs = []
air_temp = []
soil_temp = []
air_humidity = []
soil_humidity = []


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    global data_frame

    data = json.loads(str(msg.payload, "UTF-8"))
    print(data)
    readings = data['data']
    air_temp.append(readings["air"]["temp"])
    soil_temp.append(readings["soil"]["temp"])

    air_humidity.append(readings["air"]["humidity"])
    soil_humidity.append(readings["soil"]["humidity"])

    updates = pd.json_normalize(data)

    data_frame = data_frame.append(updates)
    cls()
    print(data_frame)


def add_point(i, xs, air_temp, soil_temp, air_humidity, soil_humidity):
    xs = xs[-20:]
    air_temp = air_temp[-20:]
    soil_temp = soil_temp[-20:]
    air_humidity = air_humidity[-20:]
    soil_humidity = soil_humidity[-20:]

    # Draw x and y lists
    ax[0].clear()
    ax[0].plot(xs, air_temp)
    ax[0].plot(xs, soil_temp)

    ax[1].clear()
    ax[1].plot(xs, air_humidity)
    ax[1].plot(xs, soil_humidity)
    plt.pause(1)


# def animate(i, xs, air_temp, soil_temp, air_humidity, soil_humidity):
#     # Read temperature (Celsius) from TMP102
#     # temp_c = round(tmp102.read_temp(), 2)

#     # Add x and y to lists
#     # xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
#     # temps.append(temp_c)

#     # Limit x and y lists to 20 items
#     xs = xs[-20:]
#     air_temp = air_temp[-20:]
#     soil_temp = soil_temp[-20:]
#     air_humidity = air_humidity[-20:]
#     soil_humidity = soil_humidity[-20:]

#     # Draw x and y lists
#     ax[0].clear()
#     ax[0].plot(xs, air_temp)
#     ax[0].plot(xs, soil_temp)

#     ax[1].clear()
#     ax[1].plot(xs, air_humidity)
#     ax[1].plot(xs, soil_humidity)

#     # Format plot
#     plt.xticks(rotation=45, ha='right')
#     # plt.subplots_adjust(bottom=0.30)
#     # plt.title('TMP102 Temperature over Time')
#     # plt.ylabel('Temperature (deg C)')


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, port=MQTT_PORT)  # connect to MQTT broke

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(
        fig, add_point, fargs=(xs, air_temp, soil_temp, air_humidity, soil_humidity), interval=1000)

    plt.show()

    client.loop_forever()


if __name__ == "__main__":
    main()
