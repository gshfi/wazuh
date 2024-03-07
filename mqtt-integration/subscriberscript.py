import paho.mqtt.client as paho
import time
import random

broker = "BrokerIP"
port = 1883
topics = [("topic1", 0), ("topic2", 0)]
username = "MqttSubscriberUsername" 
password = "SubscriberPassword"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topics)
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    print(f"Received message from `{msg.topic}` topic\n")
    print(f"`{msg.payload.decode()}`")

def connect_mqtt():
    client = paho.Client(f'python-mqtt-subscriber-{random.randint(0, 1000)}')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(broker, port)
    except Exception as e:
        print(f"An error occurred while connecting to the MQTT broker: {e}")
        return None
    
    return client

def run():
    client = connect_mqtt()
    if client:
        client.loop_forever()
    else:
        print("Failed to create MQTT client.")

if __name__ == '__main__':
    run()
