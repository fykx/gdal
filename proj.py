'''
Descripttion: 
version: 0.1
Author: Jianbang Wang
Date: 2020-08-11 16:44:05
'''

def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def test(pathin_data, pathout):
    from osgeo import gdal,ogr,osr
    
    import numpy as np

    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)
    sr_wkt = sr.ExportToWkt()

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + pathin_data.split('/')[-1].split('.')[0] + '.tif', 720, 332, 1, gdal.GDT_Float32)
    out_ds.SetProjection(sr_wkt)
    out_ds.SetGeoTransform((40.0, 0.25, 0.0, 70.0, 0.0, -0.25))

    out_data = np.zeros(shape=(332, 720))


    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(out_data)
    out_band.FlushCache()
    #out_band.SetNoDataValue(-99)
    out_band.ComputeStatistics(False)
    return

def main():
    pathin = r'C:\Users\fykx\Desktop\test\813'
    pathout = r'C:\Users\fykx\Desktop\test\out'
    datas = listdatas(pathin)

    for data in datas:
        print(data)
        test(data, pathout)
    return

if __name__ == "__main__":
    main()