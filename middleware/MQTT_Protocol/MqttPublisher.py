# python 3.6

from queue import Queue
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
        time.sleep(1)
        msgs = f"{msg}: {msg_count}"
        result = client.publish(topic, msg,qos=2)
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
    service_topic= "melfa/service"
    service_topic1= "melfa/service/baaaaaaaat"
    control_topic= "melfa/control/start"
    control_topic1= "melfa/control/dir8"
    while True:
     publish(client,control_topic,"Monitorrrr1111111111111")
     publish(client,service_topic,"contriooioll22222222222222222222222")
     publish(client,control_topic1,"Monijiioopyhiotorrr3333333333333333333333333r")
     publish(client,service_topic1,"controioioio44444444444444444444444444444ill")
     publish(client,control_topic,"Monitor55555555555555555555rrr")
     publish(client,service_topic,"contriooiol666666666666666666l")
     publish(client,control_topic,"Monijiioopyhiotorr777777777777777777777777rr")
     publish(client,service_topic,"controioioio8888888888888888888ill")
def testque():
#   que=Queue(maxsize=20)
  que=[]
  que.append(1)
  que.append(2)
  que.append(3)
#   while True:
  for x in que:
    if not que.empty():
     print(que.pop(0))
    else:
     break
    time.sleep(1)
def test():
        client = connect_mqtt()
        client.loop_start()
        control_topic= "melfa/control/start"
        control_topic1= "melfa/control/dir8"
        publish(client,control_topic,"Monitorrrr1111111111111")
        publish(client,control_topic1,"Monitorrrr1111111111111")
if __name__ == '__main__':
    run()
    # testque()
    # test()