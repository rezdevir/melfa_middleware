from ast import Break, While
from doctest import FAIL_FAST
from multiprocessing import Event, Lock
from queue import Queue 
from tkinter import Y
import serial
import serial.tools.list_ports
from time import sleep, perf_counter
from threading import Thread ,Lock
import threading
import time
import codecs  

def find_USB_device():
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]


    usb_port_list = [p[0] for p in myports]
    
    return usb_port_list

def get_num_port():
    return  len(find_USB_device())  


# subscribe
class _port_manager():
#port getter and setter
  ports_user=""
  ports_melfa=""
  melfa_line=""
  user_line=""
  to_melfa=""
  melfa_t_line=""
  melfa_cmds_monitor=["1;1;STATE\r","1;1;ERRORRD<;0\r"]
  # Remote_user_line=""
  dtm_rcv=False
  dtru_rcv=False
  dtu_rcv=False
  is_monitor=False
  from_melfa_queue=Queue(maxsize=500)
  to_melfa_queue=Queue(maxsize=500)
  
#Use Mutex Lock for Race Condition
  lock=Lock()
  User_timeout=0.001
  timeout=0.04
  writeTimeout=0.02
  User_writeTimeout=30
  MonitorTime=4
  starter=10
  baudrate=9600
  thread_stop=False
  DU_Idle=True
  remote_user_rcv=False

  def put_to_queue(self,msg):
       self.to_melfa_queue.put(msg) 
  # def put_to_melfa(self):
  #      self.melfa_serial.write(self.put_to_melfa())

  #melfa port
  def set_port_melfa(self,mPort):
    return self.check_port(mPort,self.ports_user)
    
  def get_port_melfa(self):
    return self.ports_melfa
  #user Port
  def set_port_user(self,uPort):
    return self.check_port(self.ports_melfa,uPort)

  def get_port_user(self):
    return self.ports_user

        
  def check_port(self,pMelfa,pUser):

      if (pMelfa==""):
        return "Select Robot Port First!"
      if (pMelfa==pUser):
        
        return "Robot port and Direct-User port cannot \nbe the same ! "
      else:
         self.ports_user=pUser
         self.ports_melfa=pMelfa
         #Here We must check athourization of robot and show the poroper message
         return "ok"
  # melfa serial port
  def start_port(self):
    if(self.ports_user==""):
      #connect melfa
      self.start_melfa_port()
      self.Mthread=threading.Thread(target=self.thread_melfa)
      self.Mthread.start()
      self.Uthread=threading.Thread(target=self.thread_user)
      self.Uthread.start()
      self.Mthread_delay=threading.Thread(target=self.thread_delay_monitor)
      self.Mthread_delay.start()
      return "Melfa port is connected"
    else: 
      #just connect both
      self.start_melfa_port()
      self.start_user_port()
      self.Mthread=threading.Thread(target=self.thread_melfa)
      self.Mthread.start()
      self.Uthread=threading.Thread(target=self.thread_user)
      self.Uthread.start()
      self.Mthread_delay=threading.Thread(target=self.thread_delay_monitor)
      self.Mthread_delay.start()
      #start reading and writing ...
      return "Melfa and Direct-user ports are connected"


  def thread_melfa(self):
   while True:

    if self.thread_stop:
        break
    else:
    
      # self.lock.acquire()
      rcv=self.melfa_serial.readline()
      rcv_txt=rcv.decode("UTF-8") 
      
      # self.lock.release()
      if(rcv_txt!=""):
        print(rcv)
        if(self.ports_user==""):
          self.dtm_rcv=True

          # melfa_line clear after write in terminal
          # self.lock.acquire()
          self.melfa_line=rcv.decode("UTF-8")
          
          self.from_melfa_queue.put(rcv.decode("UTF-8"))
          self.melfa_t_line=rcv_txt
          # self.lock.release()
          # self.melfa_t_line=rcv.decode("UTF-8")
          # print(rcv_txt)
        else:
          self.dtm_rcv=True

          # self.lock.acquire()
          self.melfa_line=rcv.decode("UTF-8")
          self.from_melfa_queue.put(rcv.decode("UTF-8"))
          self.user_serial.write(rcv)
          self.melfa_t_line=rcv_txt
          # self.lock.release()
          # self.melfa_t_line=rcv.decode("UTF-8")
          self.dtm_rcv=False
          
      # self.lock.release()


