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
#from lxml import etree
import uuid
import copy
import codecs
import re

def _get_json(filename=None):
    extension = os.path.splitext(filename)[1]
    if os.path.isfile(filename) and extension == '.json':
        with open(filename) as file:
            return json.load(file)

# Get md_config.json
_root = os.path.dirname(__file__)
_json_config = _get_json(os.path.join(_root, "json/md_config.json"))


###########################################################################
# __DICT => XML
###########################################################################
def dict_to_xml(md_dict=None, filename=None, path_out='.'):
    """Convert data object to XML
    md_data: object data à convertir en XML
    xml_file: chemin et nom du fichier XML à sauvegarder. Si non défini ou erreur, aucu fichier n'est créé.
    retourne le XML issue de la conversion
    """            
    if md_dict is not None:

        _xml_doc = xml.dom.minidom.Document()
        # Root element
        root = _xml_doc.createElementNS(_json_config['xmlns'], 'gmd:MD_Metadata')
        for key, value in _json_config['namespaces'].items():
            root.setAttributeNS(_json_config['xmlns'], 'xmlns:'+key, value)
        #root.setAttributeNS(_json_config['namespaces']['gmd'], 'xmlns', _json_config['xmlns'])
        root.setAttributeNS(_json_config['namespaces']['xsi'], 'xsi:schemaLocation', _json_config['schemalocation'])
        _xml_doc.appendChild(root)

        # md_fileIdentifier
        md_fileidentifier = _check_value(md_dict, 'md_fileidentifier', str(uuid.uuid4()))
        fileIdentifier = _create_child_ns(_xml_doc, root, 'gmd', 'fileIdentifier')
        fileIdentifier_gco = _create_child_ns(_xml_doc, fileIdentifier, 'gco', 'CharacterString', md_fileidentifier)

        # md_language
        md_language = _check_value(md_dict, 'md_language', _json_config['default']['md_language'])
        language = _create_child_ns(_xml_doc, root, 'gmd', 'language')
        attr = {
            "codeList": "http://www.loc.gov/standards/iso639-2/",
            "codeListValue": md_language
        }
        LanguageCode = _create_child_ns(_xml_doc, language, 'gmd', 'LanguageCode', md_language, attr)

        # md_characterset
        md_characterset = _check_value(md_dict, 'md_characterset', _json_config['default']['md_characterset'])
        characterSet = _create_child_ns(_xml_doc, root, 'gmd', 'characterSet')
        attr = {
            "codeList": "http://www.isotc211.org/2005/resources/codeList.xml#MD_CharacterSetCode",
            "codeListValue": md_characterset
        }
        MD_CharacterSetCode = _create_child_ns(_xml_doc, characterSet, 'gmd', 'MD_CharacterSetCode', md_characterset, attr)

        # md_hierarchyLevel
        md_hierarchylevel = _check_value(md_dict, 'md_hierarchylevel', _json_config['default']['md_hierarchylevel'])
        hierarchyLevel = _create_child_ns(_xml_doc, root, 'gmd', 'hierarchyLevel')
        attr = {
            'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode',
            'codeListValue': md_hierarchylevel
        }
        MD_ScopeCode = _create_child_ns(_xml_doc, hierarchyLevel, 'gmd', 'MD_ScopeCode', md_hierarchylevel, attr)

        # md_contacts
        if _check_value(md_dict, 'md_contacts'):
            for md_contact in md_dict['md_contacts']:
                if _check_value(md_contact, 'organisation') and _check_value(md_contact, 'email'):
                    contact = _createContact(_xml_doc, root, md_contact, 'contact')
        #md_contacts = [_createContact(_xml_doc, root, md_contact, 'contact') for md_contact in md_dict['md_contacts'] if _check_value(md_dict, 'md_contacts') and _check_value(md_contact, 'organisation') and _check_value(md_contact, 'email')]

        # dateStamp
        date_today = str(datetime.date.today())
        md_datestamp = _check_value(md_dict, 'md_datestamp', date_today)
        dateStamp = _create_child_ns(_xml_doc, root, 'gmd', 'dateStamp')
        dateStamp_gco = _create_child_ns(_xml_doc, dateStamp, 'gco', 'Date', md_datestamp)

        # metadataStandardName
        md_standardname = _check_value(md_dict, 'md_standardname', _json_config['default']['md_standardname'])
        metadataStandardName = _create_child_ns(_xml_doc, root, 'gmd', 'metadataStandardName')
        metadataStandardName_gco = _create_child_ns(_xml_doc, metadataStandardName, 'gco', 'CharacterString', md_standardname)

        # metadataStandardVersion
        md_standardversion = _check_value(md_dict, 'md_standardversion', _json_config['default']['md_standardversion'])
        metadataStandardVersion = _create_child_ns(_xml_doc, root, 'gmd', 'metadataStandardVersion')
        metadataStandardVersion_gco = _create_child_ns(_xml_doc, metadataStandardVersion, 'gco', 'CharacterString', md_standardversion)

        # referenceSystemInfo
        if _check_value(md_dict, 'data_referencesystems'):
            for data_referencesystem in md_dict['data_referencesystems']:
                if _check_value(data_referencesystem, 'code') or _check_value(data_referencesystem, 'codespace'):
                    referenceSystemInfo = _create_child_ns(_xml_doc, root, 'gmd', 'referenceSystemInfo')
                    MD_ReferenceSystem = _create_child_ns(_xml_doc, referenceSystemInfo, 'gmd', 'MD_ReferenceSystem')
                    referenceSystemIdentifier = _create_child_ns(_xml_doc, MD_ReferenceSystem, 'gmd', 'referenceSystemIdentifier')
                    RS_Identifier = _create_child_ns(_xml_doc, referenceSystemIdentifier, 'gmd', 'RS_Identifier')
                    # referencesystem code
                    if _check_value(data_referencesystem, 'code'):
                        code = _create_child_ns(_xml_doc, RS_Identifier, 'gmd', 'code')
                        code_gco = _create_child_ns(_xml_doc, code, 'gco', 'CharacterString', data_referencesystem['code'])
                    # referencesystem codespace
                    if _check_value(data_referencesystem, 'codespace'):
                        codeSpace = _create_child_ns(_xml_doc, RS_Identifier, 'gmd', 'codeSpace')
                        code_gco = _create_child_ns(_xml_doc, codeSpace, 'gco', 'CharacterString', data_referencesystem['codespace'])

        # identificationInfo
        identificationInfo = _create_child_ns(_xml_doc, root, 'gmd', 'identificationInfo')
        dataIdentification = _create_child_ns(_xml_doc, identificationInfo, 'gmd', 'MD_DataIdentification')
        citation = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'citation')
        CI_Citation = _create_child_ns(_xml_doc, citation, 'gmd', 'CI_Citation')
        # data_title
        if _check_value(md_dict, 'data_title'):
            title = _create_child_ns(_xml_doc, CI_Citation, 'gmd', 'title')
            title_gco = _create_child_ns(_xml_doc, title, 'gco', 'CharacterString', md_dict['data_title'])
        else:
            print 'error: ', 'champ "titre" obligatoire.'
        # dates
        '''
        if _check_value(md_dict, 'data_datecreation'):
            _createDate(_xml_doc, CI_Citation, 'data_datecreation', 'creation')
        if _check_value(md_dict, 'data_daterevision'):

            _createDate(_xml_doc, CI_Citation, 'data_daterevision', 'revision')
        if _check_value(md_dict, 'data_datepublication'):
            _createDate(_xml_doc, CI_Citation, 'data_datepublication', 'publication')
        '''
        if _check_value(md_dict, 'data_dates'):
            for data_date in md_dict['data_dates']:
                if _check_value(data_date, 'date'):
                    _createDate(_xml_doc, CI_Citation, data_date['date'], data_date['type'])
        # presentationForm
        if _check_value(md_dict, 'data_presentationform'):
            presentationForm = _create_child_ns(_xml_doc, CI_Citation, 'gmd', 'presentationForm')
            attr = {
                'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_PresentationFormCode',
                'codeListValue':md_dict['data_presentationform']
            }
            CI_PresentationFormCode = _create_child_ns(_xml_doc, presentationForm, 'gmd', 'CI_PresentationFormCode', '', attr)

        # identifier
        if _check_value(md_dict, 'data_identifiers'):
            for data_identifier in md_dict['data_identifiers']:
                if _check_value(data_identifier, 'code'):
                    identifier = _create_child_ns(_xml_doc, CI_Citation, 'gmd', 'identifier')
                    RS_Identifier = _create_child_ns(_xml_doc, identifier, 'gmd', 'RS_Identifier')
                    # identifier code
                    code = _create_child_ns(_xml_doc, RS_Identifier, 'gmd', 'code')
                    code_gco = _create_child_ns(_xml_doc, code, 'gco', 'CharacterString', md_fileidentifier)
                    # identifier codespace
                    if _check_value(data_identifier, 'codespace'):
                        codeSpace = _create_child_ns(_xml_doc, RS_Identifier, 'gmd', 'codeSpace')
                        code_gco = _create_child_ns(_xml_doc, codeSpace, 'gco', 'CharacterString', '')

        # abstract
        if _check_value(md_dict, 'data_abstract'):
            abstract = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'abstract')
            abstract_gco = _create_child_ns(_xml_doc, abstract, 'gco', 'CharacterString', md_dict['data_abstract'])

        # data_contacts
        if _check_value(md_dict, 'data_contacts'):
            for data_contact in md_dict['data_contacts']:
                if _check_value(data_contact, 'organisation') and _check_value(data_contact, 'email'):
                    contact = _createContact(_xml_doc, dataIdentification, data_contact, 'pointOfContact')
        #data_contacts = [_createContact(_xml_doc, dataIdentification, data_contact, 'pointOfContact') for data_contact in md_dict['data_contacts'] if _check_value(md_dict, 'data_contacts')]

        # resourceMaintenance
        if _check_value(md_dict, 'data_maintenancefrequencycode'):
            resourceMaintenance = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'resourceMaintenance')
            MD_MaintenanceInformation = _create_child_ns(_xml_doc, resourceMaintenance, 'gmd', 'MD_MaintenanceInformation')
            maintenanceAndUpdateFrequency = _create_child_ns(_xml_doc, MD_MaintenanceInformation, 'gmd', 'maintenanceAndUpdateFrequency')
            attr = {
                'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_MaintenanceFrequencyCode',
                'codeListValue':md_dict['data_maintenancefrequencycode']
            }
            MD_MaintenanceFrequencyCode = _create_child_ns(_xml_doc, maintenanceAndUpdateFrequency, 'gmd', 'MD_MaintenanceFrequencyCode', attr['codeListValue'], attr)

        # graphicOverview
        if _check_value(md_dict, 'data_browsegraphics'):
            for data_browsegraphic in md_dict['data_browsegraphics']:
                if _check_value(data_browsegraphic, 'url'):
                    graphicOverview = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'graphicOverview')
                    MD_BrowseGraphic = _create_child_ns(_xml_doc, graphicOverview, 'gmd', 'MD_BrowseGraphic')
                    # url
                    fileName = _create_child_ns(_xml_doc, MD_BrowseGraphic, 'gmd', 'fileName')
                    fileName_gco = _create_child_ns(_xml_doc, fileName, 'gco', 'CharacterString', data_browsegraphic['url'])
                    # description
                    fileDescription = _create_child_ns(_xml_doc, graphicOverview, 'gmd', 'fileDescription')
                    fileDescription_gco = _create_child_ns(_xml_doc, fileDescription, 'gco', 'CharacterString', data_browsegraphic['description'])
                    # type
                    fileType = _create_child_ns(_xml_doc, graphicOverview, 'gmd', 'fileType')
                    fileType_gco = _create_child_ns(_xml_doc, fileType, 'gco', 'CharacterString', data_browsegraphic['type'])

        # data_keywords
        #data_keywords = [_createKeyword(_xml_doc, dataIdentification, data_keyword) for data_keyword in md_dict['data_keywords'] if _check_value(md_dict, 'data_keywords') and _check_value(data_keyword, 'keyword')]
        if _check_value(md_dict, 'data_keywords'):
            for data_keyword in md_dict['data_keywords']:
                if _check_value(data_keyword, 'keyword'):
                    keywords = _createKeyword(_xml_doc, dataIdentification, data_keyword)

        # data_inspirekeywords
        #keywords = [_createKeyword(_xml_doc, dataIdentification, data_inspirekeyword) for data_inspirekeyword in md_dict['data_inspirekeywords'] if _check_value(md_dict, 'data_inspirekeywords') and _check_value(data_inspirekeyword, 'keyword')]
        if _check_value(md_dict, 'data_inspirekeywords'):
            for data_inspirekeyword in md_dict['data_inspirekeywords']:
                if _check_value(data_inspirekeyword, 'keyword'):
                    keywords = _createKeyword(_xml_doc, dataIdentification, data_inspirekeyword)
        
        # resourceConstraints: le principe retenu ici est d'utiliser 1 <resourceConstraints> pour chaque type de contrainte: <MD_Constraints>, <MD_LegalConstraints> et <MD_SecurityConstraints>
        
        # MD_Constraints - useLimitation
        if _check_value(md_dict, 'data_uselimitations'):
            resourceConstraints = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'resourceConstraints')
            MD_Constraints = _create_child_ns(_xml_doc, resourceConstraints, 'gmd', 'MD_Constraints')
            for data_uselimitation in md_dict['data_uselimitations']:
                uselimitation = _createUseLimitation(_xml_doc, MD_Constraints, data_uselimitation)

        # MD_LegalConstraints
        if any([_check_value(md_dict, 'data_legal_uselimitations'), _check_value(md_dict, 'data_legal_useconstraints'), _check_value(md_dict, 'data_legal_accessconstraints'), _check_value(md_dict, 'data_legal_otherconstraints')]):
            resourceConstraints_legal = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'resourceConstraints')
            MD_LegalConstraints = _create_child_ns(_xml_doc, resourceConstraints_legal, 'gmd', 'MD_LegalConstraints')
            # MD_LegalConstraints - useLimitations
            if _check_value(md_dict, 'data_legal_uselimitations'):
                for data_legal_uselimitation in md_dict['data_legal_uselimitations']:
                    legal_uselimitation = _createUseLimitation(_xml_doc, MD_LegalConstraints, data_legal_uselimitation)
            # MD_LegalConstraints - useConstraints
            if _check_value(md_dict, 'data_legal_useconstraints'):
                for data_legal_useconstraint in md_dict['data_legal_useconstraints']:
                    if data_legal_useconstraint:
                        useConstraints = _create_child_ns(_xml_doc, MD_LegalConstraints, 'gmd', 'useConstraints')
                        attr = {
                            'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode',
                            'codeListValue': data_legal_useconstraint
                        }
                        MD_RestrictionCode = _create_child_ns(_xml_doc, useConstraints, 'gmd', 'MD_RestrictionCode', attr['codeListValue'], attr)
            # MD_LegalConstraints - accessConstraints
            if _check_value(md_dict, 'data_legal_accessconstraints'):
                for data_legal_accessconstraint in md_dict['data_legal_accessconstraints']:
                    if data_legal_accessconstraint:
                        accessConstraints = _create_child_ns(_xml_doc, MD_LegalConstraints, 'gmd', 'accessConstraints')
                        attr = {
                            'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode',
                            'codeListValue': data_legal_accessconstraint
                        }
                        MD_RestrictionCode = _create_child_ns(_xml_doc, accessConstraints, 'gmd', 'MD_RestrictionCode', attr['codeListValue'], attr)
            # MD_LegalConstraints - otherConstraints
            if _check_value(md_dict, 'data_legal_otherconstraints'):
                for data_legal_otherconstraint in md_dict['data_legal_otherconstraints']:
                    if data_legal_otherconstraint:
                        otherConstraints = _create_child_ns(_xml_doc, MD_LegalConstraints, 'gmd', 'otherConstraints')
                        otherConstraints_gco = _create_child_ns(_xml_doc, otherConstraints, 'gco', 'CharacterString', data_legal_otherconstraint)

        # MD_SecurityConstraints
        if any([_check_value(md_dict, 'data_security_uselimitations'), _check_value(md_dict, 'data_security_classification')]):
            resourceConstraints_security = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'resourceConstraints')
            MD_SecurityConstraints = _create_child_ns(_xml_doc, resourceConstraints_security, 'gmd', 'MD_SecurityConstraints')
            # MD_SecurityConstraints - useLimitation
            if _check_value(md_dict, 'data_security_uselimitations'):
                for data_security_uselimitation in md_dict['data_security_uselimitations']:
                    security_uselimitation = _createUseLimitation(_xml_doc, MD_SecurityConstraints, data_security_uselimitation)
            # MD_SecurityConstraints - classification
            data_security_classification = _check_value(md_dict, 'data_security_classification', _json_config['default']['data_security_classification'])
            classification = _create_child_ns(_xml_doc, MD_SecurityConstraints, 'gmd', 'classification')
            attr = {
                'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ClassificationCode',
                'codeListValue': data_security_classification
            }
            MD_ClassificationCode = _create_child_ns(_xml_doc, classification, 'gmd', 'MD_ClassificationCode', attr['codeListValue'], attr)

        # spatialRepresentationType
        if _check_value(md_dict, 'data_spatialrepresentationtype'):
            spatialRepresentationType = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'spatialRepresentationType')
            attr = {
                'codeList': 'http://www.isotc211.org/2005/resources/codeList.xml#MD_SpatialRepresentationTypeCode',
                'codeListValue':md_dict['data_spatialrepresentationtype']
            }
            MD_SpatialRepresentationTypeCode = _create_child_ns(_xml_doc, spatialRepresentationType, 'gmd', 'MD_SpatialRepresentationTypeCode', attr['codeListValue'], attr)

        # spatialResolution: pour complémeter l'implémentation...
        if _check_value(md_dict, 'data_scaledenominator') or _check_value(md_dict, 'data_scaledistance'):
            spatialResolution = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'spatialResolution')
            MD_Resolution = _create_child_ns(_xml_doc, spatialResolution, 'gmd', 'MD_Resolution')
            if _check_value(md_dict, 'data_scaledenominator'):
                equivalentScale = _create_child_ns(_xml_doc, MD_Resolution, 'gmd', 'equivalentScale')
                MD_RepresentativeFraction = _create_child_ns(_xml_doc, equivalentScale, 'gmd', 'MD_RepresentativeFraction')
                denominator = _create_child_ns(_xml_doc, MD_RepresentativeFraction, 'gmd', 'denominator')
                denominator_gco = _create_child_ns(_xml_doc, denominator, 'gco', 'Integer', md_dict['data_scaledenominator'])
            if _check_value(md_dict, 'data_scaledistance'):
                distance = _create_child_ns(_xml_doc, MD_Resolution, 'gmd', 'distance')
                attr = {
                    'codeList': 'http://standards.iso.org/ittf/PublicityAvailableStandards/ISO_19139_Schemas/resources.uom/ML_gmxUom.xml#m',
                    'codeListValue':md_dict['data_scaledistance']
                }
                distance_gco = _create_child_ns(_xml_doc, distance, 'gco', 'CharacterString', attr['codeListValue'], attr)

        # language
        data_languages = _check_value(md_dict, 'data_languages', _json_config['default']['data_languages'])
        for data_language in data_languages:
            if data_language: # Au cas où la valeur par défaut serait définie à "".
                language = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'language')
                attr = {
                    'codeList': 'http://www.loc.gov/standards/iso639-2/',
                    'codeListValue': data_language
                }
                LanguageCode = _create_child_ns(_xml_doc, language, 'gmd', 'LanguageCode', attr['codeListValue'], attr)

        # characterSet
        data_characterset = _check_value(md_dict, 'data_characterset', _json_config['default']['data_characterset'])
        characterSet = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'characterSet')
        attr = {
            'codeList': 'http://www.isotc211.org/2005/resources/codeList.xml#MD_CharacterSetCode',
            'codeListValue': data_characterset
        }
        MD_CharacterSetCode = _create_child_ns(_xml_doc, characterSet, 'gmd', 'MD_CharacterSetCode', attr['codeListValue'], attr)
        # topicCategory
        if _check_value(md_dict, 'data_topiccategories'):
            for data_topiccategory in md_dict['data_topiccategories']:
                topicCategory = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'topicCategory')
                MD_TopicCategoryCode = _create_child_ns(_xml_doc, topicCategory, 'gmd', 'MD_TopicCategoryCode', data_topiccategory)

        # extend - geo
        if _check_value(md_dict, 'data_geographicextents'):
            for data_geographicextent in md_dict['data_geographicextents']:
                if _check_value(data_geographicextent, 'xmin') and _check_value(data_geographicextent, 'xmax') and _check_value(data_geographicextent, 'ymin') and _check_value(data_geographicextent, 'ymax'):
                    extent_geo = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'extent')
                    EX_Extent_geo = _create_child_ns(_xml_doc, extent_geo, 'gmd', 'EX_Extent')
                    if _check_value(data_geographicextent, 'name'):
                        description_geo = _create_child_ns(_xml_doc, EX_Extent_geo, 'gmd', 'description')
                        description_geo_gco = _create_child_ns(_xml_doc, description_geo, 'gco', 'CharacterString', data_geographicextent['name'])
                    geographicElement = _create_child_ns(_xml_doc, EX_Extent_geo, 'gmd', 'geographicElement')
                    EX_GeographicBoundingBox = _create_child_ns(_xml_doc, geographicElement, 'gmd', 'EX_GeographicBoundingBox')
                    westBoundLongitude = _create_child_ns(_xml_doc, EX_GeographicBoundingBox, 'gmd', 'westBoundLongitude')
                    westBoundLongitude_gco = _create_child_ns(_xml_doc, westBoundLongitude, 'gco', 'Decimal', data_geographicextent['xmin'])
                    eastBoundLongitude = _create_child_ns(_xml_doc, EX_GeographicBoundingBox, 'gmd', 'eastBoundLongitude')
                    eastBoundLongitude_gco = _create_child_ns(_xml_doc, eastBoundLongitude, 'gco', 'Decimal', data_geographicextent['xmax'])
                    southBoundLatitude = _create_child_ns(_xml_doc, EX_GeographicBoundingBox, 'gmd', 'southBoundLatitude')
                    southBoundLatitude_gco = _create_child_ns(_xml_doc, southBoundLatitude, 'gco', 'Decimal', data_geographicextent['ymin'])
                    northBoundLatitude = _create_child_ns(_xml_doc, EX_GeographicBoundingBox, 'gmd', 'northBoundLatitude')
                    northBoundLatitude_gco = _create_child_ns(_xml_doc, northBoundLatitude, 'gco', 'Decimal', data_geographicextent['ymax'])

        # extend - temporal
        if _check_value(md_dict, 'data_temporalextents'):
            for data_temporalextent in md_dict['data_temporalextents']:
                if _check_value(data_temporalextent, 'start'):
                    extent_temp = _create_child_ns(_xml_doc, dataIdentification, 'gmd', 'extent')
                    EX_Extent_temp = _create_child_ns(_xml_doc, extent_temp, 'gmd', 'EX_Extent')
                    if _check_value(data_temporalextent, 'name'):
                        description_temp = _create_child_ns(_xml_doc, EX_Extent_temp, 'gmd', 'description')
                        description_temp_gco = _create_child_ns(_xml_doc, description_temp, 'gco', 'CharacterString', data_temporalextent['description'])
                    temporalElement = _create_child_ns(_xml_doc, EX_Extent_temp, 'gmd', 'temporalElement')
                    EX_TemporalExtent = _create_child_ns(_xml_doc, temporalElement, 'gmd', 'EX_TemporalExtent')
                    extent = _create_child_ns(_xml_doc, EX_TemporalExtent, 'gmd', 'extent')
                    TimePeriod = _create_child_ns(_xml_doc, extent, 'gml', 'gml:TimePeriod')
                    #TimePeriod.setAttributeNS(_json_config['namespaces']['xsi'], 'type', 'gml:TimePeriodType')
                    beginPosition = _create_child_ns(_xml_doc, TimePeriod, 'gml', 'gml:beginPosition', data_temporalextent['start'])
                    endPosition = _create_child_ns(_xml_doc, TimePeriod, 'gml', 'gml:endPosition', data_temporalextent['end'])

        # distributionInfo
        if _check_value(md_dict, 'data_distformats') or _check_value(md_dict, 'data_linkages'):
            distributionInfo = _create_child_ns(_xml_doc, root, 'gmd', 'distributionInfo')
            MD_Distribution = _create_child_ns(_xml_doc, distributionInfo, 'gmd', 'MD_Distribution')
            # distributionFormat
            for data_distformat in md_dict['data_distformats']:
                if _check_value(data_distformat, 'name'):
                    distributionFormat = _create_child_ns(_xml_doc, MD_Distribution, 'gmd', 'distributionFormat')
                    MD_Format = _create_child_ns(_xml_doc, distributionFormat, 'gmd', 'MD_Format')
                    # name
                    distributionFormat_name = _create_child_ns(_xml_doc, MD_Format, 'gmd', 'name')
                    distributionFormat_name_gco = _create_child_ns(_xml_doc, distributionFormat_name, 'gco', 'CharacterString', data_distformat['name'])
                    # version
                    if _check_value(data_distformat, 'version'):
                        distributionFormat_version = _create_child_ns(_xml_doc, MD_Format, 'gmd', 'version')
                        distributionFormat_version_gco = _create_child_ns(_xml_doc, distributionFormat_version, 'gco', 'CharacterString', data_distformat['version'])
                    # specification
                    if _check_value(data_distformat, 'specification'):
                        distributionFormat_specification = _create_child_ns(_xml_doc, MD_Format, 'gmd', 'specification')
                        distributionFormat_specification_gco = _create_child_ns(_xml_doc, distributionFormat_specification, 'gco', 'CharacterString', data_distformat['specification'])

            # transferOptions
            if _check_value(md_dict, 'data_linkages'):
                transferOptions = _create_child_ns(_xml_doc, MD_Distribution, 'gmd', 'transferOptions')
                MD_DigitalTransferOptions = _create_child_ns(_xml_doc, transferOptions, 'gmd', 'MD_DigitalTransferOptions')
                for data_linkage in md_dict['data_linkages']:
                    if _check_value(data_linkage, 'name'):
                        onLine = _create_child_ns(_xml_doc, MD_DigitalTransferOptions, 'gmd', 'onLine')
                        CI_OnlineResource = _create_child_ns(_xml_doc, onLine, 'gmd', 'CI_OnlineResource')
                        # linkage
                        if _check_value(data_linkage, 'url'):
                            linkage = _create_child_ns(_xml_doc, CI_OnlineResource, 'gmd', 'linkage')
                            URL = _create_child_ns(_xml_doc, linkage, 'gmd', 'URL', data_linkage['url'])
                        # protocol
                        if _check_value(data_linkage, 'protocol'):
                            protocol = _create_child_ns(_xml_doc, CI_OnlineResource, 'gmd', 'protocol')
                            protocol_gco = _create_child_ns(_xml_doc, protocol, 'gco', 'CharacterString', data_linkage['protocol'])
                        # name
                        name = _create_child_ns(_xml_doc, CI_OnlineResource, 'gmd', 'name')
                        name_gco = _create_child_ns(_xml_doc, name, 'gco', 'CharacterString', data_linkage['name'])
                        # description
                        if _check_value(data_linkage, 'description'):
                            description = _create_child_ns(_xml_doc, CI_OnlineResource, 'gmd', 'description')
                            description_gco = _create_child_ns(_xml_doc, description, 'gco', 'CharacterString', data_linkage['description'])

        # data_li_statement
        if _check_value(md_dict, 'data_linkages'):
            dataQualityInfo = _create_child_ns(_xml_doc, root, 'gmd', 'dataQualityInfo')
            DQ_DataQuality = _create_child_ns(_xml_doc, dataQualityInfo, 'gmd', 'DQ_DataQuality')
            # scope - level
            scope = _create_child_ns(_xml_doc, DQ_DataQuality, 'gmd', 'scope')
            DQ_Scope = _create_child_ns(_xml_doc, scope, 'gmd', 'DQ_Scope')
            level = _create_child_ns(_xml_doc, DQ_Scope, 'gmd', 'level')
            data_dq_level = _check_value(md_dict, 'data_dq_level', _json_config['default']['md_hierarchylevel'])
            attr = {
                'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode',
                'codeListValue': data_dq_level
            }
            MD_ScopeCode = _create_child_ns(_xml_doc, level, 'gmd', 'MD_ScopeCode', attr['codeListValue'], attr)
            # lineage
            lineage = _create_child_ns(_xml_doc, DQ_DataQuality, 'gmd', 'lineage')
            LI_Lineage = _create_child_ns(_xml_doc, lineage, 'gmd', 'LI_Lineage')
            statement = _create_child_ns(_xml_doc, LI_Lineage, 'gmd', 'statement')
            data_li_statement = _check_value(md_dict, 'data_li_statement')
            statement_gco = _create_child_ns(_xml_doc, statement, 'gco', 'CharacterString', data_li_statement)

        #md_xml = ''
        md_xml = _xml_doc.toprettyxml(indent="\t", encoding="UTF-8")
        #md_xml = _xml_doc.toxml("ISO-8859-1")
        #.decode("utf-8")
        
        if filename is None: filename = md_fileidentifier+'.xml'
        filename = os.path.join(path_out, filename)
        #_save_xml(_xml_doc, filename)
        #_xml_doc.writexml(codecs.open(filename,'w','utf-8'), encoding='UTF-8')
        with open(filename, "w") as f:
            #_xml_doc.writexml(f, encoding="utf-8")
            f.write(md_xml)
        
        return md_xml
    else:
        md_xml = False
    return md_xml
        
        
