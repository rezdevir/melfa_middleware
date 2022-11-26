# 2 Topic types must be add Control and service
from asyncio import all_tasks
import zlib
import pandas as pd
import re
from asyncio.windows_events import NULL
import json 

class _command():
    def __init__(self,topic,cmd):
     self.topic=topic
     self.cmd=cmd
    def get_cmd(self,topic):
        if self.topic== topic:
            return self.cmd
        else:
            return ""
    def get_topic(self,cmd):
        if self.cmd== cmd:
            return self.topic
        else:
            return ""

class _PPOSF():  
    # type="PPOSF"
    # state="state"
    # x=""
    # y=""
    # z=""
    # a=""
    # b=""
    # c=""
    def __init__(self,state,x,y,z,a,b,c,ovrd):
        self.type="PPOSF"
        self.state=state
        self.x=x
        self.y=y
        self.z=z
        self.a=a
        self.b=b
        self.c=c
        # Two Empty
        self.ovrd=ovrd
        # two empy
    def getJson(self):
        if self.x is not NULL:
         return  json.dumps(self.__dict__)
    def isEmpty_(self):
        if self.x is not NULL:
            return False
        else :
            return True
    # def getx(self):
    #     return self.x
class _JPOSF():  
    def __init__(self,state,j1,j2,j3,j4,j5,j6,ovrd):
        self.type="JPOSF"
        self.state=state
        self.j1=j1
        self.j2=j2
        self.j3=j3
        self.j4=j4
        self.j5=j5
        self.j6=j6
        # Two Empty
        self.ovrd=ovrd
        # two Empty
    def getJson(self):
        if self.j1 is not NULL:
         return  json.dumps(self.__dict__)
    def isEmpty_(self):
        if self.j1 is not NULL:
            return False
        else :
            return True


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

