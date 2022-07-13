# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 8083
# topic = "M2MQTT_Unity/test"
# topic = "rrrrwrw/sensor1"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'rezzza'
password = '222333444'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id,transport='websockets')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,topic,msg):
    msg_count = 0
    while True:
        time.sleep(1)
        msgs = f"{msg}: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msgs}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client,"melfarv1a/Monitorcommand","Mohsen ane")


if __name__ == '__main__':
    run()