def _create_child_ns(_xml_doc=None, parent=None, prefix=None, balise=None, text=None, attributes={}):
    """Create child tree element"""
    element = None
    if parent and balise:
        if _json_config['namespaces'] and prefix:
            element = _xml_doc.createElementNS(_json_config['namespaces'][prefix], ':'.join((prefix, balise)))
        else:
            element = _xml_doc.createElement(balise)
        if text:
            #print text
            if isinstance(text, basestring): text = text.encode('utf-8')
            txt = _xml_doc.createTextNode(str(text).decode('utf-8'))
            element.appendChild(txt)
        if attributes:
            for key, value in attributes.items():
                element.setAttributeNS(_json_config['namespaces'][prefix], key, value)
        parent.appendChild(element)
    return element

def _check_value(dictionary={}, key=None, default=None):
    """Chek if data object exists and assign default value if necessary"""
    if dictionary and key in dictionary:
        if dictionary[key]:
            if isinstance(dictionary[key], basestring):
                return dictionary[key]
            elif isinstance(dictionary[key], int) or isinstance(dictionary[key], float):
                return str(dictionary[key])
            elif isinstance(dictionary[key], list):
                items = [item for item in dictionary[key] if item]
                if items:
                    return items
            else:
                return str(dictionary[key])
    return default

