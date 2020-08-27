'''
Descripttion: slope
version: 0.1
Author: Jianbang Wang
Date: 2020-08-27 16:05:44
'''
def listdatas(pathin):
    import os

    _datas = []
    for _root, _dirs, _files in os.walk(pathin):
        _datas_i = []
        if len(_files) != 0:
            for _file in _files:
                _vv = None
                if _file.endswith('.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas_i.append(_vv)
        _datas_i.sort()
        if len(_datas_i) != 0:
            _datas.append(_datas_i)
    return _datas

def slope(datalist, pathout):
    import math
    import os
    import numpy as np
    from osgeo import gdal

    print(datalist[0].split('/')[-1].split('.')[0].split('_')[0])

    datalist.sort()
    in_ds = gdal.Open(datalist[0])
    in_band = in_ds.GetRasterBand(1)
    xsize = in_band.XSize
    ysize = in_band.YSize

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + datalist[0].split('/')[-1].split('.')[0].split('_')[0] + '.tif', xsize, ysize, 1, gdal.GDT_Float32)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    para_0 = np.zeros(shape=(ysize, xsize))
    para_1 = np.zeros(shape=(ysize, xsize))

    q = 0
    w = 0
    for i in datalist:
        ds = gdal.Open(i)
        band = ds.GetRasterBand(1)
        data_array = band.ReadAsArray().astype(float)
        data_mask_array = np.where(data_array==-99.0, np.nan, data_array)

        para_0 = para_0 + (data_mask_array * float(i.split('/')[-1].split('.')[0].split('_')[3]))
        q = q + float(i.split('/')[-1].split('.')[0].split('_')[3])
        para_1 = para_1 + data_mask_array
        w = w + math.pow(float(i.split('/')[-1].split('.')[0].split('_')[3]),2)
    para_a = len(datalist) * para_0
    para_b = para_1 * q
    para_c = len(datalist) * w - math.pow(q,2)
    out_data = (para_a - para_b) / para_c
    out_array = np.where(np.isnan(out_data), -99.0, out_data)

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(out_array)
    out_band.SetNoDataValue(-99.0)
    out_band.ComputeStatistics(False) 
    return

def main():
    pathin = r'/home/forest/NEChina/tcc_fill/maps/data/h306'
    pathout = r'/home/forest/NEChina/out/slope/1'
    datalists = listdatas(pathin)
    for datalist in datalists:
        slope(datalist, pathout)
    return

if __name__ == '__main__':
    main()