#Define Direct User 
  def thread_user(self):
   rcv_txt=""
   rcv=""
   if self.ports_user=="":
      flag_du=False
   else:
      flag_du=True
   while True:
    if self.thread_stop:
      if flag_du:
        self.user_serial.close()
      break
    else:
  
    # if Direct User (DU) Is available
     if flag_du:
      # Direct User
      # Read From RS232 DUser
      rcv=self.user_serial.readline()
      rcv_txt=rcv.decode("UTF-8") 
      if(rcv_txt!="" ):
        # recive somthing from DU Flag Rcv Must be On (Lock)
        self.dtu_rcv=True
        # Write it On Melfa line
        self.user_line=rcv_txt
        self.melfa_serial.write(rcv)
        self.dtu_rcv=False
        # Unlock Dtu_RCV Flag
      else:
        # if Nothing Came
        # it's Time to monitor
        # Check for Monitor Loop 
        # self.dtu_rcv=False
        if self.is_monitor:
         self.is_monitor=False
         for x in self.melfa_cmds_monitor:
           self.melfa_serial.write(x.encode("UTF-8"))
         
       
        
     else: 
      # Remote User
         if not self.to_melfa_queue.empty():
              rcv=self.to_melfa_queue.get()
              self.dtu_rcv=True
        # Write it On Melfa line
              self.user_line=rcv_txt
              self.melfa_serial.write(rcv)
              self.dtu_rcv=False
         else:
            if self.is_monitor:
               self.Monitor_operation()
            self.dtu_rcv=False


  def Monitor_operation(self):
        
         for x in self.melfa_cmds_monitor:
           self.melfa_serial.write(x.encode("UTF-8"))
         self.is_monitor=False
       
         

         
  def thread_delay_monitor(self):
    while True:
      if self.thread_stop:
        break
      time.sleep(self.MonitorTime) 
      if not self.is_monitor and not self.dtu_rcv:
        self.is_monitor=True

  # def thread_delay_monitor(self):
  #   while True:
  #     if self.thread_stop:
  #       break
  #     time.sleep(self.MonitorTime) 
  #     if  not self.dtu_rcv:
  #       # self.is_monitor=True
  #       self.Monitor_operation()







































  # # get melfa info
  # def thread_melfa_info_get(self):
  #  time.sleep(self.starter)
  #  melfa_cmds_monitor=["1;1;STATE\r","1;1;ERRORRD<;0\r"]
  #  while True:
  #   if self.thread_stop:
  #     break
  #   # Get Melfa command from csv
  #   # it can be retrive it at start time for better performance
  #   # save it in list
   
  #   time.sleep(self.MonitorTime)
  #   for x in melfa_cmds_monitor:
  #    if not self.dtu_rcv and not self.remote_user_rcv:
  #     # time.sleep(self.writeTimeout)
  #     # -12345
  #     # self.melfa_serial.write(x.encode("UTF-8"))
  #     # print(x)
  #     # self.to_melfa_queue.put(x)

  #     # if self.ports_user=="":
  #     # self.melfa_serial.write(x.encode("UTF-8"))
  #     self.to_melfa=x.encode("UTF-8")
  #     #  self.to_melfa_queue.put(x.encode("UTF-8"))
       
  #     # else:
  #     #   self.lock.acquire()
  #     #   self.melfa_serial.write(self.to_melfa_queue.get().encode("UTF-8"))
  #     #   self.lock.release()
  #     # time.sleep(self.timeout)
  #     # self.melfa_monitor_line=self.melfa_serial.readline()
  #     # if self.melfa_monitor_line!="":
  #     #   self.dtmonitor_rcv=True
  #   else:
  #     #   self.dtmonitor_rcv=False
  #     # then call publish func => Publish(rcv)
  #     time.sleep(self.MonitorTime)
    




  # def thread_user_remote(self):
  #    while True:
  #     if self.thread_stop:
  #       break
      

###### -------------PROBLEM-------------
  # def thread_melfa_writer(self):
  #   while True:
  #     if self.thread_stop:
  #       self.melfa_serial.close()
  #       break
  #     if self.to_melfa!="":
  #       # self.lock.acquire()
  #       self.melfa_serial.write(self.to_melfa)
  #       self.to_melfa=""
  #       # self.lock.release()

























  # melfa serial port
  def start_melfa_port(self):
    self.melfa_serial = serial.Serial(
        # Serial Port to read the data from
        port=self.ports_melfa,
 
        #Rate at which the information is shared to the communication channel
        baudrate = self.baudrate,
   
        #Applying Parity Checking (none in this case)
        parity=serial.PARITY_EVEN,
 
        # Pattern of Bits to be read
        stopbits=serial.STOPBITS_TWO,

        # Total number of bits to be read
        bytesize=serial.EIGHTBITS,
        
        # Number of serial commands to accept before timing out
        timeout=self.timeout,
        write_timeout=self.writeTimeout

        )
  # user serial port
  def start_user_port(self):
      self.user_serial = serial.Serial(
        # Serial Port to read the data from
        port=self.ports_user,
 
        #Rate at which the information is shared to the communication channel
        baudrate = self.baudrate,
   
        #Applying Parity Checking (none in this case)
        parity=serial.PARITY_EVEN,
 
        # Pattern of Bits to be read
        stopbits=serial.STOPBITS_TWO,

        # Total number of bits to be read
        bytesize=serial.EIGHTBITS,
        
        # Number of serial commands to accept before timing out
        timeout=self.User_timeout,
        write_timeout=self.User_writeTimeout

        )