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

import sys
import os
import json
import datetime
import xml.dom.minidom
import xml.etree.ElementTree
import uuid
import copy
import codecs
import re

import openpyxl


def _get_json(filename=None):
    extension = os.path.splitext(filename)[1]
    if os.path.isfile(filename) and extension == '.json':
        with open(filename) as file:
            return json.load(file)

_root = os.path.dirname(__file__)
_json_config = _get_json(os.path.join(_root, "json/md_config.json"))
#md_dict = _get_json(os.path.join(_root, "json/md_data.json"))


def _get_xml_item_value(element, xpath, namespaces, attribute=None):
    item = element.find(xpath, namespaces)
    if item is not None:
        if attribute is not None:
            return item.attrib[attribute]
        else:
            return item.text
    else:
        return None

def _get_xml_item_values(element, xpath, namespaces, attribute=None):
    items = element.findall(xpath, namespaces)
    results = []
    for item in items:
        if item is not None:
            if attribute is not None:
                results.append(item.attrib[attribute])
            else:
                results.append(item.text)
    return results

def _get_xml_contacts_values(root, md_xpaths, namespaces, element):
    contacts = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            contact = {}
            contact['name'] = _get_xml_item_value(item, md_xpaths['cntname'], namespaces, None)
            contact['position'] = _get_xml_item_value(item, md_xpaths['cntposition'], namespaces, None)
            contact['organisation'] = _get_xml_item_value(item, md_xpaths['cntorganism'], namespaces, None)
            contact['email'] = _get_xml_item_value(item, md_xpaths['cntemail'], namespaces, None)
            contact['tel'] = _get_xml_item_value(item, md_xpaths['cnttel'], namespaces, None)
            contact['address'] = _get_xml_item_value(item, md_xpaths['cntaddress'], namespaces, None)
            contact['cp'] = _get_xml_item_value(item, md_xpaths['cntpostalcode'], namespaces, None)
            contact['city'] = _get_xml_item_value(item, md_xpaths['cntcity'], namespaces, None)
            contact['logo_url'] = _get_xml_item_value(item, md_xpaths['cntlogourl'], namespaces, 'src')
            contact['logo_text'] = _get_xml_item_value(item, md_xpaths['cntlogotext'], namespaces, None)
            contact['role'] = _get_xml_item_value(item, md_xpaths['cntrole'], namespaces, 'codeListValue')
            contacts.append(contact)
    return contacts

def _get_xml_dates_values(root, md_xpaths, namespaces, element):
    dates = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            date = {}
            date['datetype'] = _get_xml_item_value(item, md_xpaths['datetype'], namespaces, None)
            date['date'] = _get_xml_item_value(item, md_xpaths['date'], namespaces, None)
            dates.append(date)
    return dates 

def _get_xml_identifiers_values(root, md_xpaths, namespaces, element):
    identifiers = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            identifier = {}
            identifier['code'] = _get_xml_item_value(item, md_xpaths['data_identifiercode'], namespaces, None)
            identifier['codespace'] = _get_xml_item_value(item, md_xpaths['data_identifierspacename'], namespaces, None)
            identifiers.append(identifier)
    return identifiers 

def _get_xml_browsegraphics_values(root, md_xpaths, namespaces, element):
    browsegraphics = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            browsegraphic = {}
            browsegraphic['url'] = _get_xml_item_value(item, md_xpaths['data_graphicoverviewname'], namespaces, None)
            browsegraphic['description'] = _get_xml_item_value(item, md_xpaths['data_graphicoverviewdescription'], namespaces, None)
            browsegraphic['type'] = _get_xml_item_value(item, md_xpaths['data_graphicoverviewtype'], namespaces, None)
            browsegraphics.append(browsegraphic)
    return browsegraphics

