#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Module docstring
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2015, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@region-alsace.org"
__status__ = "Developement"

import bottle
import os
from uuid import uuid4
#import socket
import time
import glob
import json
import pprint
import re
import zipfile 

# from api.md import xlsx_to_dict
# from api.md import dict_to_xml
from api import shp_info

from api import xlsx_shp_to_xml
from api import xml_to_xlsx

app = application = bottle.default_app()
'''
@app.route('/')# Handle HTTP GET for the application root
def index():
    return template('<h1>{{message}}</h1>', message='Hello Runabove')
'''
 
@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    try:
        return bottle.static_file(filename, root='{}/static'.format(os.path.dirname(__file__)))
    except:
        return '{}/static'.format(os.path.dirname(os.path.abspath(__file__)))

@app.route('/zaphir/<filename:path>')
def zaphir(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='./web/zaphirWeb')
    
@app.route('/mdreader/<filename:path>')
def mdreader(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='./web/mdReaderJS')

@app.get('/xml2csw')
@app.post('/xml2csw')
def xml2csw():
    '''
    Serve xml file like csw
    '''
    xml = ''
    get_xml_dir = bottle.request.query.xml_dir or None
    get_request = bottle.request.query.request or 'GetRecordById'
    get_id = bottle.request.query.id or None
    
    if get_request and get_request == 'GetRecordById':
        if get_id is not None:
            xml_filepath = os.path.join(get_xml_dir, get_id)
            if os.path.isfile(xml_filepath):
                with open(xml_filepath, 'r') as xml_file:
                    xml = xml_file.readlines()
                    xml.pop(0)
                    # xml[0] = '<csw:GetRecordByIdResponse xmlns:csw="http://www.opengis.net/cat/csw/2.0.2">'
                    # xml.append('</csw:GetRecordByIdResponse>')
                             
                #bottle.response.headers['Content-Type'] = 'xml/application'
                bottle.response.content_type = "application/xml; charset=UTF-8"
                    
                return xml
            else:
                return xml_filepath
        else:
            return 'dir: ', get_xml_dir, 'request:', get_request, 'id:', get_id
    else:
        return '"Request" parameter missing.'
    
"""
@app.post('/server/index.py')
def server():
    '''
    Serve static files
    '''
    #return bottle.static_file(filename, root='./xml2cws')
    return '<b>ok</b>'
"""
 
@app.route('/files/<filename:path>')
def files(filename):
    return bottle.static_file(filename, root='./files', download=filename)
    
@app.get('/')
def show_index():
    '''
    serve "index" page
    '''
    #return 'Hello, this is the index page 1'
    bottle.redirect('/zaphir/index.html')
    

@app.route('/convert', method='POST')
def convert():
    '''
    get files, convert them and return link to result
    '''
    success = False
    #path = os.path.join('files', str(uuid4()))
    #ip = socket.gethostbyname(socket.gethostname())
    ip = bottle.request.environ.get('REMOTE_ADDR')
    dtime = time.time()
    path = os.path.join('files', str(ip)+'_'+str(int(dtime)))
    path_in = os.path.join(path, 'IN')
    path_out = os.path.join(path, 'OUT')
    if not os.path.exists(path_in): 
        os.makedirs(path_in)
    if not os.path.exists(path_out): 
        os.makedirs(path_out)
            
    upload = bottle.request.files.get('file')
    name, ext = os.path.splitext(upload.filename)
    upload.save(path_in, True) # appends upload.filename automatically
    
    is_zip = False
    # if ext.lower() == '.zip'
    if zipfile.is_zipfile(os.path.join(path_in, upload.filename)):
        is_zip = True
        file_out = name+'.zip'
        zfile = zipfile.ZipFile(os.path.join(path_in, upload.filename), 'r')
        zfile.extractall(path_in)
    elif ext.lower() == '.xlsx':
        file_out = name+'.xml'
    elif ext.lower() == '.xml':
        file_out = name+'.xlsx'
    else:
        file_out = False
        
    files = glob.glob(os.path.join(path_in, '*.*'))
    # print path_in
    # print files
    files_out = []
    files_shp = []
    for file_in in files:
        path, filename_in = os.path.split(path)
        name_in, ext_in = os.path.splitext(file_in)
        name_in = os.path.basename(name_in) # Nécessaire car pb de détection du nom de fichier à cause de l'adresse IP dans le chemin
        # print name_in, ext_in
        if ext_in.lower() == '.xlsx':
            # print ext_in.lower()
            # try:
            # Charger md_default = md.json
            json_file = 'json/md.json'
            if os.path.isfile(json_file):
                with open(json_file, 'r') as md_file:
                    md_dict = json.load(md_file)
            else:
                md_dict = {}

            md_xml = xlsx_shp_to_xml.convert(file_in, path_out, md_dict)
            files_out.append({'src': name_in+'.xlsx', 'dst': name_in+'.xml'})
            # except:
            # pass
            
        elif ext_in.lower() == '.xml'and not name_in.endswith('.shp') :
            json_file = 'json/md.json'
            if os.path.isfile(json_file):
                with open(json_file, 'r') as md_file:
                    md_dict = json.load(md_file)
            else:
                md_dict = {}
            # TODO: get xlsx_template from zip file (template.xlsx)
            xlsx_template = 'tpl/MODELE-VIDE_FicheMD-CIGAL_simple_150428.xlsx'
            md_xlsx = xml_to_xlsx.convert(file_in, os.path.join(path_out, name_in+'.xlsx'), xlsx_template, md_dict)
            files_out.append({'src': name_in+'.xml', 'dst': name_in+'.xlsx', 'src_view': '1', 'dst_view': 0})
            # xml_view = 1

        elif ext_in.lower() == '.shp':
            shp = {}
            shp = shp_info.get_shp_info(file_in)
            if shp: 
                files_shp.append(shp)
  
    if is_zip:
        zip_files = glob.glob(os.path.join(path_out, '*.*'))
        with zipfile.ZipFile(os.path.join(path_out, file_out), mode='w') as zf:
            for zip_file in zip_files:
                zf.write(zip_file, os.path.basename(zip_file), zipfile.ZIP_DEFLATED)
    
    response = {'success': True, 'path_in': path_in, 'filename_in': upload.filename, 'path_out': path_out, 'files_out': files_out, 'file_out': file_out, 'files_shp': files_shp}
    return response
    
@app.route('/upload', method='POST')
def do_upload():
    category   = bottle.request.forms.get('category')
    upload     = bottle.request.files.get('file')
    name, ext = os.path.splitext(upload.filename)
    '''
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    '''
    #save_path = get_save_path_for_category(category)
    upload.save('.') # appends upload.filename automatically
    return upload.filename
    
@app.route('/test', method='POST')
def test():
    response = {'success': True, 'path_in': 'path_in', 'filename_in': 'upload.filename', 'path_out': 'path_out', 'files_out': {'src': 'name'+'.xlsx', 'dst': 'name'+'.xml'}, 'file_out': 'file_out'}
    return response
    
@app.route('/page/<name>')
def show_page(name):
    '''
    show how to use a simple template for rendering.
    '''
    #return str(bottle.TEMPLATE_PATH) ##+ 
    try:
        return bottle.template('page', url_name=name)
    except Exception, e:
        return "<p>Error: %s</p> <p>%s</p>" % (str(e), os.getcwd())

# Run bottle internal test server when invoked directly ie: non-uxsgi mode
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8081, debug=True, reloader=True)
# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
    app = application = bottle.default_app()
