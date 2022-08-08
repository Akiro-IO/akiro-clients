import random
import sys
import time

from paho.mqtt import client as mqtt_client
from configparser import ConfigParser
from pathlib import Path

# Read config.ini file
config_object = ConfigParser()
path_current_directory = sys.path[1]
config_object.read(path_current_directory + "/python-mqtt/conf/config.ini")
contents = Path(path_current_directory + "/python-mqtt/conf/sampleMessage.json").read_text()

# MQTT Broker
akiroBrokerConfig = config_object["AkiroMQTTConfig"]
broker = akiroBrokerConfig["host"]
port = int(akiroBrokerConfig["port"])
# MQTT Topic
topic = akiroBrokerConfig["topic"]
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# MQTT Credentials
username = akiroBrokerConfig["username"]
password = akiroBrokerConfig["password"]
# Client Keep Alive time period
keepalive = int(akiroBrokerConfig["keepalive"])
# Quality of Service in which the client publish the data
qos = int(akiroBrokerConfig["qos"])
# Quality of Service in which the client publish the data
message_limit = int(akiroBrokerConfig["message_limit"])


def connect_mqtt():
    def on_connect(akiro_client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Akiro MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    akiro_client = mqtt_client.Client(client_id)
    akiro_client.username_pw_set(username, password)
    akiro_client.on_connect = on_connect
    akiro_client.connect(broker, port, keepalive)
    return akiro_client


def disconnect_mqtt(akiro_client):
    print(f"Mqtt Client got disconnected `{client_id}")
    akiro_client.disconnect()


def akiro_publish(akiro_client):
    msg_count = 0
    while msg_count <= message_limit:
        time.sleep(1)
        msg = contents
        result = akiro_client.publish(topic, msg, qos, False)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}` with qos `{qos}`")
        else:
            print(f"Failed to send message to topic `{topic}` with qos `{qos}`")
        msg_count += 1


def start():
    akiro_client = connect_mqtt()
    akiro_client.loop_start()
    akiro_publish(akiro_client)
    # akiro_client.loop_stop()
    disconnect_mqtt(akiro_client)


if __name__ == '__main__':
    start()