def _get_xml_keywords_values(root, md_xpaths, namespaces, element):
    keywords = []
    inspire_keywords = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            keyword = {}
            keyword['keyword'] = _get_xml_item_value(item, md_xpaths['data_keyword'], namespaces, None)
            keyword['type'] = _get_xml_item_value(item, md_xpaths['data_keywordtypecode'], namespaces, 'codeListValue')
            keyword['thesaurus_name'] = _get_xml_item_value(item, md_xpaths['data_keywordthesaurus'], namespaces, None)
            keyword['thesaurus_dates'] = _get_xml_dates_values(item, md_xpaths, namespaces, 'data_keywordthesaurusdates')
        if keyword['thesaurus_name'] is not None and 'inspire' in keyword['thesaurus_name'].lower():
            inspire_keywords.append(keyword)
        else:
            keywords.append(keyword)
    return keywords, inspire_keywords
'''
def _get_xml_geographicextents_values(root, md_xpaths, namespaces, element):
    geographicextents = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            geographicextent = {}
            geographicextent['name'] = _get_xml_item_value(item, md_xpaths['data_geographicextentname'], namespaces, None)
            geographicextent['xmin'] = _get_xml_item_value(item, md_xpaths['data_geographicextentwest'], namespaces, None)
            geographicextent['xmax'] = _get_xml_item_value(item, md_xpaths['data_geographicextenteast'], namespaces, None)
            geographicextent['ymin'] = _get_xml_item_value(item, md_xpaths['data_geographicextentsouth'], namespaces, None)
            geographicextent['ymax'] = _get_xml_item_value(item, md_xpaths['data_geographicextentnorth'], namespaces, None)
            geographicextents.append(geographicextent)
    return geographicextents
'''
def _get_xml_extents_values(root, md_xpaths, namespaces, element, type):
    extents = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            extent = {}
            extent['name'] = _get_xml_item_value(item, md_xpaths['data_extentname'], namespaces, None)
            if type == 'geographicextents':
                geographicextents = item.findall(md_xpaths['data_geographicextents'], namespaces)
                for geographicextent in geographicextents:
                    if geographicextent is not None:
                        extent['xmin'] = _get_xml_item_value(geographicextent, md_xpaths['data_geographicextentwest'], namespaces, None)
                        extent['xmax'] = _get_xml_item_value(geographicextent, md_xpaths['data_geographicextenteast'], namespaces, None)
                        extent['ymin'] = _get_xml_item_value(geographicextent, md_xpaths['data_geographicextentsouth'], namespaces, None)
                        extent['ymax'] = _get_xml_item_value(geographicextent, md_xpaths['data_geographicextentnorth'], namespaces, None)
            elif type == 'temporalextents':
                temporalextents = item.findall(md_xpaths['data_temporalextents'], namespaces)
                for temporalextent in temporalextents:
                    if temporalextent is not None:
                        extent['start'] = _get_xml_item_value(temporalextent, md_xpaths['data_temporalextentbegin'], namespaces, None)
                        extent['end'] = _get_xml_item_value(temporalextent, md_xpaths['data_temporalextentend'], namespaces, None)
                        extent['description'] = _get_xml_item_value(temporalextent, md_xpaths['data_temporalextentdescription'], namespaces, None)
            elif type == 'verticalextents':
                verticalextents = item.findall(md_xpaths['data_geographicextents'], namespaces)
                for verticalextent in verticalextents:
                    if verticalextent is not None:
                        extent['datum'] = _get_xml_item_value(verticalextent, md_xpaths['data_verticalextentdatum'], namespaces, None)
                        extent['uom'] = _get_xml_item_value(verticalextent, md_xpaths['data_verticalextentuom'], namespaces, None)
                        extent['min'] = _get_xml_item_value(verticalextent, md_xpaths['data_verticalextentmin'], namespaces, None)
                        extent['max'] = _get_xml_item_value(verticalextent, md_xpaths['data_verticalextentmax'], namespaces, None)
            extents.append(extent)
    return extents
'''
def _get_xml_temporalextents_values(root, md_xpaths, namespaces, element):
    temporalextents = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            temporalextent = {}
            temporalextent['start'] = _get_xml_item_value(item, md_xpaths['data_temporalextentbegin'], namespaces, None)
            temporalextent['end'] = _get_xml_item_value(item, md_xpaths['data_temporalextentend'], namespaces, None)
            temporalextent['description'] = _get_xml_item_value(item, md_xpaths['data_temporalextentdescription'], namespaces, None)
            temporalextents.append(temporalextent)
    return temporalextents
    '''
