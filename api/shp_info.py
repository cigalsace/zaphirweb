#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Get informations from SHP file and return Python objet like:
    {
        'dirname': 'shp'
        'base': '31372_bd_topo.shp'
        'filename': '31372_bd_topo',
        'size': 5720160L,
        'size_human': '5.5MiB', 
        'ext': '.shp',
        'is_shp': True,        
        'epsg': '2154', 
        'nb_features': 3471, 
        'extent': {
            'xmin': 987326.299999997, 
            'xmax': 1082910.7000000007, 
            'ymin': 6710818.3999999985
            'ymax': 6895714.2, 
        },
        'extent_wgs84': {
            'xmin': 6.813480012761984,
            'xmax': 8.241612082310239,
            'ymin': 49.04688173670964,
            'ymax': 47.43526128964639
        }
    }

"""

import sys
import os
import string

try:
    from osgeo import gdal
    from osgeo import osr
    from osgeo import ogr
    gdal_actif = True
except ImportError:
    print "Error with GDAL module"
    gdal_actif = False

esri_epsg = {
    'RGF_1993_Lambert_93': '2154',
    'RGF_1993_CC48': '3948',
    'RGF_1993_CC49': '3947'
}

def change_point_srs(x=None, y=None, input=None, output=None):
    # Spatial Reference System
    inputEPSG = input
    outputEPSG = output
    # create a geometry from coordinates
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(x, y)
    # create coordinate transformation
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(inputEPSG)
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(outputEPSG)
    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    # transform point
    point.Transform(coordTransform)
    # print point in EPSG output
    return point.GetX(), point.GetY()


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
    
def get_shp_info(shp_file):
    shp_info = { 'is_shp': False }
    if os.path.isfile(shp_file) and gdal_actif is True:
        shp_info['base'] = os.path.basename(shp_file)
        shp_info['filename'], shp_info['ext'] = os.path.splitext(shp_info['base'])
        shp_info['dirname'] = os.path.dirname(shp_file)    
        shp_info['size'] = os.path.getsize(shp_file)
        shp_info['size_human'] = sizeof_fmt(shp_info['size'])
        if shp_info['ext'].lower() == '.shp':
            shp_info['is_shp'] = True
            driver = ogr.GetDriverByName('ESRI Shapefile')
            data = driver.Open(shp_file, 0) # 0 means read-only. 1 means writeable.
            layer = data.GetLayer(0)
            
            # Get reference system (SRS)
            srs = layer.GetSpatialRef()
            srs.AutoIdentifyEPSG()
            shp_info['epsg'] = srs.GetAuthorityCode(None)
            if not shp_info['epsg'] and srs.IsProjected:
                shp_info['epsg'] = esri_epsg[srs.GetAttrValue('projcs')]
    
            # Number of features
            shp_info['nb_features'] = layer.GetFeatureCount()

            shp_info['extent'] = {}
            shp_info['extent_wgs84'] = {}
            extent = layer.GetExtent()
            if extent:
                wgs84_xmin, wgs84_ymin = change_point_srs(extent[0], extent[2], int(shp_info['epsg']), 4326)
                wgs84_xmax, wgs84_ymax = change_point_srs(extent[1], extent[3], int(shp_info['epsg']), 4326)
                shp_info['extent'] = {
                    'xmin': extent[0],
                    'xmax': extent[1],
                    'ymin': extent[2],
                    'ymax': extent[3]
                }
                shp_info['extent_wgs84'] = {
                    'xmin': wgs84_xmin,
                    'xmax': wgs84_xmax,
                    'ymin': wgs84_ymin,
                    'ymax': wgs84_ymax
                }

    return shp_info
                
if __name__ == "__main__":
    shp_file = "shp/31372_bd_topo.shp"
    print get_shp_info(shp_file)
