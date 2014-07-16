#import cx_Oracle
import sqlite3
class DataBase:

    def __init__(self, user_name, user_password, host, SID):
        try:
            #conn_str = user_name + '/' + user_password + '@' + host + '/' + SID
            #print conn_str
            #self.connection = cx_Oracle.connect(conn_str)
            self.connection = sqlite3.connect("gl.sqlite") 
        except:
            print "Invalid connection."
            
    def login(self, user_name, password):
        cur = self.connection.cursor()
        cur.execute("SELECT GROUP_ID FROM USERS WHERE USER_NAME=? AND PASSWORD=?",(user_name,password,))
        id=cur.fetchall()
        if len(id) == 0:
            print "Null"
            return -1
        else:
            if id[0][0] == 0:
                print "User"
                return 0
            elif id[0][0] == 1:
                print "Admin"
                return 1
        cur.close()
        

    def get_tables(self):
        cur = self.connection.cursor()
        try:
            return cur.execute("SELECT * FROM user_tables;")#user_tables
        except:
            print "Cannot get tables."
        finally:
            cur.close()
        

    def get_tables_quantity(self, table_name):
        cur = connectiaon.cursor()
        try:
            return cur.execute("SELECT COUNT(*) FROM user_tables;")
        except:
            print "Cannot get tables quantity."
        finally:
            cur.close()

    def update():
        pass

    def insert():
        pass

    def create(table_name):
        pass

    def delete_table(self, table_name):
        cur = self.connection.cursor()
        try:
            cur.execute("DROP TABLE IF EXISTS" + table_name + ";")
            print "DROP TABLE succeeded"
        except:
            print "Cannot drop table."
        finally:
            cur.close()
            
        

    def delete_value(table_name, params):
        pass

    def select_without_params(self, table_name):
        cur = self.connection.cursor()
        try:
            print "SELECT * FROM " + table_name + ";"
            return cur.execute("SELECT * FROM " + table_name + ";")     
        except:
            print "Cannot execute method." #!
        finally:
            cur.close()

    def select_with_params(self, table_name, params):
        '''
        USER_NAME=5;GROUP_ID=1
        '''
        names = []
        values = []
        temp = params.split(';')

        for i in range(len(temp)):
            names.append(temp[i].split("=")[0])
            values.append(temp[i].split("=")[1])
        print names
        print values

        cur = self.connection.cursor()
        print "SELECT "

if __name__ == "__main__":
    d = DataBase("practice", "123", "192.168.111.133", "orcl")
##    result = d.login("Admin", "123")
    d.select_with_params("USERS", "USER_NAME=5;GROUP_ID=1")
    
    