def _get_xml_referencesystems_values(root, md_xpaths, namespaces, element):
    referencesystems = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            referencesystem = {}
            referencesystem['code'] = _get_xml_item_value(item, md_xpaths['data_referencesystemcode'], namespaces, None)
            #referencesystem['codespace'] = _get_xml_item_value(item, md_xpaths['data_referencesystemcodespace'], namespaces, None)
            referencesystems.append(referencesystem)
    return referencesystems

def _get_xml_distformats_values(root, md_xpaths, namespaces, element):
    distformats = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            distformat = {}
            distformat['name'] = _get_xml_item_value(item, md_xpaths['data_distformatname'], namespaces, None)
            distformat['version'] = _get_xml_item_value(item, md_xpaths['data_distformatversion'], namespaces, None)
            distformat['specification'] = _get_xml_item_value(item, md_xpaths['data_distformatspecification'], namespaces, None)
            distformats.append(distformat)
    return distformats

def _get_xml_linkages_values(root, md_xpaths, namespaces, element):
    linkages = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            linkage = {}
            linkage['name'] = _get_xml_item_value(item, md_xpaths['data_linkagename'], namespaces, None)
            linkage['description'] = _get_xml_item_value(item, md_xpaths['data_linkagedescription'], namespaces, None)
            linkage['url'] = _get_xml_item_value(item, md_xpaths['data_linkageurl'], namespaces, None)
            linkage['protocol'] = _get_xml_item_value(item, md_xpaths['data_linkageprotocol'], namespaces, None)
            linkages.append(linkage)
    return linkages

def _get_xml_conformities_values(root, md_xpaths, namespaces, element):
    conformities = []
    items = root.findall(md_xpaths[element], namespaces)
    for item in items:
        if item is not None:
            conformitie = {}
            conformitie['specification'] = _get_xml_item_value(item, md_xpaths['dq_inspireconformitytitle'], namespaces, None)
            conformitie['explaination'] = _get_xml_item_value(item, md_xpaths['dq_inspireconformitydescription'], namespaces, None)
            conformitie['pass'] = _get_xml_item_value(item, md_xpaths['dq_inspireconformitypass'], namespaces, None)
            conformitie['dates'] = _get_xml_dates_values(item, md_xpaths, namespaces, 'dq_inspireconformitydates')
            conformities.append(conformitie)
    return conformities
        
        
