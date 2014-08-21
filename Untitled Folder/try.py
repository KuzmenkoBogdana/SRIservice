# -*- coding: utf-8 -*-
import os
import lxml
from lxml import etree
ALLOWED_EXTENSIONS = ['htm', 'html']
SPLIT_SYMBOLS=['/','-','\\','.']
class FileHandler:
    def __init__(self, path):
    	self.path=path
        dict_tags=[]
        self.files=[]
    def get_all_files(self):
        if os.path.isdir(self.path):
            for root, dirs, files in os.walk(self.path): 
                for name in files:
                    fullname = os.path.join(root, name)
                    if fullname.split('.')[1] in ALLOWED_EXTENSIONS:
                    	self.files.append(fullname)
        print self.files

    def parse_file(self, path):
    	f=open(path)
    	fileContent=f.read()
    	root = etree.fromstring(fileContent)
    	tmp=[]
    	for element in root.iter():
    		tmp.append((element.tag, element.text))
    	return dict(tmp)	
 
    def rename_file(self, tag):
    	for path in self.files: 
    		dict_tags=self.parse_file(path)
    		directory=os.path.split(path)[0]
    		if tag in dict_tags.keys():
    			file_name=dict_tags[tag]
    			for i in SPLIT_SYMBOLS:
    				if i not in file_name:
    					os.rename(path,os.path.join(directory,(file_name.strip()+'.html')))
    				else:
    					sub_dir_create=file_name.split(i)
    					for i in range(len(sub_dir_create)-1):
    						directory=os.path.join(directory,sub_dir_create[i])
    						if not os.path.isdir(directory):
   								os.makedirs(directory)
#db_obj=FileHandler('/home/bogdana/forfile/test.html')
file_obj=FileHandler('/home/bogdana/test/')
file_obj.get_all_files()
file_obj.rename_file("title")