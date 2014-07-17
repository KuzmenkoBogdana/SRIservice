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
        

##    def get_tables_quantity(self, table_name):
##        cur = self.connectiaon.cursor()
##        try:
##            return cur.execute("SELECT COUNT(*) FROM user_tables;")
##        except:
##            print "Cannot get tables quantity."
##        finally:
##            cur.close()

    def update(self, table_name, update_field, condition):
        #UPDATE table_name SET col1=val1, col2=val2 WHERE ID=6;
        #SET USER_NAME='Admin',GROUP_ID=1
        #WHERE condition
        cur = self.connection.cursor()
        get_field_params = update_field.replace(';',',')
        get_where_params = condition.replace(';',' AND ')

        query = "UPDATE " + table_name + " SET " + get_field_params + " WHERE " + get_where_params + ";"       
##        print query
        try:
            cur.execute(query)
        except:
            print "Cannot execute method" #TODO:
        finally:
            cur.close()

    def insert(self, table_name, fields, values):
        cur = self.connection.cursor()
        get_fields = fields.replace(';',',')
        get_values = values.replace(';',',')
        
        query = "INSERT INTO " + table_name + " (" + get_fields + ") VALUES (" + get_values + ");"
##        print query
        try:
            cur.execute(query)
            cur.execute("SELECT * FROM USERS;")
            print cur.fetchall()
        except:
            print "Cannot execute method" #TODO:
        finally:
            cur.close()

    def create(self, table_name, params):
        cur = self.connection.cursor()

        query = "CREATE TABLE " + table_name + " (" + params + ");"
        try:
            cur.execute(query)
        except:
            print "Cannot execute method" #TODO:
        finally:
            cur.close()

    def delete_table(self, table_name):
        cur = self.connection.cursor()
        try:
            cur.execute("DROP TABLE IF EXISTS" + table_name + ";")
            print "DROP TABLE succeeded"
        except:
            print "Cannot drop table."
        finally:
            cur.close()
                    

    def delete_value(self, table_name, condition):
        #DELETE FROM table_name WHERE
        cur = self.connection.cursor()
        
        get_value = condition.replace(';',' AND ')
        query = "DELETE FROM " + table_name + " WHERE " + get_value + ";"
##        print query
        try:
            cur.execute(query)
            cur.execute("SELECT * FROM USERS;")
            print cur.fetchall()
        except:
            print "Cannot execute method" #TODO:
        finally:
            cur.close()

    def select_without_params(self, table_name):
        cur = self.connection.cursor()
        
        try:
##            print "SELECT * FROM " + table_name + ";"
            return cur.execute("SELECT * FROM " + table_name + ";")     
        except:
            print "Cannot execute method." #!
        finally:
            cur.close()

    def select_with_params(self, table_name, params):
##        USER_NAME='Admin',GROUP_ID=1
##            SELECT * FROM TABLE_NAME WHERE USER_NAME=Admin, GROUP_ID=1;
        cur = self.connection.cursor()
        get_params = params.replace(';', ' AND ')

        query = "SELECT * FROM " + table_name + " WHERE " + get_params + ";"
                
        print query
        try:
            return cur.execute(query)
        except:
            print "Comment area" #Vot tut srochno doljen bit' comment
        finally:
            cur.close()
##        print cur.fetchall() #Test cursora

##TODO: SELECT with *args
    def select(self, table_name, *params):
        cur = self.connection.cursor()
        
        if len(params) == 0:
            try:
                print "SELECT * FROM " + table_name + ";"
                return cur.execute("SELECT * FROM " + table_name + ";")     
            except:
                print "Cannot execute method." #!
            finally:
                cur.close()
        else:
            get_params = params.replace(';',' AND ')

            query = "SELECT * FROM " + table_name + " WHERE " + get_params + ";"                
##            print query
            try:
                return cur.execute(query)
            except:
                print "Comment area" #Vot tut srochno doljen bit' comment
            finally:
                cur.close()
##            print cur.fetchall() #Test cursora

        
if __name__ == "__main__":
    d = DataBase("practice", "123", "192.168.111.133", "orcl")
##    result = d.login("Admin", "123")
##    d.select_with_params("USERS", "USER_NAME='Admin';GROUP_ID=1")
##    d.update("USERS", "USER_NAME='Admin'", "GROUP_ID=1")
##    d.insert("USERS", "USER_NAME;PASSWORD;GROUP_ID", "'John';666;0")
##    d.delete_value("USERS", "USER_NAME='Test'")
##    d.insert("USERS", "USER_NAME;PASSWORD;GROUP_ID", "'Test';666;0")

