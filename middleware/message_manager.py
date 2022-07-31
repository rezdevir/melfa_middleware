# 2 Topic types must be add Control and service
import pandas as pd
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

class message_interpreter(message,_command):
   cmds=[]
   list_cmds=[]
   du_state=False

   def interpreter(self,msg):
    if not self.du_state:
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
    #    print(self.topic)
       self.dispatch()
       self.clear_message()
       return "ok"
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
                tmpcmd=[]
                # self.melfa_serial.write(self.Remote_user_line)
                self.dtru_rcv=True
                for x in self.list_cmds:
                   tmp=x.get_cmd(self.topic[2])
                   if(tmp!=""):
                     # print (tmp)
                     tmpcmd.append(tmp)
                self.cmds=tmpcmd
                
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
        

# if __name__ == "__main__":
#    m= message_interpreter()
#    m.on_Start()