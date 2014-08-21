# -*- coding: utf-8 -*-

import _mysql
import sys
import MySQLdb as mdb

class DataBaseCl:
    
    def __init__(self):
        # try:
        self.con = mdb.connect('localhost', 'root', 'pass', 'testdb')
        self.cursor=self.con.cursor()    
        # except _mysql.Error, e:
            # return "Error %d: %s" % (e.args[0], e.args[1])
            
    def db_if_table_exsists(self, table_name):
        self.cursor.execute('SHOW TABLES LIKE \''+table_name+'\'')
        res = self.cursor.fetchall()
        return len(res)
    
    def db_get_all_tables(self):
        self.cursor.execute("select table_name from information_schema.tables where TABLE_SCHEMA=\"testdb\"")
        res = self.cursor.fetchall()
        return self.user_friendly_return([['tableName']],res)
      
    def get_table_fields(self, table_name):
        self.cursor.execute('SELECT column_name, DATA_TYPE  FROM information_schema.columns WHERE table_name =\'%s\';'%table_name)
        res = self.cursor.fetchall()
        return res

    def get_autu_increment_field(self,table_name):
        self.cursor.execute("show columns from %s where extra like \'auto_increment\'"%table_name)
        res=self.cursor.fetchall()
        return res[0][0]

    def db_select(self, table_name, *param):
        if len(param)>0:
            params=self.checkparams(*param)
            try:
                print ('SELECT * FROM %s WHERE %s ;' %( table_name,' AND ' .join(params)))
                self.cursor.execute('SELECT * FROM %s WHERE %s ;' %( table_name,' AND ' .join(params)))
                res = self.cursor.fetchall() 
            except:  
                return {"Error": "Wrong type of input value"} 
        else:
            print ('select * from '+str(table_name)+';')
            self.cursor.execute('select * from '+table_name+';')
            res = self.cursor.fetchall()
        fields=self.get_table_fields(table_name) 
        return self.user_friendly_return(fields,res)


    def db_delete(self, table_name, *param):
        params=self.checkparams(*param)
        with self.con:
             print ('Delete from %s where %s ;' %(table_name, ' AND ' .join(params)))
             self.cursor.execute('Delete from %s where %s ;' %(table_name, ' AND ' .join(params)))
    
    def db_update(self,  table_name, *params):
        values=self.checkparams(*params[0])
        criteria_to_update=self.checkparams(*params[1])
        with self.con:
            try:
                print ('Update %s set %s where %s ;' %(table_name, ', ' .join(values), ' AND ' .join(criteria_to_update)))
                self.cursor.execute('Update %s set %s where %s ;' %(table_name, ', ' .join(values), ' AND ' .join(criteria_to_update)))  
                rowsaffected = self.cursor.rowcount
                if self.cursor.rowcount==0:
                    return {"Error":["No raws were affected"]}
            except:
                return {"Error":["There are no records matching the query"]} 
        return self.db_select(table_name)
        
    def checkparams(self,*param):
        params=[]
        for i in param:
            if str(type(i))=="<type 'list'>":
                tmp='%s' %( 'AND ' .join(i))
                params.append(tmp)
                tmp=[]
            else:
                params=param[:]
        return params
        
    def db_insert(self,  table_name, *params):
        with self.con:
            for i in params:
                print ('Insert into %s set %s'%(table_name, ', ' .join(i)))
                self.cursor.execute('Insert into %s set %s'%(table_name, ', ' .join(i)))

    def db_table_create(self, table_name, *params):   
        print ('Create table %s (%s )'%(table_name, ', ' .join(params)))
        with self.con:
            return self.cursor.execute('Create table %s (%s )'%(table_name, ', ' .join(params)))

    def checkauth(self,login,password):
        self.cursor.execute('select login, password, rang from dbUsers where login=\'%s\''%login)
        result=self.cursor.fetchall()
        fields=[['login'],['password'], ['range']]
        if len(result)>0:
            for i in result:
                if password==i[1]:
                    return self.user_friendly_return(fields, result)
                else:
                    return {'Error':['wrong password']}
        else:
            return {'Error':['wrong login']}

    def user_friendly_return(self,*parameters):
        diction={}
        fin=[]
        if len(parameters[1])>0:
            for i in parameters[1]:
                for j in range(len(i)):
                    diction[parameters[0][j][0]]=i[j]
                fin.append(diction)
                diction={}
            return {"result":fin}
        return {'Error':'There are no records that match the query'}
