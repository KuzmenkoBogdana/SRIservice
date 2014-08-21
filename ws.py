# -*- coding: utf-8 -*-
<<<<<<< HEAD

import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask, jsonify, abort, request, make_response, url_for, flash
from flask import send_from_directory
from flask import render_template
from werkzeug import secure_filename
from DataBaseCl import *
from FileHandler import *
from RequestHandler import *
from functools import wraps
import logging
import json
from flask import render_template

app = Flask(__name__, static_url_path='')
UPLOAD_FOLDER = '/home/bogdana/forfile/'
ALLOWED_EXTENSIONS = ['txt', 'xml', 'html']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] =  2 * 1024 * 1024
db_obj=DataBaseCl()
reqHandler=RequestHandler()

class WS:
    
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"Error":"sorry, page is not found"})
    
    def login(*rang):
        def decorator(fn):
            @wraps(fn)
            def decorated2(*args, **kwargs):
                auth = reqHandler.get_auth_params(request)
                if auth["login"]!=None:
                    if auth["password"]!=None:
                        res = db_obj.checkauth(auth['login'],auth['password'])
                        try:
                            if res['result'][0]['range'] in rang:
                                return fn(*args,**kwargs)
                        except:
                            return jsonify(res)
                        return jsonify({"Error":["You have no permissions"]})
                    return jsonify({"Error":["password field is empty"]})
                return jsonify({"Error":["login field is empty"]})
            return decorated2
        return decorator

    def check_table(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            table_name=reqHandler.get_table(request)
            if table_name!=None:
                if db_obj.db_if_table_exsists(table_name)==1:
                    return func(*args,**kwargs)
                else:
                    return jsonify({"Error":["Table doesn't exsist"]})
            return jsonify({"Error":["table field is empty"]})
        return decorated_function


    @app.route('/ws/authorisation/', methods = ['GET', 'POST'])
    def authorisation():
        '''
        authorization
        '''
        auth=reqHandler.get_auth_params(request)
        return jsonify(db_obj.checkauth(auth['login'],auth['password']))

    @app.route('/ws/alltables/', methods = ['GET','POST'])
    @login(*['admin','user'])
    def get_all_tables():
        '''
        returns list of all tables from data base
        '''
        auth = reqHandler.get_auth_params(request)
        res=app.test_client().get('/ws/authorisation/?login='+auth["login"]+'&password='+auth["password"])
        result=db_obj.db_get_all_tables()
        if json.loads(res.data)["result"][0]["range"] =='user':
            result['result'].remove({'tableName':'dbUsers'})
        return jsonify(result)     

    @app.route('/ws/get_tables_fields/', methods = ['GET', 'POST'])
    @login(*['admin','user'])
    @check_table
    def get_tables_fields():
        '''
        returns ductionaty of all filds and their types according to the input table
        '''
        table_name=reqHandler.get_table(request)
        return jsonify({"result":[dict(db_obj.get_table_fields(table_name))]})

    @app.route('/ws/get_tables_fields_without_autoinc/', methods = ['GET', 'POST'])
    @login(*['admin','user'])
    @check_table
    def get_tables_fields_insert():
        '''
        returns ductionaty of all filds and their types according to the input table
        '''
        table_name=reqHandler.get_table(request)
        auto_increment=db_obj.get_autu_increment_field(table_name)
        result=list(db_obj.get_table_fields(table_name))
        for i in result:
            if i[0] in auto_increment:
                result.remove(i)
        return jsonify({"result":[dict(result)]})


    @app.route('/ws/get_items/', methods=['GET','POST'])
    @login(*['admin','user'])
    @check_table
    def get_items():
        '''
        returns all items of input table
        '''
        table_name=reqHandler.get_table(request)
        list_of_params= reqHandler.get_parameters('params',table_name,request)
        if len(list_of_params)>0:
            return jsonify(db_obj.db_select(table_name,*list_of_params))
        return jsonify(db_obj.db_select(table_name))

    @app.route('/ws/update/',methods=['POST'])
    @login(*['admin'])
    @check_table
    def update_items():
        '''
        changes records with params_before according to params_after
        returns all items after upding
        '''
        if request.method == 'POST':
            request.get_json(force=True)
            table_name=request.json.get("table_name") 
            criteria_for_update=reqHandler.get_parameters('params',table_name,request,True)
            values=reqHandler.get_parameters('criteria_for_update',table_name,request)
        if criteria_for_update==[] or values==[]:
            return jsonify({"Error":["Not all query parameters introduced"]})
        params=[criteria_for_update, values]
        return jsonify(db_obj.db_update(table_name, *params))
        

    @app.route('/ws/delete/',methods=['GET','POST'])
    @login(*['admin'])
    @check_table
    def delete_items():
        '''
        deletes records according to unput params
        returns all items after deleting
        '''
        table_name=reqHandler.get_table(request)
        list_of_params=reqHandler.get_parameters('params',table_name,request)
        if len(list_of_params)>0:
            db_obj.db_delete(table_name,*list_of_params)
            return jsonify(db_obj.db_select(table_name))
        return jsonify({"Error":"Empty list of params"})

    @app.route('/ws/insert/',methods=['GET','POST'])
    @login(*['admin'])
    @check_table
    def insert_items():
        '''
        deletes records according to unput params
        returns all items after deleting
        '''
        table_name=reqHandler.get_table(request)
        list_of_params=reqHandler.get_parameters('params',table_name,request,True)
        if len(list_of_params)>0:
            db_obj.db_insert(table_name,*list_of_params)
            return jsonify(db_obj.db_select(table_name))
        return jsonify({"Error":"Empty list of params"})

    @app.route('/ws/create_table/', methods=["POST"])
    @login(*['admin'])
    def table_create():
        request.get_json(force=True)
        table_name=request.json.get("table_name") 
        tables_fields=reqHandler.get_tables_fields_for_creating(request)
        return db_obj.db_table_create(table_name, *tables_fields)
        

    @app.route('/ws/drop_table/', methods=["POST","GET"])
    @login(*['admin'])
    def drop_table():
        table_name=reqHandler.get_table(request)
        return db_obj.db_drop_table(table_name)

    @app.route('/ws/file_upload/', methods=['GET', 'POST'])
    def upload_file():
        '''
        modification data base accoding to parameters specified at the input file
        '''
        if request.method == 'POST':
            f = request.files['file_name']
            if f: 
                if f.filename.split('.')[1] in ALLOWED_EXTENSIONS:
                    filename = secure_filename(f.filename)
                    path_f=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    f.save(path_f)
                    req=FileHandler(path_f)
                    res=req.parse_file()
                    return jsonify( { 'result' : res} )
            else:
                return 'not upload' 
        return '''
        <!doctype html>
        <form action="" method=post enctype=multipart/form-data>
              <p><input type=file name= file_name> 
             <input type=submit value=Upload>
        </form>
        '''  
    @app.route('/ws/test/', methods = ['POST'])
    def test():
        '''
        authorization
        '''
        request.get_json(force=True)
        variable=request.json.get('i')
        return str(variable)
if __name__ == '__main__': 
    app.run(debug = True, host='0.0.0.0')  
=======
import os
import logging 
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask import send_from_directory
from werkzeug import secure_filename
from DataBaseCl import *
from FileHandler import *

app = Flask(__name__)
auth = HTTPBasicAuth()
UPLOAD_FOLDER = '/home/bogdana/forfile/'
ALLOWED_EXTENSIONS = ['txt', 'xml']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

class WS:
    
    

    @app.route('/ws/<table_name>/<login>/<password>', methods = ['GET'])
    def get_product_type(table_name,login, password):
        '''
        Returns all items of <table_name> table
        '''
        db_obj=DataBaseCl()
        if db_obj.checkauth(login, password):
            result=db_obj.select_without_params(table_name)
            return jsonify( { 'result:' : result} )
        else:
            return ('You have no permissions')

    @app.route('/ws/<table_name>/<params>/<login>/<password>', methods = ['GET'])
    def get_items(table_name, params,login, password):
        '''
        Returns all items of <table_name> table, according to the parameters
        '''
        db_obj=DataBaseCl()
        if db_obj.checkauth(login, password):
            result=db_obj.select_with_params(table_name, params)
            return jsonify( { 'result:' : result} )
        else:
            return ('You have no permissions')
    
    @app.route('/ws/delete/<table_name>/<params>/<login>/<password>',methods=['DELETE'])
    def delete_items(table_name, params,login, password):
        '''
        Deletes items ftom the <table_name> table according to the parameters
        '''
        db_obj=DataBaseCl()
        if db_obj.checkauth(login, password):
            result=db_obj.db_func_delete(table_name, params)
            return jsonify({ 'result:' : result})
        else:
            return ('You have no permissions')
        
        
    @app.route('/ws/file_upload/<login>/<password>', methods=['GET', 'POST'])
    def upload_file(login, password):
        '''
        Uploads files 
        '''
        db_obj=DataBaseCl()
        if db_obj.checkauth(login, password):
            if request.method == 'POST':
                f = request.files['file_name']
                if f: 
                    if f.filename.split('.')[1] in ALLOWED_EXTENSIONS:
                        filename = secure_filename(f.filename)
                        path_f=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        f.save(path_f)
                        req=FileHandler(path_f)
                        res=req.parse_file()
                        return jsonify( { 'result:' : res} )
                else:
                    return 'not upload' 
            return '''
            <!doctype html>
            <form action="" method=post enctype=multipart/form-data>
                  <p><input type=file name= file_name> 
                 <input type=submit value=Upload>
            </form>    
                '''
        else:
            return ('you have no permissions')


if __name__ == '__main__':
##    log_f=os.path.join(app.config['UPLOAD_FOLDER'],'mylog.log')
##    logger = logging.getLogger()
##    logger.setLevel(logging.DEBUG)
##    handler = logging.FileHandler(log_f)
##    handler.setLevel(logging.DEBUG)
##    logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = log_f)
##    logger.addHandler(handler)
##    logger.info('Getting started')
##    logger.info('Done')
##    handler.close()   
    app.run(debug = True)  
>>>>>>> b02e1a3900b5400d18bb5a610cad8dc2ca1b0712
