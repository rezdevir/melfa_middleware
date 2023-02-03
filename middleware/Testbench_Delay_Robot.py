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
import datetime 
from SaveCommandManager import _save



# subscribe
class _port_manager(_save):
#port getter and setter
  tttstop=False
  ports_user=""
  ports_melfa=""
  melfa_line=""
  user_line=""
  to_melfa=""
  melfa_t_line=""
  # ,"1;-1;PPOSF\r","1;-1;JPOSF\r","1;-1;GPPOSF\r","1;-1;GJPOSF\r"
  melfa_cmds_monitor=['{"type": "JPOSF", "state": "QoK", "j1": -23.14, "j2": 23.56, "j3": 97.26, "j4": -13.72, "j5": 31.6, "j6": 93.06, "ovrd": ""}'+'\r\n']
  melfa_MonitorCommand="1;-1;JPOSF\r\n"
  dtm_rcv=False
  dtru_rcv=False
  dtu_rcv=False
  is_monitor=False
  from_melfa_queue=Queue(maxsize=1)
  to_melfa_queue=Queue(maxsize=5)
  from_DT_queue=Queue(maxsize=5)
#Use Mutex Lock for Race Condition
  lock=Lock()
  User_timeout=0.001 #0.001
  timeout=0.04     #0.04
  writeTimeout=1
  User_writeTimeout=30 #30
  MonitorTime=0.1
  delay_starvation=0.208
  starter=5
  baudrate=9600
  thread_stop=False
  DU_Idle=True
  remote_user_rcv=False
  flag_isMonitor=False
  flag_isCOM=False
  counter_m=0
  # def put_to_queue(self,msg):
  #      self.to_melfa_queue.put(msg) 
  #melfa port
  def set_port_melfa(self,mPort):
    return self.check_port(mPort,self.ports_user)
    
  # def get_port_melfa(self):
  #   return self.ports_melfa
  #user Port
  def set_port_user(self,uPort):
    return self.check_port(self.ports_melfa,uPort)

  # def get_port_user(self):
  #   return self.ports_user

        
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
 
  
 


  def thread_melfa(self):
   line = []
   seq = []
   count = 1
   while True:
       
       for c in self.melfa_serial.read(9600):
        line.append(chr(c)) #convert from ANSII
        L_line = ''.join(str(v) for v in line) #Make a string from array
        if chr(c) == '\r':
            print(L_line)
            # self.melfa_line=L_line   
            if(L_line!="QoK"):
             self.from_melfa_queue.put(L_line)
            
            self.melfa_t_line=L_line

            self.dtm_rcv=False
            line = []
            self.melfa_serial.flush()
            break


# #Define Direct User 
#   def thread_user(self):
#    rcv_txt=""
#    rcv=""
#    if not self.ports_user=="" or self.flag_isCOM:
#       flag_du=True
#    else:
#       flag_du=False
#    while True:
#     if self.thread_stop:
#       if flag_du:
#         self.user_serial.close()
#       break
#     else:
  
#     # if Direct User (DU) Is available
#      if flag_du:
#       # Direct User
#       # Read From RS232 DUser
#       rcv=self.user_serial.readline()
#       rcv_txt=rcv.decode("UTF-8") 
#       if(rcv_txt!="" ):
#         # recive somthing from DU Flag Rcv Must be On (Lock)
#         self.dtu_rcv=True
#         # Write it On Melfa line
#         self.user_line=rcv_txt
      
#         self.melfa_serial.write(rcv)
       
#         self.dtu_rcv=False
#         # Unlock Dtu_RCV Flag
#       else:
#         # if Nothing Came
#         # it's Time to monitor
#         # Check for Monitor Loop 
#         if self.is_monitor:
#          self.is_monitor=False
#          for x in self.melfa_cmds_monitor:
#            self.melfa_serial.write(x.encode("UTF-8"))
    
#      else:
#       # Remote User
       