def xml_to_dict(xml_file=None, md_dict={}):
    """
    Convert xml file to Python dictionary
    Return Python dictionary or False
    """
    
    if os.path.isfile(xml_file):
        # Get md_codelist.json file
        _json_xpaths = _get_json(os.path.join(_root, "json/md_xpaths.json"))

        namespaces = _json_config['namespaces']
        root = xml.etree.ElementTree.parse(xml_file)

        md_dict = {}
        md_dict['md_fileidentifier'] = _get_xml_item_value(root, _json_xpaths['md_fileidentifier'], namespaces, None)
        md_dict['md_language'] = _get_xml_item_value(root, _json_xpaths['md_language'], namespaces, 'codeListValue')
        md_dict['md_characterset'] = _get_xml_item_value(root, _json_xpaths['md_characterset'], namespaces, 'codeListValue')
        md_dict['md_hierarchylevel'] = _get_xml_item_value(root, _json_xpaths['md_hierarchylevel'], namespaces, 'codeListValue')
        md_dict['md_contacts'] = _get_xml_contacts_values(root, _json_xpaths, namespaces, 'md_contacts')
        md_dict['md_datestamp'] = _get_xml_item_value(root, _json_xpaths['md_datestamp'], namespaces, None)
        md_dict['md_standardname'] = _get_xml_item_value(root, _json_xpaths['md_standardname'], namespaces, None)
        md_dict['md_standardversion'] = _get_xml_item_value(root, _json_xpaths['md_standardversion'], namespaces, None)
        md_dict['data_title'] = _get_xml_item_value(root, _json_xpaths['data_title'], namespaces, None)
        md_dict['data_dates'] = _get_xml_dates_values(root, _json_xpaths, namespaces, 'data_dates')
        md_dict['data_identifiers'] = _get_xml_identifiers_values(root, _json_xpaths, namespaces, 'data_identifiers')
        md_dict['data_abstract'] = _get_xml_item_value(root, _json_xpaths['data_abstract'], namespaces, None)
        md_dict['data_browsegraphics'] = _get_xml_browsegraphics_values(root, _json_xpaths, namespaces, 'data_graphicoverviews')
        md_dict['data_maintenancefrequencycode'] = _get_xml_item_value(root, _json_xpaths['data_maintenancefrequency'], namespaces, 'codeListValue')
        md_dict['data_temporalextents'] = _get_xml_extents_values(root, _json_xpaths, namespaces, 'data_temporalextents', 'temporalextents')
        md_dict['data_languages'] = _get_xml_item_values(root, _json_xpaths['data_languagecodes'], namespaces, 'codeListValue')
        md_dict['data_topiccategories'] = _get_xml_item_values(root, _json_xpaths['data_topiccategories'], namespaces, None)
        md_dict['data_keywords'], md_dict['data_inspirekeywords'] = _get_xml_keywords_values(root, _json_xpaths, namespaces, 'data_keywords')
        md_dict['data_contacts'] = _get_xml_contacts_values(root, _json_xpaths, namespaces, 'data_contacts')
        md_dict['data_geographicextents'] = _get_xml_extents_values(root, _json_xpaths, namespaces, 'data_extents', 'geographicextents')
        md_dict['data_referencesystems'] = _get_xml_identifiers_values(root, _json_xpaths, namespaces, 'data_referencesystems')

        md_dict['data_presentationform'] = _get_xml_item_value(root, _json_xpaths['data_presentationform'], namespaces, 'codeListValue')
        md_dict['data_spatialrepresentationtype'] = _get_xml_item_value(root, _json_xpaths['data_spatialrepresentationtype'], namespaces, 'codeListValue')
        md_dict['data_scaledenominator'] = _get_xml_item_value(root, _json_xpaths['data_scaledenominator'], namespaces, None)
        md_dict['data_scaledistance'] = _get_xml_item_value(root, _json_xpaths['data_scaledistance'], namespaces, None)
        md_dict['data_dq_level'] = _get_xml_item_value(root, _json_xpaths['dq_level'], namespaces, 'codeListValue')
        md_dict['data_li_statement'] = _get_xml_item_value(root, _json_xpaths['li_statement'], namespaces, None)
        md_dict['data_characterset'] = _get_xml_item_value(root, _json_xpaths['data_characterset'], namespaces, 'codeListValue')

        md_dict['data_distformats'] = _get_xml_distformats_values(root, _json_xpaths, namespaces, 'data_distformats')

        md_dict['data_uselimitations'] = _get_xml_item_values(root, _json_xpaths['data_uselimitations'], namespaces, None)
        md_dict['data_legal_uselimitations'] = _get_xml_item_values(root, _json_xpaths['data_legal_uselimitations'], namespaces, None)
        md_dict['data_legal_useconstraints'] = _get_xml_item_values(root, _json_xpaths['data_legal_useconstraints'], namespaces, 'codeListValue')
        md_dict['data_legal_accessconstraints'] = _get_xml_item_values(root, _json_xpaths['data_legal_accessconstraints'], namespaces, 'codeListValue')
        md_dict['data_legal_otherconstraints'] = _get_xml_item_values(root, _json_xpaths['data_legal_otherconstraints'], namespaces, None)
        md_dict['data_security_uselimitations'] = _get_xml_item_values(root, _json_xpaths['data_security_uselimitations'], namespaces, None)
        md_dict['data_security_classification'] = _get_xml_item_value(root, _json_xpaths['data_security_classification'], namespaces, 'codeListValue')

        md_dict['data_linkages'] = _get_xml_linkages_values(root, _json_xpaths, namespaces, 'data_linkages')
        md_dict['data_dq_inspireconformities'] = _get_xml_conformities_values(root, _json_xpaths, namespaces, 'dq_inspireconformities')

        return md_dict

    else:
        return False

        
if __name__ == "__main__":        
    xml_file = 'xml/FR-341142131-ARAA_BDSol-Alsace_250000_2011.xml'
    print xml_to_dict(xml_file)

