import json
import random
import sys
import time

from paho.mqtt import client as mqtt_client
from configparser import ConfigParser
from pathlib import Path

# Read config.ini file
config_object = ConfigParser()
path_current_directory = sys.path[1]
print(path_current_directory)
config_object.read(path_current_directory + "/python/python-mqtt/conf/config.ini")

# MQTT Broker
akiroBrokerConfig = config_object["AkiroMQTTConfig"]
broker = akiroBrokerConfig["host"]
port = int(akiroBrokerConfig["port"])
# MQTT Topic
topic = akiroBrokerConfig["publisher_topic"]
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# MQTT Credentials
username = akiroBrokerConfig["username"]
password = akiroBrokerConfig["password"]
# Client Keep Alive time period
keepalive = int(akiroBrokerConfig["keepalive"])
# Quality of Service in which the client publish the data
qos = int(akiroBrokerConfig["qos"])


def connect_mqtt():
    def on_connect(akiro_mqtt_client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Akiro MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    akiro_mqtt_client = mqtt_client.Client(client_id)
    akiro_mqtt_client.username_pw_set(username, password)
    akiro_mqtt_client.on_connect = on_connect
    akiro_mqtt_client.connect(broker, port, keepalive)
    return akiro_mqtt_client


def disconnect_mqtt(akiro_mqtt_client):
    print(f"Mqtt Client got disconnected `{client_id}")
    akiro_mqtt_client.disconnect()


def akiro_publish(akiro_mqtt_client, pub_message):
    result = akiro_mqtt_client.publish(topic, pub_message, qos, False)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{pub_message}` to topic `{topic}` with qos `{qos}`")
    else:
        print(f"Failed to send message to topic `{topic}` with qos `{qos}`")


def start():
    publish_message = {"a": "test"}
    akiro_mqtt_client = connect_mqtt()
    akiro_mqtt_client.loop_start()
    akiro_publish(akiro_mqtt_client, (json.dumps(publish_message)))
    # akiro_client.loop_stop()
    time.sleep(2)
    disconnect_mqtt(akiro_mqtt_client)


if __name__ == '__main__':
    start()
