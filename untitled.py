
import _mysql
import sys
import MySQLdb as mdb
from collections import OrderedDict
class DataBaseCl:
    
    def __init__(self):
        try:
            self.con = mdb.connect('localhost', 'practice', '123', 'testdb')  
        except _mysql.Error, e:
            return "Error %d: %s" % (e.args[0], e.args[1])  
    
    def try_to_create_stored_proc(self):
        self.cursor=self.con.cursor()  
        sql = "call ProG" 
        args = ["cables"]
        try:
            self.cursor.callproc("Select_without_params",args)
            result = self.cursor.fetchall()
        except Exception, e:
            print e
        print result
        self.cursor.close()
    def try_to_create_stored_proc1(self):
        self.cursor=self.con.cursor()  
        sql = "call ProG" 
        args = ["cables"]
        try:
            self.cursor.callproc("test",args)
            result = self.cursor.fetchall()
        except Exception, e:
            print e
        print result
        self.cursor.close()




# delimiter //
# create procedure Select_without_params(IN table_name VARCHAR(20)) 
# begin 
# SELECT * FROM table_name;
# end;//

# delimiter //
# create procedure test() 
# begin 
# SELECT * FROM table_name;
# end;//



db_obj=DataBaseCl() 
db_obj.try_to_create_stored_proc()
db_obj.try_to_create_stored_proc1()
