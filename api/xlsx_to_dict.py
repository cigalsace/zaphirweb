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
import re

try:
    import openpyxl
    openpyxl_actif = True
except ImportError:
    print "Error with openpyxl module"
    openpyxl_actif = False

def _get_json(filename=None):
    extension = os.path.splitext(filename)[1]
    if os.path.isfile(filename) and extension == '.json':
        with open(filename) as file:
            return json.load(file)

_root = os.path.dirname(__file__)
_json_config = _get_json(os.path.join(_root, "json/md_config.json"))
# Get md_data.json
#md_dict = _get_json(os.path.join(_root, "json/md_data.json"))

def _get_cell_value(wb, cell_name='', cell_type='', cell_codelist={}):
    """
    """
    cell_names = [cell_name, cell_name.lower(), cell_name.upper()]
    for c_name in cell_names:
        cell = wb.get_named_range(c_name)
        #print cell
        if cell:
            ws = cell.destinations[0][0]
            c = ws.cell(cell.destinations[0][1])
            c_value = c.value or None
            if c_value:
                if cell_type == 'date':
                    #print datetime.date(1899, 12, 30) + datetime.timedelta(days=c_value)
                    return datetime.date(1899, 12, 30) + datetime.timedelta(days=c.internal_value)
                    #return c_value.strftime('%Y-%m-%d')
                elif cell_type == 'code':
                    regex = re.compile('[0-9]{1,6}')
                    code = re.match(regex, c_value)
                    if code:
                        return cell_codelist[code.group()]
                    else: 
                        return c_value
                else:
                    return c_value
        else:
            return False

def _get_contact(wb, type='', i=0, _json_codelist={}):
    cnt = {}
    cnt['name'] = _get_cell_value(wb, type+'_contact'+str(i)+'_name')
    cnt['position'] = _get_cell_value(wb, type+'_contact'+str(i)+'_position')
    cnt['organisation'] = _get_cell_value(wb, type+'_contact'+str(i)+'_organisation')
    cnt['tel'] = _get_cell_value(wb, type+'_contact'+str(i)+'_tel')
    cnt['email'] = _get_cell_value(wb, type+'_contact'+str(i)+'_email')
    cnt['address'] = _get_cell_value(wb, type+'_contact'+str(i)+'_address')
    cnt['cp'] = _get_cell_value(wb, type+'_contact'+str(i)+'_cp')
    cnt['city'] = _get_cell_value(wb, type+'_contact'+str(i)+'_city')
    cnt['logo_url'] = _get_cell_value(wb, type+'_contact'+str(i)+'_logo')
    cnt['role'] = _get_cell_value(wb, type+'_contact'+str(i)+'_role', 'code', _json_codelist['RoleCode'])
    return cnt

