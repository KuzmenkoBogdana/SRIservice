# -*- coding: utf-8 -*-
import ws
import unittest
import json


class WsTestCases(unittest.TestCase):
    def setUp(self):
        self.app = ws.app.test_client()
        
    def test_table_name(self):
        expected={"Error": ["Table doesn't exsist"]}
        rv=self.app.get('/ws/get_items/?table_name=cablles&login=user&password=qwerty')
        print json.loads(rv.data)
        self.assertEqual(json.loads(rv.data), expected)
    def test_login_not_emppty(self):
        expected={"Error": ['login field is empty']}
        rv=self.app.get('/ws/get_items/?table_name=cables&password=qwerty')
        print json.loads(rv.data)
        self.assertEqual(json.loads(rv.data), expected)
    def test_password_not_emppty(self):
        expected={"Error": ["password field is empty"]}
        rv=self.app.get('/ws/get_items/?table_name=cables&login=user')
        print json.loads(rv.data)
        self.assertEqual(json.loads(rv.data), expected)
    def test_password(self):
        expected={"Error": ["wrong password"]}
        rv=self.app.get('/ws/get_items/?table_name=cablles&login=user&password=qweerty')
        print json.loads(rv.data)
        self.assertEqual(json.loads(rv.data), expected)
    def test_login(self):
        expected={"Error": ["wrong login"]}
        rv=self.app.get('/ws/get_items/?table_name=cables&login=userr&password=qwerty')
        print json.loads(rv.data)
        self.assertEqual(json.loads(rv.data), expected)
    def test_delete_permissions(self):
        expected={"Error": ["You have no permissions"]}
        rv=self.app.get('/ws/delete/?table_name=cables&id=1&login=user&password=qwerty')
        print json.loads(rv.data)
        self.assertEqual(json.loads(rv.data), expected)

    def test_create_table(self):
        rv=self.app.post('/ws/create_table/',
            data=json.dumps({
                'login':'admin',
                'password':'qwerty',
                "table_name":"some_name",
                "params":[{"t_field_name":"id",
                "type":"int",
                "peculiar_properties":["primary key", "autoinctement"]},
                {"t_field_name":"name",
                "type":"varchar",
                "peculiar_properties":[]}]
                }), content_type='application/json')
        print rv.data
# @app.route('/login', methods=['POST', 'OPTIONS'])
# def login():
#     print request.remote_addr
#     print request.headers['User-Agent']
# And then in your testing code you do something like: 
# client = app.test_client()
# client.post('/login',
#             data=json.dumps({
#                 'username': 'sheldon@cooper.com',
#                 'password': 'howimetyourmother'
#             }), content_type='application/json')

#     def test_checkauthorisation(self):
#         rv = self.app.post('/ws/authorisation/', data='{"login":"user", "password":"qwerty"}', content_type='application/json')
#         print self.reqparse.add_argument('login', type=str, location='get_json')
if __name__ == '__main__':
    unittest.main()
    
