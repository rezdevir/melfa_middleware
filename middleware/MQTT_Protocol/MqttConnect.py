# python3.6

from http import client
import random

from paho.mqtt import client as mqtt_client


class _Connect():
    
    broker = 'broker.emqx.io'
    port = 8083
    # generate client ID with pub prefix randomly
    client_id = f'python-mqtt-{random.randint(0, 100)}'
    username = 'rezzza'
    password = '2223334441'
    def connect_mqtt(self) -> mqtt_client:
     def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker !")
        else:
            print("Failed to connect, return code %d\n", rc)

     client = mqtt_client.Client(self.client_id,transport='websockets')
     client.username_pw_set(self.username, self.password)
     client.on_connect = on_connect
     client.connect(self.broker, self.port)
     return client
