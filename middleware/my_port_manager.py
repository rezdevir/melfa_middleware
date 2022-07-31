from ast import Break
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

  # melfa_monitor_line=""
  # Remote_user_line=""
  dtm_rcv=False
  dtru_rcv=False
  dtu_rcv=False
  from_melfa_queue=Queue(maxsize=20)
  to_melfa_queue=Queue(maxsize=50)
  
#Use Mutex Lock for Race Condition
  lock=Lock()
  timeout=0.001
  writeTimeout=300
  MonitorTime=2
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
      self.Mthread_writer=threading.Thread(target=self.thread_melfa_writer)
      self.Mthread_writer.start()
      self.Monitorthread=threading.Thread(target=self.thread_melfa_info_get)
      self.Monitorthread.start()
      # if direct user not set then remote user can control the robot
      # self.RUthread=threading.Thread(target=self.thread_user_remote)
      # self.RUthread.start()
      return "Melfa port is connected"
    else: 
      #just connect both
      self.start_melfa_port()
      self.start_user_port()
      self.Mthread=threading.Thread(target=self.thread_melfa)
      self.Mthread.start()
      self.Mthread_writer=threading.Thread(target=self.thread_melfa_writer)
      self.Mthread_writer.start()
      self.Uthread=threading.Thread(target=self.thread_user)
      self.Uthread.start()
      self.Monitorthread=threading.Thread(target=self.thread_melfa_info_get)
      self.Monitorthread.start()
      #start reading and writing ...
      return "Melfa and Direct-user ports are connected"


  def thread_melfa(self):
   while True:

    if self.thread_stop:
        break
    else:
    
      self.lock.acquire()
      rcv=self.melfa_serial.readline()
      rcv_txt=rcv.decode("UTF-8") 
      if(rcv_txt!=""):
        self.dtm_rcv=True
        self.from_melfa_queue.put(rcv)
        if(self.ports_user==""):
          # melfa_line clear after write in terminal
          self.melfa_line=rcv_txt
          print(rcv_txt)
        else:
          self.melfa_line=rcv_txt
          self.user_serial.write(rcv)
          print(rcv)
      else:
        self.dtm_rcv=False
    self.lock.release()
    
    # 
  # def _melfa_port(self,cmd):
  #   # -12345
  #    self.melfa_serial.write(self.put_to_melfa())
  #   #  print(cmd)1


#Define Direct User 
  def thread_user(self):
   rcv_txt=""
   rcv
   if self.ports_user=="":
      flag_du=False
   else:
      flag_du=True
   while True:
    if self.thread_stop:
       if flag_du:
         self.user_serial.close()
         time.sleep(1)
         break
       else:
         time.sleep(1)
         break
    else:
      self.lock.acquire()
      if flag_du:
        rcv=self.user_serial.readline()
        rcv_txt=rcv.decode("UTF-8") 
      if(rcv_txt!="" ):
        self.dtu_rcv=True
       
        self.user_line=rcv_txt
        # write to melfa from queue -12345
        self.to_melfa_queue.put(rcv_txt)
        # self.melfa_serial.write(rcv)
        print(rcv)
      else:
        # if direct user line (serial user) empty then get melfa info
        # self.melfa_info_get()
        self.dtu_rcv=False
      self.lock.release()
      
  # get melfa info
  def thread_melfa_info_get(self):
   
   while True:
    if self.thread_stop:
      break
    # Get Melfa command from csv
    # it can be retrive it at start time for better performance
    # save it in list
    melfa_cmds_monitor=["cmd1","cmd2"]
    for x in melfa_cmds_monitor:
     if not self.dtu_rcv and not self.remote_user_rcv:
      # time.sleep(self.writeTimeout)
      # -12345
      # self.melfa_serial.write(x.encode("UTF-8"))
      self.to_melfa_queue.put(x)
    time.sleep(self.MonitorTime)
      # time.sleep(self.timeout)
      # self.melfa_monitor_line=self.melfa_serial.readline()
      # if self.melfa_monitor_line!="":
      #   self.dtmonitor_rcv=True
      # else:
      #   self.dtmonitor_rcv=False
      # then call publish func => Publish(rcv)
  def thread_melfa_writer(self):
    while True:
      if self.thread_stop:
        self.melfa_serial.close()
        break
      if not self.to_melfa_queue.empty():
        self.melfa_serial.write(self.to_melfa_queue.get().encode("UTF-8"))

























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
        timeout=self.timeout,
        write_timeout=self.writeTimeout

        )