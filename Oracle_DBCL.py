import cx_Oracle

class DataBaseCl:
    def __init__(self):
        self.__db = cx_Oracle.Connection("/as sysdba")
        self.__cursor = self.__db.cursor()
        return self
    
    def db_if_table_exsists(self, table_name):
        return self.cursor.execute('SHOW TABLES LIKE \''+table_name+'\'')

    def get_table_fields(self, table_name):
        '''
        Returns all fields of table
        '''
        table_fields=[]
        self.cursor.execute('SELECT column_name FROM information_schema.columns WHERE table_name =\'%s\''%table_name)
        res = self.cursor.fetchall()
        for i in range(len(res)):
            table_fields.append(res[i][0].lower())
        return table_fields
    
       
    def db_select(self, table_name, *param):
        if len(param)>0:
            self.__cursor.callproc("DB_SELECT_WITH_PARAMS",table_name, (', ' .join(params)))  
        else:
            self.__cursor.callproc("DB_SELECT_WITHOUT_PARAMS", table_name)
    
    def db_delete(self, table_name, *params):
        self.__cursor.callproc("DB_DELETE",table_name, (', ' .join(params)))

    def db_update(self,  table_name, *params):
        self.__cursor.callproc("DB_UPDATE",table_name, (', ' .join(params[0]), ', ' .join(params[1])))
  
    def db_insert(self,  table_name, *params):
        self.__cursor.callproc("DB_INSERT", table_name,(', ' .join(params)))

    def db_table_create(self, table_name, *params):
        self.__cursor.callproc("DB_CREATE_TABLE", table_name,(', ' .join(params)))


    def checkauth(self,login,password):
        self.__cursor.callproc("DB_CHECKOUTH", login, password)   
od=DataBaseCl()
