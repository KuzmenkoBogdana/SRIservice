# -*- coding: utf-8 -*-

from DataBaseCl import *
from functools import wraps

class RequestHandler:
    def __init__(self):
        self.db_obj=DataBaseCl()      

    def get_table(self,request):
        if request.method == 'POST':
            request.get_json(force=True)
            table_name=request.json.get("table_name") 
        if request.method == 'GET':
            table_name=request.args.get("table_name") 
        return table_name

    def get_parameters(self,key,table_name,request,type_method=None):
        print request
        print request.json
        table_fields=dict(self.db_obj.get_table_fields(table_name)).keys()
        if request.method == 'POST':
            params=self.params_for_post(key,table_fields,request, type_method)      
        if request.method == 'GET':
            params=self.params_for_get(table_fields, request, type_method)
        return params

    def params_for_get(self, table_fields, request, type_method):
        res_params=[]
        list_of_params= [request.args.get(item.lower()) for item in table_fields]
        params=zip(table_fields,list_of_params)
        for l in params:
            if l[1]!=None:
                res_params.append(l)
        params=["%s=%s" % (k, v) for k, v in dict(res_params).items()]
        if type_method:
            return [params]
        return params
    
    def params_for_post(self,key,table_fields, request, type_method):
        params,item_parameter=[],[]
        request.get_json(force=True)
        all_parameters=request.json.get(key)
        if all_parameters:
            for items in all_parameters:
                for i in table_fields:
                    if i in items.keys():
                        if type_method:
                            item_parameter.append([i,items[i],'='])
                        else:
                            item_parameter.append([i,items[i],items['sign_comparison']])
                parameter=self.creating_params_list_for_post(*item_parameter)
                params.append(parameter)
                item_parameter=[]     
        return params

    def creating_params_list_for_post(self,*params):
        res_params=[]
        for i in params:
            req=i[0]+' '+i[2]+' "'+i[1]+'"'
            res_params.append(req)
        return res_params
    
    def get_tables_fields_for_creating(self,request):
        table_parameters,table_fields=[],[]
        request.get_json(force=True)
        fields=request.json.get("params")
        for f in fields:
            table_fields.append(f["t_field_name"])
            table_fields.append(f["type"])
            for i in f["peculiar_properties"]:
                table_fields.append(i)
            table_parameters.append(' ' .join(table_fields))
            table_fields=[]
        return table_parameters


    def get_auth_params(self,request):
        auth={}
        if request.method == 'POST':
            request.get_json(force=True)
            login=request.json.get('login')
            password =request.json.get('password')
        if request.method == 'GET':
            login=request.args.get('login')
            password =request.args.get('password')
        auth["login"]=login
        auth["password"]=password
        return auth