def _createContact(_xml_doc=None, parent = None, cnt_data = {}, cnt_balise=None):
    if parent and cnt_data and cnt_balise:
        contact = _create_child_ns(_xml_doc, parent, 'gmd', cnt_balise)
        CI_ResponsibleParty = _create_child_ns(_xml_doc, contact, 'gmd', 'CI_ResponsibleParty')
        # individualName
        if _check_value(cnt_data, 'name'):
            individualName = _create_child_ns(_xml_doc, CI_ResponsibleParty, 'gmd', 'individualName')
            individualName_gco = _create_child_ns(_xml_doc, individualName, 'gco', 'CharacterString', cnt_data['name'])
        # organisationName
        if _check_value(cnt_data, 'organisation'):
            organisationName = _create_child_ns(_xml_doc, CI_ResponsibleParty, 'gmd', 'organisationName')
            organisationName_gco = _create_child_ns(_xml_doc, organisationName, 'gco', 'CharacterString', cnt_data['organisation'])
        # positionName
        if _check_value(cnt_data, 'position'):
            positionName = _create_child_ns(_xml_doc, CI_ResponsibleParty, 'gmd', 'positionName')
            positionName_gco = _create_child_ns(_xml_doc, positionName, 'gco', 'CharacterString', cnt_data['position'])
        # contactInfo
        if _check_value(cnt_data, 'tel') or _check_value(cnt_data, 'address') or _check_value(cnt_data, 'city') or _check_value(cnt_data, 'email') or _check_value(cnt_data, 'logo_url'):
            contactInfo = _create_child_ns(_xml_doc, CI_ResponsibleParty, 'gmd', 'contactInfo')
            CI_Contact = _create_child_ns(_xml_doc, contactInfo, 'gmd', 'CI_Contact')
            # phone
            if _check_value(cnt_data, 'tel'):
                phone = _create_child_ns(_xml_doc, CI_Contact, 'gmd', 'phone')
                CI_Telephone = _create_child_ns(_xml_doc, phone, 'gmd', 'CI_Telephone')
                voice = _create_child_ns(_xml_doc, CI_Telephone, 'gmd', 'voice')
                voice_gco = _create_child_ns(_xml_doc, voice, 'gco', 'CharacterString', cnt_data['tel'])
            # address
            if _check_value(cnt_data, 'city') or _check_value(cnt_data, 'email'):
                if _check_value(cnt_data, 'city'):
                    address = _create_child_ns(_xml_doc, CI_Contact, 'gmd', 'address')
                    CI_Address = _create_child_ns(_xml_doc, address, 'gmd', 'CI_Address')
                    # deliveryPoint
                    if _check_value(cnt_data, 'address'):
                        deliveryPoint = _create_child_ns(_xml_doc, CI_Address, 'gmd', 'deliveryPoint')
                        deliveryPoint_gco = _create_child_ns(_xml_doc, deliveryPoint, 'gco', 'CharacterString', cnt_data['address'])
                    # city
                    if _check_value(cnt_data, 'city'):
                        city = _create_child_ns(_xml_doc, CI_Address, 'gmd', 'city')
                        city_gco = _create_child_ns(_xml_doc, city, 'gco', 'CharacterString', cnt_data['city'])
                    # postalCode
                    if _check_value(cnt_data, 'cp'):
                        postalCode = _create_child_ns(_xml_doc, CI_Address, 'gmd', 'postalCode')
                        postalCode_gco = _create_child_ns(_xml_doc, postalCode, 'gco', 'CharacterString', cnt_data['cp'])
                if _check_value(cnt_data, 'email'):
                    # electronicMailAddress
                    electronicMailAddress = _create_child_ns(_xml_doc, CI_Address, 'gmd', 'electronicMailAddress')
                    electronicMailAddress_gco = _create_child_ns(_xml_doc, electronicMailAddress, 'gco', 'CharacterString', cnt_data['email'])
            # contactInstructions - logo
            if _check_value(cnt_data, 'logo_url'):
                contactInstructions = _create_child_ns(_xml_doc, CI_Contact, 'gmd', 'contactInstructions')
                attr = {
                    'src': cnt_data['logo_url']
                }
                FileName = _create_child_ns(_xml_doc, contactInstructions, 'gmx', 'FileName', 'logo', attr)
        # cnt_role
        cnt_role = _check_value(cnt_data, 'role', _json_config['default']['cnt_role'])
        role = _create_child_ns(_xml_doc, CI_ResponsibleParty, 'gmd', 'role')
        attr = {
            'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode',
            'codeListValue': cnt_role,
        }
        CI_RoleCode = _create_child_ns(_xml_doc, role, 'gmd', 'CI_RoleCode', cnt_role, attr)
        return contact
    else:
        return False

