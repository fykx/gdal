import os
from osgeo import gdal
import numpy as np

'''读取HDF文件数据'''
def test(path):
    band_fn = path + '/' +  'MOD13Q1.A2015289.h25v06.006.2015317212006.hdf'
    ds = gdal.Open(band_fn)
    subdatasets = ds.GetSubDatasets()
    in_ds = gdal.Open(subdatasets[0][0])
    in_band = in_ds.GetRasterBand(1)
    in_data = in_band.ReadAsArray()
    driver  = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(path + '/' + 'modis_data.tif', in_band.XSize, in_band.YSize, 1, in_band.DataType)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(in_data)
    out_band.FlushCache()
    return

            
if __name__ == "__main__":
    path = os.getcwd()
    test(path)
    
