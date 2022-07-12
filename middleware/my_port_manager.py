from ast import Break
from multiprocessing import Event
from tkinter import Y
import serial
import serial.tools.list_ports
from time import sleep, perf_counter
from threading import Thread
import threading
import time
import codecs  
import MQTT_Protocol.MqttPublisher
def find_USB_device():
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]


    usb_port_list = [p[0] for p in myports]
    
    return usb_port_list

def get_num_port():
    return  len(find_USB_device())  


#Todo:// Make Port Allocation ........

class _port_manager():
#port getter and setter
  ports_user=""
  ports_melfa=""
  melfa_line=""
  user_line=""
  dtm_rcv=False
  dtu_rcv=False
  timeout=0.05
  writeTimeout=30
  baudrate=9600
  thread_stop=False
  DU_Idle=True;
  # def __init__(self):
  #   #self.OnMessageArrive=Event()
    
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


      return "Melfa port is connected"
    else: 
      #just connect both
      self.start_melfa_port()
      self.start_user_port()
      self.Mthread=threading.Thread(target=self.thread_melfa)
      self.Mthread.start()
      self.Uthread=threading.Thread(target=self.thread_user)
      self.Uthread.start()
      #start reading and writing ...
      return "Melfa and Direct-user ports are connected"


  def thread_melfa(self):
   while True:
   
    if self.thread_stop:
      self.melfa_serial.close()
      break
    else:
      
      rcv=self.melfa_serial.readline()
      rcv_txt=rcv.decode("UTF-8") 
      #rcv_txt=rcv
      #rcv_txt=codecs.decode(rcv,'UTF-8')
      if(rcv_txt!=""):
        self.dtm_rcv=True
        if(self.ports_user==""):

          self.melfa_line=rcv_txt
          print(rcv_txt)
        else:
          self.melfa_line=rcv_txt
          
          self.user_serial.write(rcv)
          print(rcv)
          
      else:
        self.dtm_rcv=False

  # def thread_user_remote(self):
  #  while True:
   
  #   if self.thread_stop:
  #     #self.user_serial.close()
  #     break
  #   else:
      
  #     rcv=self.user_serial.readline()
      
  #     rcv_txt=rcv.decode("UTF-8") 
  #     #Open Du Communication
  #     if(rcv_txt==""):
  #       DU_Idle=False
  #     #Close Du Communication
  #     if(rcv_txt==""):
  #       DU_Idle=True
  #     #rcv_txt=rcv   
  #     #rcv_txt=codecs.decode(rcv,'UTF-8')   
  #     if(rcv_txt!=""):
  #       self.dtu_rcv=True
  #       self.user_line=rcv_txt
  #       self.melfa_serial.write(rcv)
  #       print(rcv)
  #     else:
  #       self.dtu_rcv=False
      
#Define Direct User 
  def thread_user(self):
   while True:
   
    if self.thread_stop:
      self.user_serial.close()
      break
    else:
      
      rcv=self.user_serial.readline()
       
      rcv_txt=rcv.decode("UTF-8") 
      #Open Du Communication
      if(rcv_txt==""):
        DU_Idle=False
      #Close Du Communication
      if(rcv_txt==""):
        DU_Idle=True
      #rcv_txt=rcv   
      #rcv_txt=codecs.decode(rcv,'UTF-8')   
      if(rcv_txt!=""):
        self.dtu_rcv=True
        self.user_line=rcv_txt
        self.melfa_serial.write(rcv)
        print(rcv)
      else:
        self.dtu_rcv=False
      
  #def port_alloc():



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