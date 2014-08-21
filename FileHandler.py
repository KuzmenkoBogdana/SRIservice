import os
import lxml
from lxml import etree

from DataBaseCl import *
class FileHandler:
    
    def __init__(self, path):
      self.path=path
      self.l=[]
      self.comm=[]
      self.tables=[]
      self.items=[]
      self.params=[]
      self.requests=[]
      self.tmp={}
      self.db_obj=DataBaseCl()

    def parse_file(self):
      f=open(self.path)
      dbinf=f.read()
      self.get_query_types(dbinf)
      while len(self.comm)>1:
          self.gettables()
      return self.requests

    def get_query_types(self, dbinf):
      root = etree.fromstring(dbinf)
      for element in root.iter():
         self.l.append((element.tag, element.text))
      for i in range(len(self.l)):
          if self.l[i][0]=='delete':
              self.tmp['delete']=i
          if self.l[i][0]=='insert':
              self.tmp['insert']=i
      for key, value in sorted(self.tmp.iteritems(), key=lambda (k,v): (v,k)):
          self.comm.append([value, key])
      self.comm.append([len(self.l),'eof'])

    def gettables(self):
      for  i in range(self.comm[0][0],self.comm[1][0]):
        if self.l[i][0]=='table_name':
          self.tables.append([i,self.l[i][1]])
      self.tables.append((self.comm[1][0], ''))
      self.getitems()
      self.comm.remove(self.comm[0])
       
    def getitems(self):
      while len(self.tables)>1: 
        for i in range(self.tables[0][0], self.tables[1][0]):
          if self.l[i][0]=='item':
            self.items.append(i)
        self.items.append(self.tables[1][0])
        self.getitemsparam()
        self.tables.remove(self.tables[0])
         
    def getitemsparam(self):
      while len(self.items)>1:
        for i in range(self.items[0]+1,self.items[1]):
          self.params.append(str(self.l[i][0]+'='+self.l[i][1]))
        if len(self.params)>2:
          self.query_create()                        
        self.items.remove(self.items[0])
        self.params=[]

    def query_create(self):
      if self.db_obj.db_if_table_exsists(self.tables[0][1])==1:
        if self.comm[0][1]=='delete':
          self.db_obj.db_delete(self.tables[0][1], *self.params  )
          self.requests.append('data %s had been deleted from %s'%(', '.join(self.params),self.tables[0][1]))
        elif self.comm[0][1]=='insert':
          self.db_obj.db_insert(self.tables[0][1], *[self.params] )
          self.requests.append('data %s had been inserted to %s'%(', '.join(self.params),self.tables[0][1]))
      else:
        if self.comm[0][1]=='delete':
          self.requests.append('there is no %s table in db' %self.tables[0][1])
        elif self.comm[0][1]=='insert':
          self.create_table(self.tables[1][0], *[self.params])
          self.db_obj.db_insert(*self.params  )
      try:
        os.remove(self.path)
      except OSError:
        pass
        
    def create_table(self, *params  ):
        res=[]
        for i in self.params  :
           s=i.split('=')
           if s[1].isdigit():
               type_var='INT'
           elif s[1].replace('.','').isdigit():
               type_var='float'
           else :
               type_var='VARCHAR(25)'
           res.append('%s %s'%(s[0], type_var))
        self.db_obj.db_table_create(self.tables[0][1], *res)
                        
