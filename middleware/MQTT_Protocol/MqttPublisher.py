# python 3.6

from queue import Queue
import random
import time
import datetime
from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 8080 
# broker='192.168.247.128'
# port=1883
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
    # client = mqtt_client.Client(client_id,transport='websockets')
    client = mqtt_client.Client(client_id,transport="WebSockets")
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,topic,msg,file):
        # msg_count = 0
        time.sleep(0.001)
        # msgs = f"{msg}: {msg_count}"
        result = client.publish(topic, msg,qos=2)
        # result: [0, 1]
        status = result[0]
        if status == 0:
        
         file.write(datetime.datetime.now().isoformat()+" : "+msg+"\n")
        #  print(datetime.datetime.now().isoformat()+" : "+msg)
            # print(f"Send `{msg}` to topic `{topic}`")
         
        else:
            print(f"Failed to send message to topic {topic}")
        # msg_count += 1


def run():
    file=open('TraceFile_PUB.txt',"w")  
    client = connect_mqtt()
    client.loop_start()
    c=0
    service_topic= "melfa/service"
    service_topic1= "melfa/service/baaaaaaaat"
    control_topic= "melfa/control/start"
    control_topic1= "melfa/control/dir8"
    
    while True:
     if(c>500):
        file.close()
        break
     time.sleep(0.001)
     c=c+1
     publish(client,"melfa/monitor/"+"JPOSF"+"/"+str(c),'{"type": "JPOSF", "state": "QoK", "j1": 65.85, "j2": 30.92, "j3": 109.74, "j4": 6.63, "j5": -5.13, "j6": 93.05, "ovrd": ""}',file)

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