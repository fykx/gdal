'''
Descripttion: 无效值填充
version: 0.1
Author: Jianbang Wang
Date: 2020-08-27 09:46:40
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

def fill(datalist):
    import os
    import numpy as np
    from osgeo import gdal

    nodata = -99.0

    for i in range(len(datalist)):
        if i == range(len(datalist))[0]:
            print('Processing:',datalist[i])
            print(datalist[i+1])
            print(datalist[i+2])
            print('\n')
            in_ds_a = gdal.Open(datalist[i])
            in_band_a = in_ds_a.GetRasterBand(1)
            in_data_a = in_band_a.ReadAsArray().astype(float)
            in_data_a_mask = np.where(in_data_a>100.0, nodata, in_data_a)
            xsize = in_band_a.XSize#列
            ysize = in_band_a.YSize#行
            

            in_ds_b = gdal.Open(datalist[i+1])
            in_band_b = in_ds_b.GetRasterBand(1)
            in_data_b = in_band_b.ReadAsArray().astype(float)
            in_data_b_mask = np.where(in_data_b>100.0, nodata, in_data_b)

            in_ds_c = gdal.Open(datalist[i+2])
            in_band_c = in_ds_c.GetRasterBand(1)
            in_data_c = in_band_c.ReadAsArray().astype(float)
            in_data_c_mask = np.where(in_data_c>100.0, nodata, in_data_c)

            for x in range(xsize):#遍历列
                for y in range(ysize):#遍历行
                    value = []
                    if in_data_a_mask[y,x] == nodata:
                        value.append(in_data_b_mask[y,x])
                        value.append(in_data_c_mask[y,x])
                        for j in value:
                            if j == nodata:
                                value.remove(j)
                        if len(value) != 0:
                            in_data_a_mask[y,x] = np.mean(value)
                        if len(value) == 0:
                            in_data_a_mask[y,x] = nodata

            pathout = datalist[i].replace('tcc', 'tcc_fill')
            pathout_1 = pathout.replace('/' + pathout.split('/')[-1],'')
            if os.path.isdir(pathout_1):
                pass
            else:
                os.makedirs(pathout_1)
            pathout_data = datalist[i].replace('tcc', 'tcc_fill')

            gtiff_driver = gdal.GetDriverByName('GTiff')
            out_ds = gtiff_driver.Create(pathout_data, xsize, ysize, 1, gdal.GDT_Float32)
            out_ds.SetProjection(in_ds_a.GetProjection())
            out_ds.SetGeoTransform(in_ds_a.GetGeoTransform())

            out_band = out_ds.GetRasterBand(1)
            out_band.FlushCache()
            out_band.WriteArray(in_data_a_mask)
            out_band.SetNoDataValue(nodata)#设置nodata
            out_band.ComputeStatistics(False)

        elif i == range(len(datalist))[-1]:
            print('Processing:',datalist[i])
            print(datalist[i-1])
            print(datalist[i-2])
            print('\n')
            in_ds_a = gdal.Open(datalist[i])
            in_band_a = in_ds_a.GetRasterBand(1)
            in_data_a = in_band_a.ReadAsArray().astype(float)
            in_data_a_mask = np.where(in_data_a>100.0, nodata, in_data_a)
            xsize = in_band_a.XSize#列
            ysize = in_band_a.YSize#行
            

            in_ds_b = gdal.Open(datalist[i-1])
            in_band_b = in_ds_b.GetRasterBand(1)
            in_data_b = in_band_b.ReadAsArray().astype(float)
            in_data_b_mask = np.where(in_data_b>100.0, nodata, in_data_b)

            in_ds_c = gdal.Open(datalist[i-2])
            in_band_c = in_ds_c.GetRasterBand(1)
            in_data_c = in_band_c.ReadAsArray().astype(float)
            in_data_c_mask = np.where(in_data_c>100.0, nodata, in_data_c)

            for x in range(xsize):#遍历列
                for y in range(ysize):#遍历行
                    value = []
                    if in_data_a_mask[y,x] == nodata:
                        value.append(in_data_b_mask[y,x])
                        value.append(in_data_c_mask[y,x])
                        for j in value:
                            if j == nodata:
                                value.remove(j)
                        if len(value) != 0:
                            in_data_a_mask[y,x] = np.mean(value)
                        if len(value) == 0:
                            in_data_a_mask[y,x] = nodata

            pathout = datalist[i].replace('tcc', 'tcc_fill')
            pathout_1 = pathout.replace('/' + pathout.split('/')[-1],'')

            if os.path.isdir(pathout_1):
                pass
            else:
                os.makedirs(pathout_1)
            pathout_data = datalist[i].replace('tcc', 'tcc_fill')

            gtiff_driver = gdal.GetDriverByName('GTiff')
            out_ds = gtiff_driver.Create(pathout_data, xsize, ysize, 1, gdal.GDT_Float32)
            out_ds.SetProjection(in_ds_a.GetProjection())
            out_ds.SetGeoTransform(in_ds_a.GetGeoTransform())

            out_band = out_ds.GetRasterBand(1)
            out_band.FlushCache()
            out_band.WriteArray(in_data_a_mask)
            out_band.SetNoDataValue(nodata)#设置nodata
            out_band.ComputeStatistics(False)

        else:
            print('Processing:',datalist[i])
            print(datalist[i+1])
            print(datalist[i-1])
            print('\n')
            in_ds_a = gdal.Open(datalist[i])
            in_band_a = in_ds_a.GetRasterBand(1)
            in_data_a = in_band_a.ReadAsArray().astype(float)
            in_data_a_mask = np.where(in_data_a>100.0, nodata, in_data_a)
            xsize = in_band_a.XSize#列
            ysize = in_band_a.YSize#行
            

            in_ds_b = gdal.Open(datalist[i+1])
            in_band_b = in_ds_b.GetRasterBand(1)
            in_data_b = in_band_b.ReadAsArray().astype(float)
            in_data_b_mask = np.where(in_data_b>100.0, nodata, in_data_b)

            in_ds_c = gdal.Open(datalist[i-1])
            in_band_c = in_ds_c.GetRasterBand(1)
            in_data_c = in_band_c.ReadAsArray().astype(float)
            in_data_c_mask = np.where(in_data_c>100.0, nodata, in_data_c)

            for x in range(xsize):#遍历列
                for y in range(ysize):#遍历行
                    value = []
                    if in_data_a_mask[y,x] == nodata:
                        value.append(in_data_b_mask[y,x])
                        value.append(in_data_c_mask[y,x])
                        for j in value:
                            if j == nodata:
                                value.remove(j)
                        if len(value) != 0:
                            in_data_a_mask[y,x] = np.mean(value)
                        if len(value) == 0:
                            in_data_a_mask[y,x] = nodata

            pathout = datalist[i].replace('tcc', 'tcc_fill')
            pathout_1 = pathout.replace('/' + pathout.split('/')[-1],'')

            if os.path.isdir(pathout_1):
                pass
            else:
                os.makedirs(pathout_1)
            pathout_data = datalist[i].replace('tcc', 'tcc_fill')

            gtiff_driver = gdal.GetDriverByName('GTiff')
            out_ds = gtiff_driver.Create(pathout_data, xsize, ysize, 1, gdal.GDT_Float32)
            out_ds.SetProjection(in_ds_a.GetProjection())
            out_ds.SetGeoTransform(in_ds_a.GetGeoTransform())

            out_band = out_ds.GetRasterBand(1)
            out_band.FlushCache()
            out_band.WriteArray(in_data_a_mask)
            out_band.SetNoDataValue(nodata)#设置nodata
            out_band.ComputeStatistics(False)
    return


def main():
    pathin = r'/home/forest/NEChina/tcc/maps/data'
    for pathin_datalist in listdatas(pathin):
        fill(pathin_datalist)
    return

if __name__ == "__main__":
    main()