#          time.sleep(self.User_timeout*10)
#          if not self.to_melfa_queue.empty()  :
#               rcvv=self.to_melfa_queue.get()
#               self.dtru_rcv=True
#         # Write it On Melfa line
#               self.user_line=rcv_txt  
#               self.melfa_serial.write(rcvv.encode("UTF-8"))
            
#               self.dtru_rcv=False
       
#          else:
        
#            if self.is_monitor:
#             self.is_monitor=False
            
#             self.melfa_serial.write(self.melfa_MonitorCommand.encode("UTF-8"))

            
  def thread_Remote_monitor(self):
    number=200
    
    print("delay_starvation="+str(self.delay_starvation)+" | Number="+str(number))
    time.sleep(self.starter)
    self.melfa_MonitorCommand="1;1;STATE\r"
    c=0
    while True:
      c=c+1
      if(c>number):
      
       self.tttstop=True
       break
      for x in self.melfa_cmds_monitor:
           self.melfa_MonitorCommand=x 
        #    print(self.melfa_MonitorCommand)
           print(datetime.datetime.now().isoformat()+" : "+self.melfa_MonitorCommand)
           self.melfa_serial.write(self.melfa_MonitorCommand.encode("UTF-8"))
           self.is_monitor=True 
           time.sleep(self.delay_starvation)
        

         
#   def thread_delay_monitor(self):
#     while True:
#       if self.thread_stop:
#         break
#       time.sleep(self.MonitorTime) 
#       if self.dtu_rcv:
#         time.sleep(5) 
    
#       if not self.is_monitor and not self.dtu_rcv:
#           self.is_monitor=True

 
#new method for read from melfa line

  def new_melfa_read_line_method(self):
   
   line = []
   seq = []
   count = 1
   
   while True:
     if self.tttstop:
       break
     else:
      for c in self.melfa_serial.read(9600):
        line.append(chr(c)) #convert from ANSII
        L_line = ''.join(str(v) for v in line) #Make a string from array
        if chr(c) == '\r':
            self.melfa_line=L_line
            # print(L_line)
            if(L_line!="QoK"):
            #  self.from_melfa_queue.put(L_line)
             print(datetime.datetime.now().isoformat()+" : "+L_line)
            
            line = []
            self.melfa_serial.flush()
            break


#   def thread_DT_user(self):
#    if self.ports_user=="":
#       flag_du=False
#    else:
#       flag_du=True
  
#    while True:
#     if self.thread_stop:
#       if flag_du:
#        self.user_serial.close()
#       break
#     else:
#       rcv=self.user_serial.readline()
#       rcv_txt=rcv.decode("UTF-8") 
#       if(rcv_txt!=""):
#         self.melfa_serial.write(rcv)
#       else:
#           if self.is_monitor:
#             self.is_monitor=False
#             self.melfa_serial.write(self.melfa_MonitorCommand.encode("UTF-8"))
#             self.save(datetime.datetime.now().isoformat()+" : "+self.melfa_MonitorCommand)










  # melfa serial port
  def start_melfa_port(self):
    self.melfa_serial = serial.Serial(
        # Serial Port to read the data from
        port="COM2",
 
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
        port="COM3",
 
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




  def start_port(self):
 
      #connect melfa
      self.start_melfa_port()
      # new_melfa_read_line_method
      # self.Mthread=threading.Thread(target=self.thread_melfa)
      # self.Mthread.start()
      self.Mthread=threading.Thread(target=self.new_melfa_read_line_method)
      self.Mthread.start()
    #   self.Uthread=threading.Thread(target=self.thread_user)
    #   self.Uthread.start()
      # self.Mthread_delay=threading.Thread(target=self.thread_delay_monitor)
      # self.Mthread_delay.start()

      self.Mthread_Ch_delay=threading.Thread(target=self.thread_Remote_monitor)
      self.Mthread_Ch_delay.start()

if __name__ == "__main__":
   
#    main_middleware.window()
    print("Start")
   
    port=_port_manager()
    port.start_port()
