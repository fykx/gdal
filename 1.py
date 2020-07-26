'''
@Descripttion: 将栅格四个顶点转shp
@version: 0.1
@Author: Jianbang Wang
@Date: 2020-07-23 15:31:54
'''

def listdatas(pathin):
    import os

    _datas = []
    _years = []
    for _root, _dirs, _files in os.walk(pathin):
        if len(_files) != 0:
            for _file in _files:
                _years.append(_file.split("_")[2])
                _vv = None
                if _file.endswith('_dat.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas.append(_vv)

    _mosaic_datas = []               
    for _year in list(set(_years)):
        _mosaic_data = []
        for _data in _datas:
            if _data.split('\\')[-1].split("_")[2] == _year:
                _mosaic_data.append(_data)
        _mosaic_datas.append(_mosaic_data)
    return _mosaic_datas[0]

'''主函数'''
def main(pathin, pathout):
    import numpy as np
    from osgeo import gdal,ogr,osr
    
    _a = listdatas(pathin)#栅格数据列表

    #创建DataSource，并添加图层
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)
    _driver = ogr.GetDriverByName('ESRI Shapefile')
    _ds = _driver.CreateDataSource(pathout + '/' + '1' + '.shp')
    _lyr = _ds.CreateLayer('extent_point', sr, ogr.wkbPoint)

    #添加字段
    _fld = ogr.FieldDefn('name', ogr.OFTString)
    _fld.SetWidth(100)
    _lyr.CreateField(_fld)

    for _band_fn in _a:
        print(_band_fn.split('/')[-1])
        
        _in_ds = gdal.Open(_band_fn)
        _in_band = _in_ds.GetRasterBand(1)#波段索引从1开始
        _adfGeoTransform = _in_ds.GetGeoTransform()

        _xsize = _in_band.XSize#列
        _ysize = _in_band.YSize#行
        
        #左上角
        _lon_0 = _adfGeoTransform[0] + range(_xsize)[0] * _adfGeoTransform[1] + range(_ysize)[0] * _adfGeoTransform[2]
        _lat_0 = _adfGeoTransform[3] + range(_xsize)[0] * _adfGeoTransform[4] + range(_ysize)[0] * _adfGeoTransform[5]

        #右上角
        _lon_1 = _adfGeoTransform[0] + range(_xsize)[0] * _adfGeoTransform[1] + range(_ysize)[-1] * _adfGeoTransform[2]
        _lat_1 = _adfGeoTransform[3] + range(_xsize)[0] * _adfGeoTransform[4] + range(_ysize)[-1] * _adfGeoTransform[5]

        #左下角
        _lon_2 = _adfGeoTransform[0] + range(_xsize)[-1] * _adfGeoTransform[1] + range(_ysize)[0] * _adfGeoTransform[2]
        _lat_2 = _adfGeoTransform[3] + range(_xsize)[-1] * _adfGeoTransform[4] + range(_ysize)[0] * _adfGeoTransform[5]

        #右下角
        _lon_3 = _adfGeoTransform[0] + range(_xsize)[-1] * _adfGeoTransform[1] + range(_ysize)[-1] * _adfGeoTransform[2]
        _lat_3 = _adfGeoTransform[3] + range(_xsize)[-1] * _adfGeoTransform[4] + range(_ysize)[-1] * _adfGeoTransform[5]

        #写入几何、属性
        _feat_1 = ogr.Feature(_lyr.GetLayerDefn())#
        _ring = ogr.Geometry(ogr.wkbPoint)
        _ring.AddPoint(_lon_0, _lat_0)
        _feat_1.SetGeometry(_ring)#写入几何
        _feat_1.SetField(0, _band_fn.split('/')[-1].split('.')[0] + '_1')#写入属性
        _lyr.CreateFeature(_feat_1)

        _feat_2 = ogr.Feature(_lyr.GetLayerDefn())#
        _ring = ogr.Geometry(ogr.wkbPoint)
        _ring.AddPoint(_lon_3, _lat_3)
        _feat_2.SetGeometry(_ring)#写入几何
        _feat_2.SetField(0, _band_fn.split('/')[-1].split('.')[0] + '_2')#写入属性
        _lyr.CreateFeature(_feat_2)

        _feat_3 = ogr.Feature(_lyr.GetLayerDefn())#
        _ring = ogr.Geometry(ogr.wkbPoint)
        _ring.AddPoint(_lon_1, _lat_1)
        _feat_3.SetGeometry(_ring)#写入几何
        _feat_3.SetField(0, _band_fn.split('/')[-1].split('.')[0] + '_3')#写入属性
        _lyr.CreateFeature(_feat_3)

        _feat_4 = ogr.Feature(_lyr.GetLayerDefn())#
        _ring = ogr.Geometry(ogr.wkbPoint)
        _ring.AddPoint(_lon_2, _lat_2)
        _feat_4.SetGeometry(_ring)#写入几何
        _feat_4.SetField(0, _band_fn.split('/')[-1].split('.')[0] + '_4')#写入属性
        _lyr.CreateFeature(_feat_4)
    return
                              
if __name__ == "__main__":
    pathin = r'/home/forest/ne/data'
    pathout = r'/home/forest/ne/out'
    main(pathin, pathout)
    
    