class message_interpreter(message,_command,_PPOSF,_JPOSF):
   cmds=[]
   list_cmds=[]
   du_state=False

   def interpreter(self,msg):
    if not self.du_state:
   
       tmp_topic=msg.topic
       self.payload=msg.payload.decode("utf-8")
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
    #    print(self.topic)
      #  if self.topic[2]!="testsv":
       self.dispatch()
       self.clear_message()
       return "ok"
      #  else:
      #   self.clear_message()
      #   return "testsv"
    else:
      #   self.cmds=["middleware","error","1","Direct user detected"]
       return ""

   def load_cmd_from_csv(self,csvfile):
      data = pd.read_excel(csvfile)
      df = pd.DataFrame(data)
      for x in df.index:
         self.list_cmds.append(_command(df['topic'][x],df['command'][x]))

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
                # for x in self.list_cmds:
                #    tmp=x.get_cmd(self.topic[2])
                #    if(tmp!=""):
                #      # print (tmp)
                #      tmpcmd.append(tmp)
                self.cmds=self.topic_to_cmds()
                
            except:
                self.Remote_user_line="RU Topic Error"
                # self.melfa_serial.write(self.Remote_user_line)
                self.dtru_rcv=True
   ########     
       
   def dt_to_cmds(self,dtMsg):
        tmpcmd=[]
        for x in self.list_cmds:
            tmp=x.get_cmd(dtMsg)
            if tmp!="":
              tmpcmd.append(tmp+"\r")
        return tmpcmd 

   ########

   def monitor_fun_switch(self):
             try:
                self.Remote_user_line="RU-Monitor-->"+self.topic[2]
                # self.melfa_serial.write(self.Remote_user_line)
               
                self.dtru_rcv=True
                
             except:
                self.Remote_user_line="RU Topic Error"
                # self.melfa_serial.write(self.Remote_user_line)
                self.dtru_rcv=True
        
   def topic_to_cmds(self):
        tmpcmd=[]
        for x in self.list_cmds:
            tmp=x.get_cmd(self.topic[2])
            if tmp!="":
             if(tmp=="testprgrm:="):
                  tmpcmd= self.program2code(self.topic[3],self.payload)
                    # tmpcmd.append(tmp+self.topic[3]+self.payload+"\r")
                    # print(self.topic[3])
             else:
              if(tmp=="1;1;OVRD="):
                  tmpcmd.append(tmp+self.payload+"\r")
              else:
                  tmpcmd.append(tmp+"\r")
                 
        return tmpcmd

   def program2code(self,name,code):
    tmpcmd=[]
    c=1
    command=["1;0;JOGST\r","1;1;CNTLON\r","1;1;SLOTINIT\r","1;1;CNTLOFF\r","1;1;NEW\r","1;1;ECLR\r","1;1;LOAD="+name+'\r',"1;1;ECLR\r","1;1;PRTVERVALS\r"]
    for x in command:
      tmpcmd.append(x)
    # newcode=code.replace("\n", "")
    # codes=""
    for line in code.splitlines():
    #  print(str(c)+":"+line)
    #  print(line)
     line=line.replace("\r\n","")
     if(line!=""):
      if(c==1):
       tmpcmd.append("1;1;EDATA "+str(c)+" "+line+" 'LNADDED\r")
      else:
       tmpcmd.append("1;1;EDATA "+str(c)+" "+line+"\r")
      c=c+1
    return tmpcmd
   def extract_cmd(self,tmp_cmd_monitor):
    x=y=z=a=b=c=j1=j2=j3=j4=j5=j6=NULL
    state=re.findall("Qo[kK]?", tmp_cmd_monitor)
    if state!=[]:
        state=state[0]

      #   print(state)
      # PPOSF(state)
    setOrgin1=tmp_cmd_monitor.find("X;****;")
    setOrgin2=tmp_cmd_monitor.find("J1;****;")
    xl=re.findall("X;([-]?\\d.*?);", tmp_cmd_monitor)
    if xl!=[]:
      x=float(xl[0])
      # PPOSF(x)
      # print(x)

    yl=re.findall("Y;([-]?\\d.*?);", tmp_cmd_monitor)
    if yl!=[]:
      y=float(yl[0])
      # PPOSF(y)
      # print(y)
    zl=re.findall("Z;([-]?\\d.*?);", tmp_cmd_monitor)
    if zl!=[]:
      z=float(zl[0])
      # PPOSF(y)
      # print(y)
    al=re.findall("A;([-]?\\d.*?);", tmp_cmd_monitor)
    if al!=[]:
      try:
        a=float(al[0])
      # PPOSF(y)
      except:
        a=NULL
      # print(y)
    bl=re.findall("B;([-]?\\d.*?);", tmp_cmd_monitor)
    if bl!=[]:
      b=float(bl[0])
      # PPOSF(y)
      # print(y)
    cl=re.findall("C;([-]?\\d.*?);", tmp_cmd_monitor)
    if cl!=[]:
       c=float(cl[0])
      # PPOSF(c)
      #  print(c)

    j1l=re.findall("J1;([-]?\\d.*?);", tmp_cmd_monitor)
    if j1l!=[]:
       j1=float(j1l[0])
       # JPOSF(j1)
      #  print(j1)

    j2l=re.findall("J2;([-]?\\d.*?);", tmp_cmd_monitor)
    if j2l!=[]:
       j2=float(j2l[0])
       # JPOSF(j2)
      #  print(j2)

    j3l=re.findall("J3;([-]?\\d.*?);", tmp_cmd_monitor)
    if j3l!=[]:
       j3=float(j3l[0])
    # JPOSF(j3)
      #  print(j3)

    j4l=re.findall("J4;([-]?\\d.*?);", tmp_cmd_monitor)
    if j4l!=[]:
       j4=float(j4l[0])
    # JPOSF(j3)
      #  print(j3)

    j5l=re.findall("J5;([-]?\\d.*?);", tmp_cmd_monitor)
    if j5l!=[]:
       j5=float(j5l[0])
    # JPOSF(j3)
      #  print(j3)
    j6l=re.findall("J6;([-]?\\d.*?);", tmp_cmd_monitor)
    if j6l!=[]:
       j6=float(j6l[0])
    # JPOSF(j3)
      #  print(j3)

    pp=_PPOSF(state,x,y,z,a,b,c,"")
    jj=_JPOSF(state,j1,j2,j3,j4,j5,j6,"")
    # print (" \nPPOSF  is :"+str(pp.getJson()))
    # print (" \nJPOSF  is :"+str(jj.getJson()))
    # print (" \nPPOSF  is :"+str(pp.isEmpty_()))
    # print (" \nJPOSF  is :"+str(jj.isEmpty_()))
    if setOrgin1 !=-1 or setOrgin2 !=-1 :
        tmp_l=[]
        tmp_l.append("message")
        tmp_l.append('{"state":"Please Set Orgin"}')
        return tmp_l
    elif not pp.isEmpty_() :
        tmp_l=[]
        tmp_l.append(pp.type)
        tmp_l.append(pp.getJson())
        return tmp_l
    elif not  jj.isEmpty_():
        tmp_l=[]
        tmp_l.append(jj.type)
        tmp_l.append(jj.getJson())
        return tmp_l  
    # elif state.find("QoK")!=-1:
    #     tmp_l=[]
    #     tmp_l.append("message/state")
    #     tmp_l.append('{"state":"OK","data":{"data":"'+tmp_cmd_monitor.replace('\r',"")+'"}}')
    #     return tmp_l
    else:
        tmp_l=[]
        tmp_l.append("message")
        tmp_l.append('{"state":"Unknown","data":{"data":"'+tmp_cmd_monitor.replace('\r',"")+'"}}')
        return tmp_l



  
   #  print (" \nPPOSF X is :"+str(pp.getx()))
   #  print (" \nJPOSF J1 is :"+str(jj.getj1()))

# if __name__ == "__main__":
#    m= message_interpreter(1,2)
# #    m= _PPOSF(1,2,2,4,5,6,7,8)
   
#    print(m.extract_cmd("QoKX;12;Y;321;Z;201;A;32;B;291;C;23;;21,222;25;0.01;00000000"))
# #    print(m.getx)
  
 