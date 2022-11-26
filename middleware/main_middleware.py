from ast import Num
from asyncio.windows_events import NULL
from functools import cache
from operator import itemgetter
from tkinter import Y
import click
from importlib_metadata import List
import serial
import serial.tools.list_ports
from time import sleep, perf_counter
from threading import Thread ,Lock
import threading
import time
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from MQTT_Protocol.mqtt_manager import mymqtt as mqtt
#inherient from my_port_manager :Check not to take same port
from my_port_manager import _port_manager
import my_port_manager
from SaveCommandManager import _save
from message_manager import message_interpreter as interpreter
class mWindow(QMainWindow,_port_manager,_save,mqtt,interpreter):  
    
    lock_P=Lock()
    def __init__(self):
        title="Melfa Middleware V1"
        self.msg=""
        self.flag_stop=False
        self.flag_terminal=False
        self.list_cmd=[]
        super(mWindow,self).__init__()
        
        #Window Size Here
        self.setFixedSize(640,480)
        # self.setFixedSize(320,240)
        # self.setGeometry(200,200,300,300)
        self.setWindowTitle(title)
        self.initUI()
        try:
         self.load_cmd_from_csv(r'middleware\sample.xlsx')
        except Exception as e:
         print(e)
         self.msg="csv command file not loaded\n"
    def initUI(self):

          lists_ports=my_port_manager.find_USB_device()
          #Refresh button
          
          self.btn_refresh=QtWidgets.QPushButton(self)
          self.btn_refresh.setText("Refresh Middleware")
          self.btn_refresh.setGeometry(200, 150, 120, 50)
          self.btn_refresh.move(260,30)
          self.btn_refresh.setStyleSheet("background-color : #F9D923")
          self.btn_refresh.clicked.connect(self.refresh)
          #Start button
         
          self.btn_start=QtWidgets.QPushButton(self)
          self.btn_start.setText("Start Middleware")
          self.btn_start.setGeometry(200, 150, 120, 50)
          self.btn_start.move(260,90)
          self.btn_start.setStyleSheet("background-color : #76BA99")
          self.btn_start.clicked.connect(self.btnstart)
          #Stop button
         
          self.btn_stop=QtWidgets.QPushButton(self)
          self.btn_stop.setText("Stop Middleware")
          self.btn_stop.setGeometry(200, 150, 120, 50)
          self.btn_stop.move(260,150)
          self.btn_stop.setStyleSheet("background-color : #DA1212")
          self.btn_stop.clicked.connect(self.btnstop)
          # Middleware state label
          self.label_state=QtWidgets.QLabel(self)
          self.label_state.setText("Middleware State")
          self.label_state.setGeometry(410, 70, 300, 100)
          #Check state and the choose color of state 
          # Robo label
          self.label_portr=QtWidgets.QLabel(self)
          self.label_portr.setText("Select Robo Port")
          self.label_portr.move(30,10)
          # Robo Port
          self.list_portsr=QtWidgets.QListWidget(self)
          self.list_portsr.move(30,40)
          self.list_portsr.addItems(lists_ports)
          self.list_portsr.clicked.connect(self.clickedr)
          # Robo label port name <---------------- Here
          self.label_portr_name=QtWidgets.QLabel(self)
          self.label_portr_name.setText("Robo Port")
          self.label_portr_name.move(30,70)
          # user label
          self.label_portu=QtWidgets.QLabel(self)
          self.label_portu.setText("Select Port")
          self.label_portu.move(500,10)
          #User CheckBox
          self.check_user=QtWidgets.QCheckBox("direct user?",self)
          self.check_user.stateChanged.connect(self.btncheck)
          self.check_user.move(410,40)

          #######
          #Use RS232 To Communicate CheckBox
          self.check_user_com=QtWidgets.QCheckBox("DT COM",self)
          self.check_user_com.stateChanged.connect(self.btncheck_COM)
          self.check_user_com.move(410,60)
          #######

          #Monitor CheckBox
          self.check_monitor=QtWidgets.QCheckBox("Is Monitoing?",self)
          self.check_monitor.stateChanged.connect(self.btncheck_Monitor)
          self.check_monitor.move(150,40)
          # User Port
          self.list_portsu=QtWidgets.QListWidget(self)
          self.list_portsu.move(500,40)
          self.list_portsu.addItems(lists_ports)
          self.list_portsu.clicked.connect(self.clickedu)
          self.list_portsu.setEnabled(False)
          ####
          # DT Port
          # self.list_portsDT=QtWidgets.QListWidget(self)
          # self.list_portsDT.move(500,80)
          # self.list_portsDT.addItems(lists_ports)
          # self.list_portsDT.clicked.connect(self.clickedu)
          # self.list_portsDT.setEnabled(False)
          ####
          # User label port name <---------------- Here
          self.label_portu_name=QtWidgets.QLabel(self)
          self.label_portu_name.setText("Port")
          self.label_portu_name.move(500,70)
          #Connection ListVIew
          self.list_connection_command=QtWidgets.QListWidget(self)
          self.list_connection_command.setGeometry(50, 220, 550, 250)
          #Add Comment
          self.Line_Comment=QtWidgets.QLineEdit(self)
          self.Line_Comment.setText(" Add Comment Here")
          self.Line_Comment.setStyleSheet("background-color : #413f42; color:#f2f2f2")
          self.Line_Comment.editingFinished.connect(self.addComment)
          self.Line_Comment.setGeometry(30, 120, 150, 50)
          #Disable Termninal CheckBox
          self.check_terminal=QtWidgets.QCheckBox("Enable Terminal  (it cause low performance !!)",self)
          self.check_terminal.stateChanged.connect(self.btncheck_terminal)
          self.check_terminal.setGeometry(200, 195, 280, 30)
  
    def addComment(self):
      t=self.Line_Comment.text()
      if(t!=""):
        print ("   <== "+self.Line_Comment.text()+ " ==>\n")
          #save to file
        self.save("   <== "+self.Line_Comment.text()+ " ==>\n")
        self.Line_Comment.clear()
        
      else: 
        print ("   <====>   \n")
          #save to file
        self.save("   <====>   \n")
    def clickedr(self, qmodelindex):
      
      item = self.list_portsr.currentItem()
      msg=self.set_port_melfa(item.text())
      if msg=="ok": 
        
        self.label_portr_name.setText(item.text()) 
        self.label_state.setText(msg)     
      else:
        self.label_state.setText(msg)
    
    def clickedu(self, qmodelindex):
      item = self.list_portsu.currentItem()
      msg=self.set_port_user(item.text())
      if msg=="ok":   
        self.label_portu_name.setText(item.text())
        self.label_state.setText(msg)       
      else:
        self.label_state.setText(msg)

    def refresh(self):
         lists_ports=my_port_manager.find_USB_device()
         self.list_portsr.clear()
         self.list_portsu.clear()
         self.list_portsr.addItems(lists_ports)
         self.list_portsu.addItems(lists_ports)
         self.label_state.clear()
         self.label_portr_name.setText("Robo Port")
         self.label_portu_name.setText("User Port")
         self.ports_melfa=""
         self.ports_user=""
         self.list_connection_command.clear()


    def btncheck(self,state):
    
         if state == QtCore.Qt.Checked:
            # print (" is selected")
            # self.direct_user=True
            self.list_portsu.setEnabled(True)
            self.label_portu.setText("Select User Port")
            self.check_user_com.setEnabled(False)
         else:
            # print (" is deselected")
            # self.direct_user=False 
            self.list_portsu.setEnabled(False)
            self.label_portu_name.setText("Port")
            self.check_user_com.setEnabled(True)
     
    def btncheck_Monitor(self,state):
    
         if state == QtCore.Qt.Checked:
            self.flag_isMonitor=True
            
            
         else:
            self.flag_isMonitor=False
          
     
    def btncheck_COM(self,state):
    
         if state == QtCore.Qt.Checked:
            self.flag_isCOM=True
            self.check_user.setEnabled(False)
            self.list_portsu.setEnabled(True)
            self.label_portu.setText("Select DT Port")
         else:
            self.flag_isCOM=False
            self.check_user.setEnabled(True)
            self.list_portsu.setEnabled(False)
            self.label_portu_name.setText("Port")
    def btncheck_terminal(self,state):
    
         if state == QtCore.Qt.Checked:
            self.flag_terminal=True
            self.terminal()
         else:
            self.flag_terminal=False

    def btnstart(self):
      
     if self.ports_melfa=="":
        self.label_state.setText("First choose Robo port please!")
     else:
        #Disable all button ...
        self.btn_refresh.setEnabled(False)
        self.btn_start.setEnabled(False)
        self.check_user.setEnabled(False)
        self.check_user_com.setEnabled(False)
        self.list_portsr.setEnabled(False)
        self.list_portsu.setEnabled(False)
        self.check_monitor.setEnabled(False)
        #make connection and do stuff ...
        self.thread_stop=False
        self.flag_stop=False
        # start HMI terminal view
        self.terminal()
        # start rs232 port manager
        try:
         self.msg=self.msg+self.start_port()
        except:
         self.msg=self.msg+"Serial port ERROR!"
        # now it's time to start Mqtt ...
        try:
         self.start_mqtt()
        except:
         self.msg=self.msg+"\nMQTT Cannot Connectet to broker!"
        # start operation
        self.op_start()
        self.label_state.setText(self.msg)

    def btnstop(self):
      self.thread_stop=True
      self.flag_stop=True
      self.btn_refresh.setEnabled(True)
      self.btn_start.setEnabled(True)
      self.check_user.setEnabled(True)
      self.list_portsr.setEnabled(True)
      self.list_portsu.setEnabled(True)
      try:
       self.client.loop_stop()
      except:
       self.label_state.setText("Middleware is already closed!")
    def terminal(self):
      thread_terminal=threading.Thread(target=self.update_terminal)
      thread_terminal.start()
    def update_terminal(self):
   
        while(True):
          if self.flag_stop or self.flag_terminal==False:
            break
          else: 
             
             if(self.melfa_t_line!=""):
              
              self.list_connection_command.addItem("Robot "+"-->"+self.melfa_t_line)
              #save to file
              self.save("Robot "+"-->"+self.melfa_t_line)
              self.melfa_t_line=""
             
              # time.sleep(self.timeout)
             if (self.user_line!=""):
               self.list_connection_command.addItem("D-U "+"-->"+self.user_line)
               #save to file
               self.save("D-U "+"-->"+self.user_line)
               self.user_line=""
             if (self.Remote_user_line!="" and self.dtru_rcv):
               self.list_connection_command.addItem(self.Remote_user_line)
               #save to file
               self.save(self.Remote_user_line)
               self.Remote_user_line=""
          time.sleep(self.timeout)
             
    def op_start(self):
       monitor_operator_thread=threading.Thread(target=self.thread_monitor_pub)
       monitor_operator_thread.start()
       if self.flag_isCOM:
        Check_DT_thread=threading.Thread(target=self.thread_Check_DT)
        Check_DT_thread.start()
        operator_thread=threading.Thread(target=self.thread_sub_op)
        operator_thread.start()
       if self.ports_user=="":
        self.du_state=False
        operator_thread=threading.Thread(target=self.thread_sub_op)
        operator_thread.start()
       else: 
        self.du_state=True
    
    def thread_sub_op(self):
        while True:
            if self.flag_stop:
              break
            if self.cmds !=[]:
               if not self.du_state or self.flag_isCOM:
                self.remote_user_rcv=True
                self.command_2_port(self.cmds)
                self.remote_user_rcv=False
                self.cmds.clear()
                
    def command_2_port(self,cmds):
        for x in cmds:
            if not self.to_melfa_queue.full():
             self.to_melfa_queue.put(x)
        


             
             
    def thread_Check_DT(self):
      while True:
        if self.flag_stop:
          break     
        time.sleep(0.04)
        if not self.from_DT_queue.empty():
         self.dt_to_cmds(self.from_DT_queue.get())
    
    
    
    def thread_monitor_pub(self):
      last_msg=""
      while True:
        if self.flag_stop:
          break
        # time.sleep(4)
        time.sleep(0.04)
        # self.lock.acquire()
        # if  self.melfa_line!="" and  not self.dtu_rcv:
        if not self.from_melfa_queue.empty() :
          # extract value from melfa response ...
          
          # print(self.melfa_line)
          tmp=self.from_melfa_queue.get()
          
            
          # time.sleep(1)
          json_l=self.extract_cmd(tmp)
          if(self.flag_isCOM):
           line=json_l[1]+'\r\n'
           self.user_serial.write(line.encode("UTF-8"))
          if(json_l[1]!=last_msg):
      
           last_msg=json_l[1]
          # msg=self.melfa_line
          # print("msg :"+msg)
           if json_l[0]=="JPOSF":
             self.publish("melfa/monitor/"+json_l[0],json_l[1],0,0.04)
             self.melfa_line=""
           
          
          # self.melfa_line=""
        # self.lock.release()
        # else:
        
                


 


def window():

    app=QApplication(sys.argv)
    win=mWindow()
    win.show()
    sys.exit(app.exec())





