# Akiro - MQTT Python Client Example

The example is based on Eclipse Paho Python Client project
## Note on Eclipse Paho
Eclipse Paho is an open source project which provides a number of clients using which one can connect to the server over MQTT messaging protocol. The Paho Python Client provides a client class with support for MQTT v5.0, MQTT v3.1.1, and v3.1 on Python 2.7 or 3.x. It also provides some helper functions to make publishing one off messages to an MQTT server very straightforward.
For complete information on the project : https://www.eclipse.org/paho/index.php?page=clients/python/index.php

## Installation
The Python client can be downloaded and installed from PyPI using the pip tool:
<pre><code>
pip install paho-mqtt
</code></pre>


## Create a Client instance
Create a Client Instance by providing the required parameters.

<pre><code>
<!-- var mqttClient = new Paho.MQTT.Client(mqtt broker ip, broker port, your clientId/deviceId) -->
import paho.mqtt.client as mqtt

akiro_mqtt_client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
</code></pre>

### Client Parameters
Following parameters are supported for creating a client

client_id(type - string) - the unique client id string used when connecting to the broker. If client_id is zero length or None, then one will be randomly generated. In this case the clean_session parameter must be True.
clean_session(type - boolean) - a boolean that determines the client type. If True, the broker will remove all information about this client when it disconnects. If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.
userdata - user defined data of any type that is passed as the userdata parameter to callbacks. It may be updated at a later point with the user_data_set() function.
protocol - the version of the MQTT protocol to use for this client. Can be either MQTTv31 or MQTTv311
transport(type - string) - set to "websockets" to send MQTT over WebSockets. Leave at the default of "tcp" to use raw TCP.

## Set username and password
Set a username and optionally a password for broker authentication. Must be called before connect().

<pre><code>
username = "example"
password = None
akiro_mqtt_client.username_pw_set(username, password)
</code></pre>

## Connect to the Broker
Connect the client to the broker by passing the connection parameters

<pre><code>
akiro_mqtt_client.connect(broker, port, keepalive)
</code></pre>

### Connection Parameters
Following connection parameters are supported

host(type - string) - the hostname or IP address of the remote broker
port(type - number) - the network port of the server host to connect to. Defaults to 1883. Note that the default port for MQTT over SSL/TLS is 8883 so if you are using tls_set() or tls_set_context(), the port may need providing manually
keepalive(type - number) - maximum period in seconds allowed between communications with the broker. If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker

## Callbacks
MQTT Client can be connected by providing the respective callbacks in order to take control on the actions and perform certain business logic.

<pre><code>
def on_connect(akiro_mqtt_client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Akiro MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

def disconnect_mqtt(akiro_mqtt_client):
    print(f"Mqtt Client got disconnected `{client_id}")
    akiro_mqtt_client.disconnect()

def on_message(akiro_mqtt_client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

def akiro_publish(akiro_mqtt_client, pub_message):
	print("Message published!")

def akiro_subscribe(akiro_mqtt_client: mqtt_client):
	print("Subscribed client!")

def akiro_unsubscribe(akiro_mqtt_client: mqtt_client):
	print("Unsubscribed client!")

akiro_mqtt_client.on_connect = on_connect
akiro_mqtt_client.on_disconnect = on_disconnect
akiro_mqtt_client.on_message = on_message
akiro_mqtt_client.on_publish = on_publish
akiro_mqtt_client.on_subscribe = on_subscribe
akiro_mqtt_client.on_unsubscribe = on_unsubscribe

akiro_mqtt_client.connect(broker, port, keepalive)
</code></pre>

## Publish Message to a Topic
Once the connection is successfully established with the Broker, we can now publish message to the required topic. 

<pre><code>
akiro_mqtt_client.publish(topic, msg, qos, False)
</code></pre>

### Publish Parameters

topic - the topic that the message should be published on
payload - the actual message to send. If not given, or set to None a zero length message will be used. Passing an int or float will result in the payload being converted to a string representing that number. If you wish to send a true int/float, use struct.pack() to create the payload you require
qos - the quality of service level to use

<pre><code>
topic = "python/mqtt"
publish_message = {"a": "test"}

message = json.dumps(publish_message)
akiro_mqtt_client.publish(topic, message, 1, False)
</code></pre>

## Subscribe to a Topic
Upon subscribing to a topic, you will start receiving the messages at the callback method configured along with the MQTT Message object.

<pre><code>
akiro_mqtt_client.subscribe(topic, qos)
</code></pre>

### Subscribe Parameters

topic - a string specifying the subscription topic to subscribe to.
qos - the desired quality of service level for the subscription. Defaults to 0.

<pre><code>
topic = "python/mqtt"
akiro_mqtt_client.subscribe(topic,qos)
</code></pre>

## Unsubscribe from a Topic
Unsubscribing from a topic is very similar and simple to subscribe.

<pre><code>
akiro_mqtt_client.unsubscribe(“topic name”)
</code></pre>

## Disconnect
Disconnect the client from the broker using a simple call.

<pre><code>
akiro_mqtt_client.disconnect();
</code></pre>

### Test -
Save both the codes in seperate files and run them 
<pre><code>
python publisher_mqtt.py
python subscriber_mqtt.py
</code></pre>