def _createKeyword(_xml_doc=None, parent=None, keywords={}):
    if parent and keywords:
        # descriptiveKeywords
        descriptiveKeywords = _create_child_ns(_xml_doc, parent, 'gmd', 'descriptiveKeywords')
        MD_Keywords = _create_child_ns(_xml_doc, descriptiveKeywords, 'gmd', 'MD_Keywords')
        # keyword
        keyword = _create_child_ns(_xml_doc, MD_Keywords, 'gmd', 'keyword')
        keyword_gco = _create_child_ns(_xml_doc, keyword, 'gco', 'CharacterString', keywords['keyword'])
        # type
        if _check_value(keywords, 'type'):
            type = _create_child_ns(_xml_doc, MD_Keywords, 'gmd', 'type')
            attr = {
                'codeList': 'http://www.isotc211.org/2005/resources/codeList.xml#MD_KeywordTypeCode',
                'codeListValue': keywords['type']
            }
            MD_KeywordTypeCode = _create_child_ns(_xml_doc, type, 'gmd', 'MD_KeywordTypeCode', keywords['type'], attr)
        # thesaurus name
        if _check_value(keywords, 'thesaurus_name'):
            thesaurusName = _create_child_ns(_xml_doc, MD_Keywords, 'gmd', 'thesaurusName')
            CI_Citation = _create_child_ns(_xml_doc, thesaurusName, 'gmd', 'CI_Citation')
            title = _create_child_ns(_xml_doc, CI_Citation, 'gmd', 'title')
            title_gco = _create_child_ns(_xml_doc, title, 'gco', 'CharacterString', keywords['thesaurus_name'])
            # dates
            '''
            if _check_value(keywords, 'thesaurus_datecreation'):
                _createDate(_xml_doc, CI_Citation, keywords['data_datecreation'], 'creation')

            if _check_value(keywords, 'thesaurus_daterevision'):
                _createDate(_xml_doc, CI_Citation, keywords['data_daterevision'], 'revision')
            if _check_value(keywords, 'thesaurus_datepublication'):
                _createDate(_xml_doc, CI_Citation, keywords['data_datepublication'], 'publication')
            '''
            if _check_value(keywords, 'thesaurus_dates'):
                for thesaurus_date in keywords['thesaurus_dates']:
                    if _check_value(thesaurus_date, 'date'):
                        _createDate(_xml_doc, CI_Citation, thesaurus_date['date'], thesaurus_date['type'])
    else:
        return False

