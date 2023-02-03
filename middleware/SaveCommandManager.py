class _save():
 isTraceFile=True
 file=open('TraceFile.txt',"w")
  
 def save(self,line):
  if (self.isTraceFile):
   self.file.write(line)
 def close_save(self):
  self.close()