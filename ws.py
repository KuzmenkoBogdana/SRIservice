# -*- coding: utf-8 -*-
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
    
    @app.route('/ws/<table_name>', methods = ['GET'])
    def get_product_type(table_name):
        '''
        Returns all items of <table_name> table
        '''
        db_obj=DataBaseCl()
        result=db_obj.select_without_params(table_name)
        return jsonify( { 'result:' : result} )
    
    @app.route('/ws/<table_name>/<params>', methods = ['GET'])
    def get_items(table_name, params):
        '''
        Returns all items of <table_name> table, according to the parameters
        '''
        db_obj=DataBaseCl()
        result=db_obj.select_with_params(table_name, params)
        return jsonify( { 'result:' : result} )
        
##
##    @app.route('/ws/<table_name>/<login>/<password>', methods = ['GET'])
##    def get_product_type(table_name,login, password):
##        '''
##        Returns all items of <table_name> table
##        '''
##        db_obj=DataBaseCl()
##        if db_obj.checkauth(login, password):
##            result=db_obj.select_without_params(table_name)
##            return jsonify( { 'result:' : result} )
##        else:
##            return ('You have no permissions')

##    @app.route('/ws/<table_name>/<params>/<login>/<password>', methods = ['GET'])
##    def get_items(table_name, params,login, password):
##        '''
##        Returns all items of <table_name> table, according to the parameters
##        '''
##        db_obj=DataBaseCl()
##        if db_obj.checkauth(login, password):
##            result=db_obj.select_with_params(table_name, params)
##            return jsonify( { 'result:' : result} )
##        else:
##            return ('You have no permissions')
    
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