def _createUseLimitation(_xml_doc=None, parent=None, uselimitation=None):
    if parent and uselimitation:
        useLimitation = _create_child_ns(_xml_doc, parent, 'gmd', 'useLimitation')
        useLimitation_gco = _create_child_ns(_xml_doc, useLimitation, 'gco', 'CharacterString', uselimitation)
    else:
        return False

def _createDate(_xml_doc=None, parent=None, date_value=None, date_type=None):
    if parent and date_value and date_type:
        date = _create_child_ns(_xml_doc, parent, 'gmd', 'date')
        CI_Date = _create_child_ns(_xml_doc, date, 'gmd', 'CI_Date')
        # date value
        date_val = _create_child_ns(_xml_doc, CI_Date, 'gmd', 'date')
        date_val_gco = _create_child_ns(_xml_doc, date_val, 'gco', 'Date', date_value)
        # dateType
        dateType = _create_child_ns(_xml_doc, CI_Date, 'gmd', 'dateType')
        attr = {
            'codeList': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode',
            'codeListValue': date_type
        }
        CI_DateTypeCode = _create_child_ns(_xml_doc, dateType, 'gmd', 'CI_DateTypeCode', attr['codeListValue'], attr)
    else:
        return False

'''        
def _save_xml(_xml_doc=None, filename=None):
    """Save XML result to file"""
    if filename and _xml_doc:
        #_xml_doc.writexml(codecs.open(filename,'w','utf-8'), encoding='UTF-8')
        with open(filename, "w") as f:
            #_xml_doc.writexml(f, encoding="utf-8")
            f.write(xmldoc.toxml("utf-8").decode("utf-8"))
'''    

        
if __name__ == "__main__":
    md_dict = _get_json(os.path.join(_root, "json/md_data.json"))       
    dict_to_xml(md_dict, 'xml/test.xml')

