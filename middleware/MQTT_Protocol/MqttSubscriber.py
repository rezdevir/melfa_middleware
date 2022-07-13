# python3.6

from http import client
import random

from paho.mqtt import client as mqtt_client


class _Subscriber():
    
    broker = 'broker.emqx.io'
    port = 8083
    #topic = "python_test/mqtt"
    topic = "melfarv1a/Monitorcommand"
    # generate client ID with pub prefix randomly
    client_id = f'python-mqtt-{random.randint(0, 100)}'
    # client_id="clientjs"

    username = 'rezzza'
    password = '222333444'
    def connect_mqtt(self) -> mqtt_client:
     def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

     client = mqtt_client.Client(self.client_id,transport='websockets')
     # client.username_pw_set(username, password)
     client.on_connect = on_connect
     client.connect(self.broker, self.port)
     return client


    # def subscribe(self,client: mqtt_client):
    
    #  def on_message(client, userdata, msg):
    #     print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #     msg.payload.decode()
        
    #  client.subscribe(self.topic)
    #  client.on_message = on_message



    # def run(self):
    #  client = self.connect_mqtt()
    #  #self.subscribe(client)
    #  client.loop_forever()


