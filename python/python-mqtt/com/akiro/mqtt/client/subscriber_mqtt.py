import random
import sys

from paho.mqtt import client as mqtt_client

from configparser import ConfigParser

# Read config.ini file
path_current_directory = sys.path[1]
config_object = ConfigParser()
config_object.read(path_current_directory + "/python-mqtt/conf/config.ini")

# Akiro MQTT Broker
akiroBrokerConfig = config_object["AkiroMQTTConfig"]
broker = akiroBrokerConfig["host"]
port = int(akiroBrokerConfig["port"])
# MQTT Topic
topic = akiroBrokerConfig["topic"]
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# Akiro MQTT Credentials
username = akiroBrokerConfig["username"]
password = akiroBrokerConfig["password"]
# Client Keep Alive time period
keepalive = int(akiroBrokerConfig["keepalive"])
# Quality of Service in which the client publish the data
qos = int(akiroBrokerConfig["qos"])


def connect_mqtt():
    def on_connect(akiro_client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
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


def akiro_subscribe(akiro_client: mqtt_client):
    def on_message(akiro_client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    akiro_client.subscribe(topic, qos)
    akiro_client.on_message = on_message


def akiro_unsubscribe(akiro_client: mqtt_client):
    def on_message(akiro_client, userdata, msg):
        print("Unsubscribed client!")

    akiro_client.unsubscribe(topic)
    akiro_client.on_message = on_message


def start():
    akiro_client = connect_mqtt()
    akiro_subscribe(akiro_client)
    akiro_unsubscribe(akiro_client)
    # akiro_client.loop_forever()
    disconnect_mqtt(akiro_client)


if __name__ == '__main__':
    start()
