import random
import sys
import time

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
# How many messages to publish
message_limit = int(akiroBrokerConfig["message_limit"])


def connect_mqtt():
    def on_connect(akiro_client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
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


def akiro_subscribe(akiro_mqtt_client: mqtt_client):
    def on_message(akiro_mqtt_client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    akiro_mqtt_client.subscribe(topic, qos)
    print(f"Mqtt Client got subscribed to topic: `{topic}")
    akiro_mqtt_client.on_message = on_message


def akiro_unsubscribe(akiro_mqtt_client: mqtt_client):
    def on_message(akiro_mqtt_client, userdata, msg):
        print("Unsubscribed client!")

    akiro_mqtt_client.unsubscribe(topic)
    akiro_mqtt_client.on_message = on_message


def start():
    akiro_mqtt_client = connect_mqtt()
    # subscribe to the topic
    akiro_subscribe(akiro_mqtt_client)
    # This client will listen to the topic forever
    akiro_mqtt_client.loop_forever()
    # # unsubscribe from the topic
    # akiro_unsubscribe(akiro_mqtt_client)
    # disconnect_mqtt(akiro_mqtt_client)


if __name__ == '__main__':
    start()
