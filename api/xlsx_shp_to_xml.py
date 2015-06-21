#!/usr/bin/env python
# -*- coding: utf8 -*-

""" XLSX + SHP => XML """

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2015, CIGAL"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume@ryckelynck.info"
__status__ = "Prototype"

import os
import glob
import json
import pprint
import re

import xlsx_to_dict
import dict_to_xml
import shp_info

def convert(xlsx_file, path_out='.', md_dict={}):
    #print xlsx_file
    path_in, name_in = os.path.split(xlsx_file)
    filename_in, ext_in = os.path.splitext(name_in)
    
    # Charger fichier JSON par défaut
    json_file = os.path.join(path_in, filename_in + '.json')
    if not os.path.isfile(json_file):
        json_file = 'md.json'
    if os.path.isfile(json_file):
        with open(json_file, 'r') as md_file:
            md_dict = json.load(md_file)

    xlsx_dict = xlsx_to_dict.xlsx_to_dict(xlsx_file, md_dict)
    #print xlsx_dict

    # fileIndentifier
    fileidentifier = False
    if 'md_fileidentifier' in xlsx_dict:
        if xlsx_dict['md_fileidentifier']: fileidentifier = True
        #print xlsx_dict['md_fileidentifier']
    if not fileidentifier:
        xlsx_dict['md_fileidentifier'] = filename_in
        if 'data_identifiers' in xlsx_dict:
            if xlsx_dict['data_identifiers']: xlsx_dict['md_fileidentifier'] = xlsx_dict['data_identifiers'][0]['code']
            #print xlsx_dict['md_fileidentifier']
    #print fileidentifier
    #print xlsx_dict['md_fileidentifier']
    
    # data_languages
    # Supprimer les doublons le cas échéant
    if 'data_languages' in xlsx_dict:
        if len(xlsx_dict['data_languages']) > 1:
            xlsx_dict['data_languages'] = list(set(xlsx_dict['data_languages']))

    # data_keywords_list
    keywords = []
    if 'data_keywords' in xlsx_dict:
        for k, v in enumerate(xlsx_dict['data_keywords']):
            keywords.append(v['keyword'])
    if 'data_keywords_list' in xlsx_dict:
        data_keywords = [kw.strip() for kw in re.split(';|,', xlsx_dict['data_keywords_list'])]
        if not 'data_keywords' in xlsx_dict: xlsx_dict['data_keywords'] = []
        for data_keyword in data_keywords:
            if data_keyword and data_keyword not in keywords:
                xlsx_dict['data_keywords'].append({'keyword': data_keyword, 'type': 'theme'})

    # data_spatialrepresentationtype
    VectorCode = ["SHP", "MIF/MID", "KML", "GeoJSON", "WFS"]
    data_spatialrepresentationtype = False
    if 'data_spatialrepresentationtype' in xlsx_dict:
        if xlsx_dict['data_spatialrepresentationtype']: data_spatialrepresentationtype = True
    if not data_spatialrepresentationtype:
        xlsx_dict['data_spatialrepresentationtype'] = 'grid'
        for format in md_dict['data_distformats']:
            # print format
            # if 'name' in format:
            for value in VectorCode:
                if value in format['name']: xlsx_dict['data_spatialrepresentationtype'] = 'vector'
                
    # data_browsegraphic
    data_browsegraphic_file = filename_in+'.jpg'
    if os.path.isfile(os.path.join(path_in, data_browsegraphic_file)): 
        if not 'data_browsegraphics' in xlsx_dict:
            xlsx_dict['data_browsegraphics'] = []
        if 'server_ressources' in xlsx_dict:
            data_browsegraphic_file = os.path.join(xlsx_dict['server_ressources'], data_browsegraphic_file)
        xlsx_dict['data_browsegraphics'].append({ "url": data_browsegraphic_file, "description": "illustration", "type": "jpg" })

    # Logos
    if 'data_contacts' in xlsx_dict:
        for id, cnt in enumerate(xlsx_dict['data_contacts']):
            if 'logo_url' in cnt:
                if cnt['logo_url']:
                    if not cnt['logo_url'].startswith('http') and 'server_logos' in xlsx_dict:
                        xlsx_dict['data_contacts'][id]['logo_url'] = os.path.join(xlsx_dict['server_logos'], cnt['logo_url'])

    # Ressources location
    # TODO: A tester!
    if 'data_linkages' in xlsx_dict:
        for id, linkage in enumerate(xlsx_dict['data_linkages']):
            if 'url' in linkage:
                if linkage['url']:
                    if not linkage['url'].startswith('http') and 'server_ressources' in xlsx_dict:
                        xlsx_dict['data_linkages'][id]['url'] = os.path.join(xlsx_dict['server_ressources'], linkage['url'])

    # shp file
    shp_dict = None
    shp_file = os.path.join(path_in, filename_in+'.shp')
    if os.path.isfile(shp_file):
        shp_dict = shp_info.get_shp_info(shp_file)

    # geographic extent
    if xlsx_dict['data_geographicextents']:
        for i, data_geographicextent in enumerate(xlsx_dict['data_geographicextents']):
            if 'name' in xlsx_dict['data_geographicextents'][i]:
                if xlsx_dict['data_geographicextents'][i]['name']: xlsx_dict['data_keywords'].append({'keyword': xlsx_dict['data_geographicextents'][i]['name'], 'type': 'place'})
            if any(not x for x in xlsx_dict['data_geographicextents'][i].values()) and shp_dict is not None:
                xlsx_dict['data_geographicextents'][i]['xmin'] = shp_dict['extent_wgs84']['xmin']
                xlsx_dict['data_geographicextents'][i]['xmax'] = shp_dict['extent_wgs84']['xmax']
                xlsx_dict['data_geographicextents'][i]['ymin'] = shp_dict['extent_wgs84']['ymin']
                xlsx_dict['data_geographicextents'][i]['ymax'] = shp_dict['extent_wgs84']['ymax']
    elif shp_dict is not None:
        xlsx_dict['data_geographicextents'].append(shp_dict['extent_wgs84'])

    # système de projection
    if shp_dict is not None:
        if 'epsg' in shp_dict:
            xlsx_dict['data_referencesystems'] = [{ 'code': shp_dict['epsg'], 'codespace': 'EPSG' }]

    pprint.pprint(xlsx_dict)
    #md_dict = _get_json(os.path.join(_root, "json/md_data.json"))   
    md_xml = dict_to_xml.dict_to_xml(xlsx_dict, filename_in+'.xml', path_out)

if __name__ == "__main__":
    xlsx_file = 'test/xlsx/FR-341142131-ARAA_BDSol-Alsace_250000_2011.xlsx'
    print convert(xlsx_file, 'test/xlsx')

