
from operator import index
from re import I
from MQTT_Protocol.MqttConnect import _Connect as subscribe

from time import sleep, perf_counter
from threading import Thread ,Lock
import threading
from ast import Break
from multiprocessing import Event, Lock
from message_manager import message_interpreter as message_interpreter
import time

service_topic= "melfa/service/#"
control_topic= "melfa/control/#"


class mymqtt(subscribe,message_interpreter):

    Remote_user_line=""
    
    def start_mqtt(self):
     
      self.client = self.connect_mqtt()
      self.user_remote_sub()
      self.client.loop_start()
    #   self.RUthread_sub=threading.Thread(target=self.thread_user_remote_sub)
    # #   self.RUthread_pub_m=threading.Thread(target=self.thread_user_remote_monitor_pub)
    #   self.RUthread_sub.start()
    #   self.RUthread_pub_m.start()
    # def thread_user_remote_monitor_pub(self):
    #     if(self.melfa_monitor_line!="" and self.dtmonitor_rcv):
    #         s=1 
    # def make_publish(melfa_line):
    #     if "cmd1" in melfa_line:
    #             s1=1


    def publish(self,topic,msg,qos,delay_time):
        msg_count = 0
        time.sleep(delay_time)
        msgs = f"{msg}: {msg_count}"
        result = self.client.publish(topic, msg,qos)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msgs}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1



    def user_remote_sub(self):

        def on_message(client, userdata, msg):
          if msg.topic=="melfa/control/testsv":
            if not self.du_state:
             self.publish("melfa/message/middleware","Melfa is Online",0,1)
            else:
             self.publish("melfa/message/middleware","melfa has direct user",0,1)
          else:
           self.interpreter(msg)
          
                
        #    elif tmpMSG=="testsv":
        #         self.publish("melfa/message","Melfa is Online",0,1)
           
            
        self.client.subscribe([(service_topic,2),(control_topic,2)])

        self.client.on_message = on_message
        
        # while True:
        #     if self.thread_stop:
        #         self.client.loop_stop()
        #         print("Stop Mqtt Subscriber")
        #         break


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
