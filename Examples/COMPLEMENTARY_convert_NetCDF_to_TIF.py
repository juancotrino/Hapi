#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:27:24 2020

@author: juanmanuel
"""

from Hapi.raster import MultipleNetCDFtoTIF
from Hapi.raster import AlignMultipleRasters

#CONVERTION OF NETCDF FILES TO TIF FILES

start_date = "01-01-2000"
end_date = "06-01-2000"

src_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/NETCDF/"
file_first_str = "MSWEP_"
file_second_str = "00.nc"
date_format = "%Y%m%d"
reference_file = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"
dst_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/NETCDF/"
dst_label = "prec_"
dst_EPSG = 21897
no_data_value = -9999

MultipleNetCDFtoTIF(start_date, 
                    end_date, 
                    src_filepath, 
                    file_first_str, 
                    file_second_str, 
                    date_format,
                    dst_filepath, 
                    dst_label,
                    dst_EPSG,
                    no_data_value)

#ALIGN CONVERTED RASTERS TO A REFERENCE RASTER FILE

src_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/NETCDF/"
file_first_str = "prec_"
file_second_str = ".tif"
date_format = "%Y%m%d"
reference_file = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"
dst_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/NETCDF/"
dst_label = "prec_"#"aligned_" if the aligned test is uncommented, the rasters generated by the MultipleNetCDFtoTIF,
                             # and the paths are the same, the rasters will be replaced

AlignMultipleRasters(start_date, 
                     end_date, 
                     src_filepath, 
                     file_first_str, 
                     file_second_str, 
                     date_format,
                     reference_file,
                     dst_filepath, 
                     dst_label)