def xlsx_to_dict(xlsx_file=None, md_dict={}):
    """
    Convert XLSX file to Python dictionary
    Return Python dictionary or False
    """

    if os.path.isfile(xlsx_file):
        # Get md_codelist.json file
        _json_codelist = _get_json(os.path.join(_root, "json/md_codelist.json"))
        
        # md_dict = {}
        wb = openpyxl.load_workbook(xlsx_file)

        '''
        named_ranges = wb.get_named_ranges()
        print named_ranges
        for a in named_ranges:
            print a.name
        '''
        
        # md_fileidentifier
        if _get_cell_value(wb, 'info_fileidentifier'): 
            md_dict['md_fileidentifier'] = _get_cell_value(wb, 'info_fileidentifier')
        # md_language
        if _get_cell_value(wb, 'info_language', 'code', _json_codelist['LanguageCode']): 
            md_dict['md_language'] = _get_cell_value(wb, 'info_language', 'code', _json_codelist['LanguageCode'])
        # md_characterset
        if _get_cell_value(wb, 'info_characterset', 'code', _json_codelist['CharacterSetCode']): 
            md_dict['md_characterset'] = _get_cell_value(wb, 'info_characterset', 'code', _json_codelist['CharacterSetCode'])
        # md_hierarchylevel
        if _get_cell_value(wb, 'info_hierarchylevel', 'code', _json_codelist['ScopeCode']): 
            md_dict['md_hierarchylevel'] = _get_cell_value(wb, 'info_hierarchylevel', 'code', _json_codelist['ScopeCode'])

        # md_contacts
        if not 'md_contacts' in md_dict: md_dict['md_contacts'] = []
        for i in range(1, 21):
            cnt = _get_contact(wb, 'info', i, _json_codelist)
            if cnt['name'] or cnt['organisation']:
                md_dict['md_contacts'].append(cnt)

        # data_contacts
        if not 'data_contacts' in md_dict: md_dict['data_contacts'] = []
        for i in range(1, 21):
            cnt = _get_contact(wb, 'data', i, _json_codelist)
            if cnt['name'] or cnt['organisation']:
                md_dict['data_contacts'].append(cnt)

        # md_datestamp
        if _get_cell_value(wb, 'info_datestamp', 'date'):
            md_dict['md_datestamp'] = _get_cell_value(wb, 'info_datestamp', 'date')
        # md_standardname
        if _get_cell_value(wb, 'info_standardname'):
            md_dict['md_standardname'] = _get_cell_value(wb, 'info_standardname')
        # md_standardversion
        if _get_cell_value(wb, 'info_standardversion'):
            md_dict['md_standardversion'] = _get_cell_value(wb, 'info_standardversion')
        # data_title
        if _get_cell_value(wb, 'data_title'):
            md_dict['data_title'] = _get_cell_value(wb, 'data_title')
        
        # data_dates
        if not 'data_dates' in md_dict: md_dict['data_dates'] = []
        data_datecreation = _get_cell_value(wb, 'data_datecreation', 'date')
        if data_datecreation:
            date = { 'date': data_datecreation, 'type': 'creation'}
            md_dict['data_dates'].append(date)
        data_daterevision = _get_cell_value(wb, 'data_daterevision', 'date')
        if data_daterevision:
            date = { 'date': data_daterevision, 'type': 'revision'}
            md_dict['data_dates'].append(date)
        data_datepublication = _get_cell_value(wb, 'data_datepublication', 'date')
        if data_datepublication:
            date = { 'date': data_datepublication, 'type': 'publication'}
            md_dict['data_dates'].append(date)
        
        # data_identifiers
        if not 'data_identifiers' in md_dict: md_dict['data_identifiers'] = []
        for i in range(1, 21):
            code = _get_cell_value(wb, 'data_identifier'+str(i)+'_code')
            codespace = _get_cell_value(wb, 'data_identifier'+str(i)+'_codespace')
            if code:
                data_identifier = {'code': code, 'codesapce': codespace}
                md_dict['data_identifiers'].append(data_identifier)

        # data_abstract
        if _get_cell_value(wb, 'data_abstract'):
            md_dict['data_abstract'] = _get_cell_value(wb, 'data_abstract')

        # data_browsegraphics
        if not 'data_browsegraphics' in md_dict: md_dict['data_browsegraphics'] = []
        for i in range(1, 21):
            url = _get_cell_value(wb, 'data_browsegraphic'+str(i)+'_url')
            description = _get_cell_value(wb, 'data_browsegraphic'+str(i)+'_description')
            type = _get_cell_value(wb, 'data_browsegraphic'+str(i)+'_type')
            if url:
                data_browsegraphic = {'url': url, 'description': description, 'type': type}
                md_dict['data_browsegraphics'].append(data_browsegraphic)

        # data_maintenancefrequency
        if _get_cell_value(wb, 'data_maintenancefrequency', 'code', _json_codelist['MaintenanceFrequencyCode']):
            md_dict['data_maintenancefrequencycode'] = _get_cell_value(wb, 'data_maintenancefrequency', 'code', _json_codelist['MaintenanceFrequencyCode'])

        # data_temporalextents
        if not 'data_temporalextents' in md_dict: md_dict['data_temporalextents'] = []
        for i in range(1, 21):
            start = _get_cell_value(wb, 'data_temporalextent'+str(i)+'_start')
            end = _get_cell_value(wb, 'data_temporalextent'+str(i)+'_end')
            description = _get_cell_value(wb, 'data_temporalextent'+str(i)+'_description')
            if start:
                data_temporalextent = {'start': start, 'end': end, 'description': description}
                md_dict['data_temporalextents'].append(data_temporalextent)

        # data_languages
        if not 'data_languages' in md_dict: md_dict['data_languages'] = []
        for i in range(1, 21):
            # language = _get_cell_value(wb, 'data_language'+str(i))
            language = _get_cell_value(wb, 'data_language'+str(i), 'code', _json_codelist['LanguageCode'])
            if language:
                md_dict['data_languages'].append(language)

        # data_topiccategories
        if not 'data_topiccategories' in md_dict: md_dict['data_topiccategories'] = []
        for i in range(1, 21):
            topiccategory = _get_cell_value(wb, 'data_topiccategory'+str(i), 'code', _json_codelist['TopicCategoryCode'])
            if topiccategory:
                md_dict['data_topiccategories'].append(topiccategory)

        # data_keywords_list
        if _get_cell_value(wb, 'data_keywords'):
            md_dict['data_keywords_list'] = _get_cell_value(wb, 'data_keywords')

        # data_keywords
        if not 'data_keywords' in md_dict: md_dict['data_keywords'] = []
        for i in range(1, 21):
            keyword = {}
            keyword['keyword'] = _get_cell_value(wb, 'data_keyword'+str(i)+'_keyword')
            keyword['type'] = _get_cell_value(wb, 'data_keyword'+str(i)+'_type', 'code', _json_codelist['KeywordTypeCode'])
            keyword['thesaurus_name'] = _get_cell_value(wb, 'data_keyword'+str(i)+'_thesaurusname')
            if not 'thesaurus_dates' in keyword: keyword['thesaurus_dates'] = []
            # keyword['thesaurus_dates'] = []
            thesaurusdatecreation = _get_cell_value(wb, 'data_keyword'+str(i)+'_thesaurusdatecreation', 'date')
            if thesaurusdatecreation:
                date = { 'date': datecreation, 'type': 'creation'}
                keyword['thesaurus_dates'].append(date)
            thesaurusdaterevision = _get_cell_value(wb, 'data_keyword'+str(i)+'_thesaurusdaterevision', 'date')
            if thesaurusdaterevision:
                date = { 'date': daterevision, 'type': 'revision'}
                keyword['thesaurus_dates'].append(date)
            thesaurusdatepublication = _get_cell_value(wb, 'data_keyword'+str(i)+'_thesaurusdatepublication', 'date')
            if thesaurusdatepublication:
                date = { 'date': datepublication, 'type': 'publication'}
                keyword['thesaurus_dates'].append(date)
            if keyword:
                md_dict['data_keywords'].append(keyword)
        
        # data_inspirekeywords
        if not 'data_inspirekeywords' in md_dict: md_dict['data_inspirekeywords'] = []
        for i in range(1, 21):
            keyword = {}
            keyword['keyword'] = _get_cell_value(wb, 'data_inspirekeyword'+str(i)+'_keyword', 'code', _json_codelist['InspireThemeCode_en'])
            keyword['type'] = 'theme'
            keyword['thesaurus_name'] = 'GEMET - INSPIRE themes, v.1.0'
            keyword['thesaurus_dates'] = []
            #keyword['thesaurus_dates'].append({ 'date': '', 'type': 'creation'})
            #keyword['thesaurus_dates'].append({ 'date': '', 'type': 'revision'})
            keyword['thesaurus_dates'].append({ 'date': '2008-06-01', 'type': 'publication'})
            if 'keyword' in keyword:
                if keyword['keyword']:
                    md_dict['data_inspirekeywords'].append(keyword)
        
        # data_geographicextents
        if not 'data_geographicextents' in md_dict: md_dict['data_geographicextents'] = []
        for i in range(1, 21):
            name = _get_cell_value(wb, 'data_geographicextent'+str(i)+'_name')
            xmin = _get_cell_value(wb, 'data_geographicextent'+str(i)+'_xmin')
            xmax = _get_cell_value(wb, 'data_geographicextent'+str(i)+'_xmax')
            ymin = _get_cell_value(wb, 'data_geographicextent'+str(i)+'_ymin')
            ymax = _get_cell_value(wb, 'data_geographicextent'+str(i)+'_ymax')
            if xmin or name:
                data_geographicextent = {'name': name, 'xmin': xmin, 'xmax': ymin, 'ymin': xmax, 'ymax': ymax}
                md_dict['data_geographicextents'].append(data_geographicextent)

        # data_referencesystems
        if not 'data_referencesystems' in md_dict: md_dict['data_referencesystems'] = []
        for i in range(1, 21):
            code = _get_cell_value(wb, 'data_referencesystem'+str(i)+'_code', 'code', _json_codelist['ReferenceSystemCode'])
            codespace = _get_cell_value(wb, 'data_referencesystem'+str(i)+'_codespace')
            if code:
                data_referencesystem = {'code': code, 'codesapce': codespace}
                md_dict['data_referencesystems'].append(data_referencesystem)
        
        # data_presentationform
        if _get_cell_value(wb, 'data_presentationform'):
            md_dict['data_presentationform'] = _get_cell_value(wb, 'data_presentationform')
        # data_spatialrepresentationtype
        if _get_cell_value(wb, 'data_spatialrepresentationtype', 'code', _json_codelist['SpatialRepresentationTypeCode']):
            md_dict['data_spatialrepresentationtype'] = _get_cell_value(wb, 'data_spatialrepresentationtype', 'code', _json_codelist['SpatialRepresentationTypeCode'])
        # data_scaledenominator
        if _get_cell_value(wb, 'data_scaledenominator'):
            md_dict['data_scaledenominator'] = _get_cell_value(wb, 'data_scaledenominator')
        # data_scaledistance
        if _get_cell_value(wb, 'data_scaledistance'):
            md_dict['data_scaledistance'] = _get_cell_value(wb, 'data_scaledistance')
        # data_dq_level
        if _get_cell_value(wb, 'data_dq_level', 'code', _json_codelist['ScopeCode']):
            md_dict['data_dq_level'] = _get_cell_value(wb, 'data_dq_level', 'code', _json_codelist['ScopeCode'])
        # data_li_statement
        if _get_cell_value(wb, 'data_li_statement'):
            md_dict['data_li_statement'] = _get_cell_value(wb, 'data_li_statement')
        # data_characterset
        if _get_cell_value(wb, 'data_characterset', 'code', _json_codelist['CharacterSetCode']):
            md_dict['data_characterset'] = _get_cell_value(wb, 'data_characterset', 'code', _json_codelist['CharacterSetCode'])
        
        # data_distformats
        if not 'data_distformats' in md_dict: md_dict['data_distformats'] = []
        for i in range(1, 21):
            name = _get_cell_value(wb, 'data_distformat'+str(i)+'_name', 'code', _json_codelist['DistributionFormatCode'])
            version = _get_cell_value(wb, 'data_distformat'+str(i)+'_version')
            specification = _get_cell_value(wb, 'data_distformat'+str(i)+'_specification')
            if name:
                data_distformat = {'name': name, 'version': version, 'specification': specification}
                md_dict['data_distformats'].append(data_distformat)

        # data_uselimitations
        if not 'data_uselimitations' in md_dict: md_dict['data_uselimitations'] = []
        for i in range(1, 21):
            uselimitation = _get_cell_value(wb, 'data_uselimitation'+str(i))
            if uselimitation:
                md_dict['data_uselimitations'].append(uselimitation)
        
        # data_legal_uselimitations
        if not 'data_legal_uselimitations' in md_dict: md_dict['data_legal_uselimitations'] = []
        for i in range(1, 21):
            uselimitation = _get_cell_value(wb, 'data_legal_uselimitation'+str(i))
            if uselimitation:
                md_dict['data_legal_uselimitations'].append(uselimitation)
              
        # data_legal_useconstraints
        if not 'data_legal_useconstraints' in md_dict: md_dict['data_legal_useconstraints'] = []
        for i in range(1, 21):
            useconstraint = _get_cell_value(wb, 'data_legal_useconstraint'+str(i), 'code', _json_codelist['RestrictionCode'])
            if useconstraint:
                md_dict['data_legal_useconstraints'].append(useconstraint)
    
        # data_legal_accessconstraints
        if not 'data_legal_accessconstraints' in md_dict: md_dict['data_legal_accessconstraints'] = []
        for i in range(1, 21):
            accessconstraint = _get_cell_value(wb, 'data_legal_accessconstraint'+str(i), 'code', _json_codelist['RestrictionCode'])
            if accessconstraint:
                md_dict['data_legal_accessconstraints'].append(accessconstraint)
    
        # data_legal_otherconstraints
        if not 'data_legal_otherconstraints' in md_dict: md_dict['data_legal_otherconstraints'] = []
        for i in range(1, 21):
            otherconstraint = _get_cell_value(wb, 'data_legal_otherconstraint'+str(i), 'code', _json_codelist['InspireRestrictionCode'])
            if otherconstraint:
                md_dict['data_legal_otherconstraints'].append(otherconstraint)
    
        # data_security_uselimitations
        if not 'data_security_uselimitations' in md_dict: md_dict['data_security_uselimitations'] = []
        for i in range(1, 21):
            uselimitation = _get_cell_value(wb, 'data_security_uselimitation'+str(i))
            if uselimitation:
                md_dict['data_security_uselimitations'].append(uselimitation)
   
        # data_security_classification
        if _get_cell_value(wb, 'data_security_classification', 'code', _json_codelist['ClassificationCode']):
            md_dict['data_security_classification'] = _get_cell_value(wb, 'data_security_classification', 'code', _json_codelist['ClassificationCode'])
    
        # data_linkages
        if not 'data_linkages' in md_dict: md_dict['data_linkages'] = []
        for i in range(1, 21):
            name = _get_cell_value(wb, 'data_linkage'+str(i)+'_name')
            description = _get_cell_value(wb, 'data_linkage'+str(i)+'_description')
            url = _get_cell_value(wb, 'data_linkage'+str(i)+'_url')
            protocol = _get_cell_value(wb, 'data_linkage'+str(i)+'_protocol', 'code', _json_codelist['ProtocolCode'])
            if name:
                data_linkage = {'name': name, 'description': description, 'url': url, 'protocol': protocol}
                md_dict['data_linkages'].append(data_linkage)

        '''
        "data_dq_inspireconformities:specification": {
            "name": "data_dq_inspireconformity%_specification",
            "type": "string",
            "codelist": "",
            "many": "1"
        },
        "data_dq_inspireconformities:datecreation": {
            "name": "data_dq_inspireconformity%_datecreation",
            "type": "date",
            "codelist": "",
            "many": "1"
        },
        "data_dq_inspireconformities:datepublication": {
            "name": "data_dq_inspireconformity%_datepublication",
            "type": "date",
            "codelist": "",
            "many": "1"
        },
        "data_dq_inspireconformities:daterevision": {
            "name": "data_dq_inspireconformity%_daterevision",
            "type": "date",
            "codelist": "",
            "many": "1"
        },
        "data_dq_inspireconformities:explaination": {
            "name": "data_dq_inspireconformity%_explaination",
            "type": "string",
            "codelist": "",
            "many": "1"
        },
        "data_dq_inspireconformities:pass": {
            "name": "data_dq_inspireconformity%_pass",
            "type": "code",
            "codelist": "PassCode",
            "many": "1"
        }
        
        "data_dq_conformities:specification": {
            "name": "data_dq_inspireconformity%_specification",
            "type": "string",
            "codelist": "",
            "many": "1"
        },
        "data_dq_conformities:datecreation": {
            "name": "data_dq_inspireconformity%_datecreation",
            "type": "date",
            "codelist": "",
            "many": "1"
        },
        "data_dq_conformities:datepublication": {
            "name": "data_dq_inspireconformity%_datepublication",
            "type": "date",
            "codelist": "",
            "many": "1"
        },
        "data_dq_conformities:daterevision": {
            "name": "data_dq_inspireconformity%_daterevision",
            "type": "date",
            "codelist": "",
            "many": "1"
        },
        "data_dq_conformities:explaination": {
            "name": "data_dq_inspireconformity%_explaination",
            "type": "string",
            "codelist": "",
            "many": "1"
        },
        "data_dq_conformities:pass": {
            "name": "data_dq_inspireconformity%_pass",
            "type": "code",
            "codelist": "PassCode",
            "many": "1"
        }
        '''

        # server_ressources
        if _get_cell_value(wb, 'server_ressources'):
            md_dict['server_ressources'] = _get_cell_value(wb, 'server_ressources')
        # server_logos
        if _get_cell_value(wb, 'server_logos'):
            md_dict['server_logos'] = _get_cell_value(wb, 'server_logos')
            

        return md_dict
        
    else:
        return False

if __name__ == "__main__":        
    xlsx_file = 'xlsx/FR-341142131-ARAA_BDSol-Alsace_250000_2011.xlsx'
    print xlsx_to_dict(xlsx_file)