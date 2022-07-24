
from operator import index
from re import I
from MQTT_Protocol.MqttConnect import _Connect as subscribe

from time import sleep, perf_counter
from threading import Thread ,Lock
import threading
from ast import Break
from multiprocessing import Event, Lock
import time

service_topic= "melfa/service/#"
control_topic= "melfa/control/#"
# 2 Topic types must be add Control and service
class message():
    topic=[]
    str_topic=""
    payload=""
    # def __init__(self,topic,str_topic,payload):
    #     self.topic=topic
    #     self.str_topic=str_topic
    #     self.payload=payload
    def clear_message(self):
    
     self.topic=[]
     self.str_topic=""
     self.payload=""

class message_interpreter(message):
   def interpreter(self,msg):
       tmp_topic=msg.topic
    #    tmp_topic=msg
       self.str_topic=tmp_topic
       indexer=0
       ender=len(tmp_topic)-1
       while True:
        
         i=tmp_topic.find("/",indexer,ender)
         if i==-1:
            self.topic.append(tmp_topic[indexer:])
            break
         self.topic.append(tmp_topic[indexer:i])
         indexer=i+1

       print(self.topic)
       self.dispatch()
       self.clear_message()



   def dispatch(self):
       if self.topic[1] =="control":
            self.control_fun_switch()
       else:
            self.monitor_fun_switch()


   
   def control_fun_switch(self):
        
            try:
                self.Remote_user_line="RU-Control-->"+self.topic[2]
                # self.melfa_serial.write(self.Remote_user_line)
                self.dtru_rcv=True
            except:
                self.Remote_user_line="RU Topic Error"
                # self.melfa_serial.write(self.Remote_user_line)
                self.dtru_rcv=True
      
   def monitor_fun_switch(self):
            try:
                self.Remote_user_line="RU-Monitor-->"+self.topic[2]
                # self.melfa_serial.write(self.Remote_user_line)
                self.dtru_rcv=True
            except:
                self.Remote_user_line="RU Topic Error"
                # self.melfa_serial.write(self.Remote_user_line)
                self.dtru_rcv=True
                
     

class mymqtt(subscribe,message_interpreter):

    Remote_user_line=""
    
    def start_mqtt(self):
      self.client = self.connect_mqtt()
      self.RUthread_sub=threading.Thread(target=self.thread_user_remote_sub)
      self.RUthread_pub_m=threading.Thread(target=self.thread_user_remote_monitor_pub)
      self.RUthread_sub.start()
      self.RUthread_pub_m.start()
      
    def thread_user_remote_monitor_pub(self):
        if(self.melfa_monitor_line!="" and self.dtmonitor_rcv):
            s=1 
    def make_publish(melfa_line):
        if "cmd1" in melfa_line:
                s1=1


    def publish(client,topic,msg):
        msg_count = 0
        time.sleep(1)
        msgs = f"{msg}: {msg_count}"
        result = client.publish(topic, msg,)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msgs}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1



    def thread_user_remote_sub(self):
        
        
        def on_message(client, userdata, msg):
            self.interpreter(msg)
        self.client.subscribe([(service_topic,2),(control_topic,2)])

        self.client.on_message = on_message
        self.client.loop_start()
        while True:
            if self.thread_stop:
                self.client.loop_stop()
                print("Stop Mqtt Subscriber")
                break


# if __name__ == '__main__':
# #    st = time.time()
#    m=mymqtt()
#    m.start_mqtt()
#    # get the end time
# #    et = time.time()
#    # get execution time
# #    res = et - st
# #    res=res*1000
# #    print(res)
