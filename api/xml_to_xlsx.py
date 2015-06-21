#!/usr/bin/env python
# -*- coding: utf8 -*-

""" XML => XLSX """

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

import xml_to_dict
import dict_to_xlsx

def convert(xml_file, xlsx_file, xlsx_template, md_dict={}):
    #print xml_file, xlsx_file, xlsx_template,  path_out, md_dict
    path_in, name_in = os.path.split(xml_file)
    filename_in, ext_in = os.path.splitext(name_in)
    
    # Charger fichier JSON par défaut
    json_file = os.path.join(path_in, filename_in + '.json')
    if not os.path.isfile(json_file):
        json_file = 'md.json'
    if os.path.isfile(json_file):
        with open(json_file, 'r') as md_file:
            md_dict = json.load(md_file)

    xml_dict = xml_to_dict.xml_to_dict(xml_file, md_dict)
    # print xml_dict

    #pprint.pprint(xml_dict)
    #md_dict = _get_json(os.path.join(_root, "json/md_data.json"))   
    md_xlsx = dict_to_xlsx.dict_to_xlsx(xml_dict, xlsx_file, xlsx_template)

if __name__ == "__main__":
    xml_file = 'test/xml/FR-341142131-ARAA_BDSol-Alsace_250000_2011.xml'
    print convert(xml_file, 'test/xlsx/test2.xlsx', 'test/xlsx/MODELE-VIDE_FicheMD-CIGAL_simple_150428.xlsx')
