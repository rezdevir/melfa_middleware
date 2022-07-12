from ast import Num

from asyncio.windows_events import NULL
from operator import itemgetter
from tkinter import Y
import click
from importlib_metadata import List
import serial
import serial.tools.list_ports
from time import sleep, perf_counter
from threading import Thread
import threading
import time

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *

#inherient from my_port_manager :Check not to take same port
from my_port_manager import _port_manager
import my_port_manager
from SaveCommandManager import _save
class mWindow(QMainWindow,_port_manager,_save):  
    

    def __init__(self):
        title="Melfa Middleware V1"
        self.flag_stop=False
        super(mWindow,self).__init__()

        #Window Size Here
        self.setFixedSize(640,480)
        # self.setFixedSize(320,240)
        # self.setGeometry(200,200,300,300)
        self.setWindowTitle(title)
        self.initUI()
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
          self.label_state.setGeometry(410, 110, 300, 40)
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
          self.label_portu.setText("Select User Port")
          self.label_portu.move(500,10)
          #User CheckBox
          self.check_user=QtWidgets.QCheckBox("direct user?",self)
          self.check_user.stateChanged.connect(self.btncheck)
          self.check_user.move(410,40)
          # User Port
          self.list_portsu=QtWidgets.QListWidget(self)
          self.list_portsu.move(500,40)
          self.list_portsu.addItems(lists_ports)
          self.list_portsu.clicked.connect(self.clickedu)
          self.list_portsu.setEnabled(False)
          # User label port name <---------------- Here
          self.label_portu_name=QtWidgets.QLabel(self)
          self.label_portu_name.setText("User Port")
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
         else:
            # print (" is deselected")
            # self.direct_user=False
            self.list_portsu.setEnabled(False)
    def btnstart(self):
      if self.ports_melfa=="":
        self.label_state.setText("First choose Robo port please!")
      else:
        #Disable all button ...
        self.btn_refresh.setEnabled(False)
        self.btn_start.setEnabled(False)
        self.check_user.setEnabled(False)
        self.list_portsr.setEnabled(False)
        self.list_portsu.setEnabled(False)
        #make connection and do stuff ...
        self.thread_stop=False
        self.flag_stop=False
        self.terminal()
        msg=self.start_port()
        self.label_state.setText(msg)
    def btnstop(self):
      self.thread_stop=True
      self.flag_stop=True
      ######

      #####
      self.btn_refresh.setEnabled(True)
      self.btn_start.setEnabled(True)
      self.check_user.setEnabled(True)
      self.list_portsr.setEnabled(True)
      self.list_portsu.setEnabled(True)
      
    def terminal(self):
      thread_terminal=threading.Thread(target=self.update_terminal)
      thread_terminal.start()
    def update_terminal(self):
   
        while(True):
          if self.flag_stop:
            break
          else: 
             if(self.melfa_line!="" and self.dtm_rcv):

              self.list_connection_command.addItem("Robot "+"-->"+self.melfa_line)
              #save to file
              self.save("Robot "+"-->"+self.melfa_line)
             if (self.user_line!="" and self.dtu_rcv):
               self.list_connection_command.addItem("D-U "+"-->"+self.user_line)
               #save to file
               self.save("D-U "+"-->"+self.user_line)
             time.sleep(self.timeout)
            




 

def window():

    app=QApplication(sys.argv)
    win=mWindow()
    

  

    win.show()
    sys.exit(app.exec())



if __name__ == "__main__":

   window()


