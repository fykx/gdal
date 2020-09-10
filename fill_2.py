'''
Descripttion: 无效值填充(线性插值法)
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
        if i < range(len(datalist))[2]:
            pass

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
            try:
                print('Processing:',datalist[i])
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

                in_ds_b_l = gdal.Open(datalist[i-1])
                in_band_b_l = in_ds_b_l.GetRasterBand(1)
                in_data_b_l = in_band_b_l.ReadAsArray().astype(float)
                in_data_b_l_mask = np.where(in_data_b_l>100.0, nodata, in_data_b_l)

                in_ds_c_l = gdal.Open(datalist[i-2])
                in_band_c_l = in_ds_c_l.GetRasterBand(1)
                in_data_c_l = in_band_c_l.ReadAsArray().astype(float)
                in_data_c_l_mask = np.where(in_data_c_l>100.0, nodata, in_data_c_l)

                for x in range(xsize):#遍历列
                    for y in range(ysize):#遍历行
                        l = {}
                        r = {}
                        if in_data_a_mask[y,x] == nodata:
                            r[int(datalist[i+1].split('/')[-1].split('_')[2])] = in_data_b_mask[y,x]
                            r[int(datalist[i+2].split('/')[-1].split('_')[2])] = in_data_c_mask[y,x]
                            nodata_r = []
                            for key_r in r.keys():
                                if r[key_r] == nodata:
                                    nodata_r.append(key_r)
                            for i_r in nodata_r:
                                r.pop(i_r)
                            
                            if len(r) != 0:
                                keys_r = []
                                for key_r_1 in r.keys():
                                    keys_r.append(key_r_1)
                                keys_r.sort()
                                year_r = keys_r[0]
                                value_r = r[keys_r[0]]

                            l[int(datalist[i-1].split('/')[-1].split('_')[2])] = in_data_b_l_mask[y,x]
                            l[int(datalist[i-2].split('/')[-1].split('_')[2])] = in_data_c_l_mask[y,x]
                            nodata_l = []
                            for key_l in l.keys():
                                if l[key_l] == nodata:
                                    nodata_l.append(key_l)
                            for i_l in nodata_l:
                                l.pop(i_l)

                            if len(l) != 0:
                                keys_l = []
                                for key_l_1 in l.keys():
                                    keys_l.append(key_l_1)
                                keys_l.sort()
                                year_l = keys_l[-1]
                                value_l = l[keys_l[-1]]
                            
                            if len(r) != 0 and len(l) != 0:
                                year = int(datalist[i].split('/')[-1].split('_')[2])
                                slope = (value_r - value_l) / (year_r - year_l)
                                b = value_l - (slope * year_l)
                                in_data_a_mask[y,x] = year * slope + b
                            else:
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

            except:
                print('Processing:',datalist[i])
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

                in_ds_b_l = gdal.Open(datalist[i-1])
                in_band_b_l = in_ds_b_l.GetRasterBand(1)
                in_data_b_l = in_band_b_l.ReadAsArray().astype(float)
                in_data_b_l_mask = np.where(in_data_b_l>100.0, nodata, in_data_b_l)

                in_ds_c_l = gdal.Open(datalist[i-2])
                in_band_c_l = in_ds_c_l.GetRasterBand(1)
                in_data_c_l = in_band_c_l.ReadAsArray().astype(float)
                in_data_c_l_mask = np.where(in_data_c_l>100.0, nodata, in_data_c_l)

                for x in range(xsize):#遍历列
                    for y in range(ysize):#遍历行
                        l = {}
                        r = {}
                        if in_data_a_mask[y,x] == nodata:
                            r[int(datalist[i+1].split('/')[-1].split('_')[2])] = in_data_b_mask[y,x]
                            nodata_r = []
                            for key_r in r.keys():
                                if r[key_r] == nodata:
                                    nodata_r.append(key_r)
                            for i_r in nodata_r:
                                r.pop(i_r)

                            if len(r) != 0:
                                keys_r = []
                                for key_r_1 in r.keys():
                                    keys_r.append(key_r_1)
                                keys_r.sort()
                                year_r = keys_r[0]
                                value_r = r[keys_r[0]]

                            l[int(datalist[i-1].split('/')[-1].split('_')[2])] = in_data_b_l_mask[y,x]
                            l[int(datalist[i-2].split('/')[-1].split('_')[2])] = in_data_c_l_mask[y,x]
                            nodata_l = []
                            for key_l in l.keys():
                                if l[key_l] == nodata:
                                    nodata_l.append(key_l)
                            for i_l in nodata_l:
                                l.pop(i_l)
                            
                            if len(l) != 0:
                                keys_l = []
                                for key_l_1 in l.keys():
                                    keys_l.append(key_l_1)
                                keys_l.sort()
                                year_l = keys_l[-1]
                                value_l = l[keys_l[-1]]
                            
                            if len(r) != 0 and len(l) != 0:
                                year = int(datalist[i].split('/')[-1].split('_')[2])
                                slope = (value_r - value_l) / (year_r - year_l)
                                b = value_l - (slope * year_l)
                                in_data_a_mask[y,x] = year * slope + b
                            else:
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
    pathin = r'/home/wangjb19/NEChina/tcc/maps'
    for pathin_datalist in listdatas(pathin):
        fill(pathin_datalist)
    return

if __name__ == "__main__":
    main()

