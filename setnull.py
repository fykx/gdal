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

def set_null(pathin_data, pathout):
    from osgeo import gdal
    import numpy as np

    in_ds = gdal.Open(pathin_data)
    in_band = in_ds.GetRasterBand(1)#波段索引从1开始
    nodata = in_band.GetNoDataValue()
    in_data = in_band.ReadAsArray()
    in_data = np.where(np.isnan(in_data),-99,in_data)
    xsize = in_band.XSize#列
    ysize = in_band.YSize#行
    print(nodata)

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + 'SETNULL_' + pathin_data.split('/')[-1], xsize, ysize, 1, in_band.DataType)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(in_data)
    out_band.FlushCache()
    out_band.SetNoDataValue(-99)
    out_band.ComputeStatistics(False)
    return

def main():
    pathin = r'C:\Users\Jayde\Desktop\1'
    pathout = r'C:\Users\Jayde\Desktop\2'
    datas = listdatas(pathin)

    for data in datas:
        print(data)
        set_null(data, pathout)
    return

if __name__ == "__main__":
    main()