var xpaths = {
    // Metadata
    Root: 'gmd\\:MD_Metadata, MD_Metadata',
    MD_FileIdentifier: 'gmd\\:MD_Metadata>gmd\\:fileIdentifier>gco\\:CharacterString, MD_Metadata>fileIdentifier>CharacterString',
    MD_Language: 'gmd\\:MD_Metadata>gmd\\:language>gmd\\:LanguageCode, MD_Metadata>language>LanguageCode',
    MD_CharacterSet: 'gmd\\:MD_Metadata>gmd\\:characterSet>gmd\\:MD_CharacterSetCode, MD_Metadata>characterSet>MD_CharacterSetCode',
    MD_HierarchyLevel: 'gmd\\:MD_Metadata>gmd\\:hierarchyLevel>gmd\\:MD_ScopeCode, MD_Metadata>hierarchyLevel>MD_ScopeCode',
    // MD_Contacts = tableau d'objets contact
    MD_Contacts: 'gmd\\:MD_Metadata>gmd\\:contact>gmd\\:CI_ResponsibleParty, MD_Metadata>contact>CI_ResponsibleParty',
    MD_DateStamp: 'gmd\\:MD_Metadata>gmd\\:dateStamp>gco\\:Date, MD_Metadata>dateStamp>Date',
    MD_StandardName: 'gmd\\:MD_Metadata>gmd\\:metadataStandardName>gco\\:CharacterString, MD_Metadata>metadataStandardName>CharacterString',
    MD_StandardVersion: 'gmd\\:MD_Metadata>gmd\\:metadataStandardVersion>gco\\:CharacterString, MD_Metadata>metadataStandardVersion>CharacterString',
    // Data
    Data_Title: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:citation>gmd\\:CI_Citation>gmd\\:title>gco\\:CharacterString, MD_Metadata>identificationInfo>MD_DataIdentification>citation>CI_Citation>title>CharacterString',
    Service_Title: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:citation>gmd\\:CI_Citation>gmd\\:title>gco\\:CharacterString, MD_Metadata>identificationInfo>SV_ServiceIdentification>citation>CI_Citation>title>CharacterString',
    Data_ReferenceSystems: 'gmd\\:MD_Metadata>gmd\\:referenceSystemInfo>gmd\\:MD_ReferenceSystem, MD_Metadata>referenceSystemInfo>MD_ReferenceSystem',
    Data_ReferenceSystemCode: 'gmd\\:referenceSystemIdentifier>gmd\\:RS_Identifier>gmd\\:code>gco\\:CharacterString, referenceSystemIdentifier>RS_Identifier>code>CharacterString',
    // Dates
    Data_Dates: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:citation>gmd\\:CI_Citation>gmd\\:date>gmd\\:CI_Date, MD_Metadata>identificationInfo>MD_DataIdentification>citation>CI_Citation>date>CI_Date',
    Service_Dates: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:citation>gmd\\:CI_Citation>gmd\\:date>gmd\\:CI_Date, MD_Metadata>identificationInfo>SV_ServiceIdentification>citation>CI_Citation>date>CI_Date',
    Date: 'gmd\\:date>gco\\:Date, date>Date',
    DateType: 'gmd\\:dateType>gmd\\:CI_DateTypeCode, dateType>CI_DateTypeCode',
    // Identifiers
    Data_Identifiers: 'gmd\\:identifier>gmd\\:RS_Identifier, identifier>RS_Identifier',
    Data_Code: 'gmd\\:code>gco\\:CharacterString, code>CharacterString',
    Data_CodeSpace: 'gmd\\:codeSpace>gco\\:CharacterString, codeSpace>CharacterString',
    Data_Abstract: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:abstract>gco\\:CharacterString, MD_Metadata>identificationInfo>MD_DataIdentification>abstract>CharacterString',
    Service_Abstract: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:abstract>gco\\:CharacterString, MD_Metadata>identificationInfo>SV_ServiceIdentification>abstract>CharacterString',
    // Contacts: tableau d'objets
    Data_PointOfContacts: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:pointOfContact>gmd\\:CI_ResponsibleParty, MD_Metadata>identificationInfo>MD_DataIdentification>pointOfContact>CI_ResponsibleParty',
    Service_PointOfContacts: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:pointOfContact>gmd\\:CI_ResponsibleParty, MD_Metadata>identificationInfo>SV_ServiceIdentification>pointOfContact>CI_ResponsibleParty',
    // Browsegraphic
    Data_BrowseGraphics: 'gmd\\:graphicOverview>gmd\\:MD_BrowseGraphic, graphicOverview>MD_BrowseGraphic',
    Data_BrowseGraphic_Name: 'gmd\\:fileName>gco\\:CharacterString, fileName>CharacterString',
    Data_BrowseGraphic_Description: 'gmd\\:fileDescription>gco\\:CharacterString, fileDescription>CharacterString',
    Data_BrowseGraphic_Type: 'gmd\\:fileType>gco\\:CharacterString, fileType>CharacterString',
    // Keywords
    Data_Keywords: 'gmd\\:descriptiveKeywords>gmd\\:MD_Keywords, descriptiveKeywords>MD_Keywords',
    Data_Keyword: 'gmd\\:keyword>gco\\:CharacterString, keyword>CharacterString',
    Data_KeywordType: 'gmd\\:type>gmd\\:MD_KeywordTypeCode, type>MD_KeywordTypeCode',
    Data_Thesaurus: '',
    Data_ThesaurusName: 'gmd\\:thesaurusName>gmd\\:CI_Citation>gmd\\:title>gco\\:CharacterString, thesaurusName>CI_Citation>title>CharacterString',
    Data_ThesaurusDates: 'gmd\\:thesaurusName>gmd\\:CI_Citation>gmd\\:date>gmd\\:CI_Date, thesaurusName>CI_Citation>date>CI_Date',
    //'Data_ThesaurusDate: 'gmd\\:date>gco\\:Date, date Date',
    //'Data_ThesaurusDateType: 'gmd\\:dateType>gmd\\:CI_DateTypeCode, dateType CI_DateTypeCode',
    // Limits and constraints
    // Uselimitations
    Data_UseLimitations: 'gmd\\:resourceConstraints>gmd\\:MD_Constraints>gmd\\:useLimitation, resourceConstraints>MD_Constraints>useLimitation',
    Data_UseLimitation: 'gco\\:CharacterString, CharacterString',
    // Legal constraints
    //'Data_LegalConstraints: 'gmd\\:resourceConstraints>gmd\\:MD_LegalConstraints',
    // AccessConstraints
    Data_AccessConstraints: 'gmd\\:resourceConstraints>gmd\\:MD_LegalConstraints>gmd\\:accessConstraints, resourceConstraints>MD_LegalConstraints>accessConstraints',
    Data_RestrictionCode: 'gmd\\:MD_RestrictionCode, MD_RestrictionCode',
    //'Data_AccessConstraint_OthersConstraints: 'gmd\\:resourceConstraints>gmd\\:MD_LegalConstraints>gmd\\:otherConstraints, resourceConstraints MD_LegalConstraints otherConstraints',
    Data_AccessConstraint_OtherConstraints: 'gmd\\:resourceConstraints>gmd\\:MD_LegalConstraints>gmd\\:otherConstraints, resourceConstraints>MD_LegalConstraints>otherConstraints',
    Data_OtherConstraint: 'gmd\\:otherConstraints>gco\\:CharacterString, otherConstraints>CharacterString',
    //'Data_AccessConstraint_OthersConstraints: 'gmd\\:resourceConstraints>gmd\\:MD_LegalConstraints>gmd\\:otherConstraints>gco\\:CharacterString, resourceConstraints>MD_LegalConstraints>otherConstraints>CharacterString',
    // UseContraints
    Data_UseConstraints: 'gmd\\:resourceConstraints>gmd\\:MD_LegalConstraints>gmd\\:useConstraints, resourceConstraints>MD_LegalConstraints>useConstraints',
    //'Data_UseConstraint': '',
    //OtherConstraints
    //'Data_OtherConstraints: 'gmd\\:otherConstraints>gco\\:CharacterString',
    //'Data_OtherConstraint': '',
    // Fin de LegalConstraints
    Data_Classification: 'gmd\\:resourceConstraints>gmd\\:MD_SecurityConstraints>gmd\\:classification>gmd\\:MD_ClassificationCode, resourceConstraints>MD_SecurityConstraints>classification>MD_ClassificationCode',
    Data_SpatialRepresentationType: 'gmd\\:spatialRepresentationType>gmd\\:MD_SpatialRepresentationTypeCode, spatialRepresentationType>MD_SpatialRepresentationTypeCode',
    Data_ScaleDenominator: 'gmd\\:MD_RepresentativeFraction>gmd\\:denominator>gco\\:Integer, MD_RepresentativeFraction>denominator>Integer',
    Data_ScaleDistance: 'gmd\\:spatialResolution>gmd\\:MD_Resolution>gmd\\:distance>gco\\:Distance, spatialResolution>MD_Resolution>distance>Distance',
    // Languages
    Data_Languages: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:language, MD_Metadata>identificationInfo>MD_DataIdentification>language',
    Service_Languages: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:language, MD_Metadata>identificationInfo>SV_ServiceIdentification>language',
    Data_Language: 'gmd\\:LanguageCode, LanguageCode',
    Data_CharacterSet: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:characterSet>gmd\\:MD_CharacterSetCode, MD_Metadata>identificationInfo>MD_DataIdentification>characterSet>MD_CharacterSetCode',
    Service_CharacterSet: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:characterSet>gmd\\:MD_CharacterSetCode, MD_Metadata>identificationInfo>SV_ServiceIdentification>characterSet>MD_CharacterSetCode',
    // TopicCategories
    Data_TopicCategories: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:topicCategory, MD_Metadata>identificationInfo>MD_DataIdentification>topicCategory',
    Service_TopicCategories: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:topicCategory, MD_Metadata>identificationInfo>SV_ServiceIdentification>topicCategory',
    Data_TopicCategory: 'gmd\\:MD_TopicCategoryCode, MD_TopicCategoryCode',
    // Extents
    Data_Extents: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:extent>gmd\\:EX_Extent, MD_Metadata>identificationInfo>MD_DataIdentification>extent EX_Extent',
    Service_Extents: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:extent>gmd\\:EX_Extent, MD_Metadata>identificationInfo>SV_ServiceIdentification>extent EX_Extent',
    Data_ExtentName: 'gmd\\:description>gco\\:CharacterString, description>CharacterString',
    // GeographicExtents
    Data_ExtentNorthbound: 'gmd\\:geographicElement>gmd\\:EX_GeographicBoundingBox>gmd\\:northBoundLatitude>gco\\:Decimal, geographicElement EX_GeographicBoundingBox northBoundLatitude Decimal',
    Data_ExtentSouthbound: 'gmd\\:geographicElement>gmd\\:EX_GeographicBoundingBox>gmd\\:southBoundLatitude>gco\\:Decimal, geographicElement EX_GeographicBoundingBox southBoundLatitude Decimal',
    Data_ExtentEastbound: 'gmd\\:geographicElement>gmd\\:EX_GeographicBoundingBox>gmd\\:eastBoundLongitude>gco\\:Decimal, geographicElement EX_GeographicBoundingBox eastBoundLongitude Decimal',
    Data_ExtentWestbound: 'gmd\\:geographicElement>gmd\\:EX_GeographicBoundingBox>gmd\\:westBoundLongitude>gco\\:Decimal, geographicElement EX_GeographicBoundingBox westBoundLongitude Decimal',
    // TemporalExtents
    Data_TemporalExtent_Begin: 'gmd\\:temporalElement>gmd\\:EX_TemporalExtent>gmd\\:extent>gml\\:TimePeriod>gml\\:beginPosition, temporalElement EX_TemporalExtent extent TimePeriod beginPosition',
    Data_TemporalExtent_End: 'gmd\\:temporalElement>gmd\\:EX_TemporalExtent>gmd\\:extent>gml\\:TimePeriod>gml\\:endPosition, temporalElement EX_TemporalExtent extent TimePeriod endPosition',
    
    // VerticalExtents
    //'Data_VerticalExtents': '',
    //'Data_VerticalExtent_Max': '',
    //'Data_VerticalExtent_Unit': '',
    //'Data_VerticalExtent_Ref': '',
    // DistInfo
    //'Data_DistInfo: 'gmd\\:MD_Metadata>gmd\\:distributionInfo>gmd\\:MD_Distribution, MD_Metadata>distributionInfo MD_Distribution',
    // DistFormats
    Data_DistFormats: 'gmd\\:MD_Metadata>gmd\\:distributionInfo>gmd\\:MD_Distribution>gmd\\:distributionFormat>gmd\\:MD_Format, MD_Metadata>distributionInfo>MD_Distribution>distributionFormat>MD_Format',
    Data_DistFormatName: 'gmd\\:name>gco\\:CharacterString, name>CharacterString',
    Data_DistFormatVersion: 'gmd\\:version>gco\\:CharacterString, version>CharacterString',
    Data_DistFormatSpecification: 'gmd\\:specification>gco\\:CharacterString, specification>CharacterString',
    // Linkages
    Data_Linkages: 'gmd\\:MD_Metadata>gmd\\:distributionInfo>gmd\\:MD_Distribution>gmd\\:transferOptions>gmd\\:MD_DigitalTransferOptions>gmd\\:onLine>gmd\\:CI_OnlineResource, MD_Metadata>distributionInfo>MD_Distribution>transferOptions>MD_DigitalTransferOptions>onLine>CI_OnlineResource',
    Data_LinkageName: 'gmd\\:name>gco\\:CharacterString, name>CharacterString, gmd\\:name>gmx\\:MimeFileType, name>MimeFileType',
    Data_LinkageDescription: 'gmd\\:description>gco\\:CharacterString, description>CharacterString',
    Data_LinkageURL: 'gmd\\:linkage>gmd\\:URL, linkage>URL',
    Data_MaintenanceFrequency: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>gmd\\:MD_DataIdentification>gmd\\:resourceMaintenance>gmd\\:MD_MaintenanceInformation>gmd\\:maintenanceAndUpdateFrequency>gmd\\:MD_MaintenanceFrequencyCode, MD_Metadata>identificationInfo>MD_DataIdentification>resourceMaintenance>MD_MaintenanceInformation>maintenanceAndUpdateFrequency>MD_MaintenanceFrequencyCode',
    Service_MaintenanceFrequency: 'gmd\\:MD_Metadata>gmd\\:identificationInfo>srv\\:SV_ServiceIdentification>gmd\\:resourceMaintenance>gmd\\:MD_MaintenanceInformation>gmd\\:maintenanceAndUpdateFrequency>gmd\\:MD_MaintenanceFrequencyCode, MD_Metadata>identificationInfo>SV_ServiceIdentification>resourceMaintenance>MD_MaintenanceInformation>maintenanceAndUpdateFrequency>MD_MaintenanceFrequencyCode',
    Data_DQ_Level: 'gmd\\:MD_Metadata>gmd\\:dataQualityInfo>gmd\\:DQ_DataQuality>gmd\\:scope>gmd\\:DQ_Scope>gmd\\:level>gmd\\:MD_ScopeCode, MD_Metadata>dataQualityInfo>DQ_DataQualityscope>DQ_Scope>level>MD_ScopeCode',
    // Conformities
    Data_DQ_Conformities: 'gmd\\:MD_Metadata>gmd\\:dataQualityInfo>gmd\\:DQ_DataQuality>gmd\\:report, MD_Metadata>dataQualityInfo>DQ_DataQuality>report',
    Data_DQ_ConformityTest: 'gmd\\:DQ_DomainConsistency>gmd\\:result>gmd\\:DQ_ConformanceResult>gmd\\:specification>gmd\\:CI_Citation>gmd\\:title>gco\\:CharacterString, DQ_DomainConsistency>result>DQ_ConformanceResult>specification CI_Citation>title>CharacterString',
    Data_DQ_ConformityDates: 'gmd\\:DQ_DomainConsistency>gmd\\:result>gmd\\:DQ_ConformanceResult>gmd\\:specification>gmd\\:CI_Citation>gmd\\:date>gmd\\:CI_Date, DQ_DomainConsistency>result>DQ_ConformanceResult>specification>CI_Citation>date>CI_Date',
    //'Data_DQ_ConformityDate: 'gmd\\:date>gco\\:Date, date Date',
    //'Data_DQ_ConformityDateType: 'gmd\\:dateType>gmd\\:CI_DateTypeCode, dateType CI_DateTypeCode',
    Data_DQ_ConformityResult: 'gmd\\:DQ_DomainConsistency>gmd\\:result>gmd\\:DQ_ConformanceResult>gmd\\:explanation>gco\\:CharacterString, DQ_DomainConsistency>result>DQ_ConformanceResult>explanation>CharacterString',
    Data_DQ_ConformityPass: 'gmd\\:DQ_DomainConsistency>gmd\\:result>gmd\\:DQ_ConformanceResult>gmd\\:pass>gco\\:Boolean, DQ_DomainConsistency>result>DQ_ConformanceResult>pass>Boolean',
    Data_LI_Statement: 'gmd\\:lineage>gmd\\:LI_Lineage>gmd\\:statement>gco\\:CharacterString, lineage>LI_Lineage>statement>CharacterString',
    //'Data_LI_ProcessStep': '',
    //'Data_LI_Source': '',
    // Contact
    CntName: 'gmd\\:individualName>gco\\:CharacterString, individualName>CharacterString',
    CntFunction: 'gmd\\:positionName>gco\\:CharacterString, positionName>CharacterString',
    CntOrganism: 'gmd\\:organisationName>gco\\:CharacterString, organisationName>CharacterString',
    CntAddress: 'gmd\\:contactInfo>gmd\\:CI_Contact>gmd\\:address>gmd\\:CI_Address>gmd\\:deliveryPoint>gco\\:CharacterString, contactInfo>CI_Contact>address>CI_Address>deliveryPoint>CharacterString',
    CntPostalCode: 'gmd\\:contactInfo>gmd\\:CI_Contact>gmd\\:address>gmd\\:CI_Address>gmd\\:postalCode>gco\\:CharacterString, contactInfo>CI_Contact>address>CI_Address>postalCode>CharacterString',
    CntCity: 'gmd\\:contactInfo>gmd\\:CI_Contact>gmd\\:address>gmd\\:CI_Address>gmd\\:city>gco\\:CharacterString, contactInfo CI_Contact>address>CI_Address>city>CharacterString',
    CntPhone: 'gmd\\:contactInfo>gmd\\:CI_Contact>gmd\\:phone>gmd\\:CI_Telephone>gmd\\:voice>gco\\:CharacterString, contactInfo>CI_Contact>phone>CI_Telephone>voice>CharacterString',
    CntEmail: 'gmd\\:contactInfo>gmd\\:CI_Contact>gmd\\:address>gmd\\:CI_Address>gmd\\:electronicMailAddress>gco\\:CharacterString, contactInfo>CI_Contact>address>CI_Address>electronicMailAddress>CharacterString',
    CntLogo: 'gmd\\:contactInfo>gmd\\:CI_Contact>gmd\\:contactInstructions>gmx\\:FileName, contactInfo>CI_Contact>contactInstructions>FileName',
    CntRole: 'gmd\\:role>gmd\\:CI_RoleCode, role>CI_RoleCode'
};
    
