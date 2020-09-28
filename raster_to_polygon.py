#功能描述：提取栅格影像矢量边界
#版本：1.1
#作者：王建邦
#编写时间：2019年8月7日

def listdatas(pathin):
    import os

    _datas = []
    _names = []
    for _root, _dirs, _files in os.walk(pathin):
        if len(_files) != 0:
            for _file in _files:
                _names.append(_file.split("_")[0])
                _vv = None
                if _file.endswith('.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas.append(_vv)

    _mosaic_datas = []               
    for _name in list(set(_names)):
        for _data in _datas:
            if _data.split('/')[-1].split('_')[0] == _name:
                _mosaic_datas.append(_data)
                break
    return _mosaic_datas

from osgeo import gdal,ogr,osr


def raster_extent(data, pathout):
    _in_ds = gdal.Open(data)
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
    
    #创建DataSource，并添加图层
    _driver = ogr.GetDriverByName('ESRI Shapefile')
    _ds = _driver.CreateDataSource(pathout + '/' + data.split('/')[-1].split('.')[0] + '.shp')
    _lyr = _ds.CreateLayer('extent', _in_ds.GetSpatialRef(), ogr.wkbPolygon)

    #添加字段
    _fld = ogr.FieldDefn('name', ogr.OFTString)
    _fld.SetWidth(100)
    _lyr.CreateField(_fld)

    #写入几何、属性
    _feat = ogr.Feature(_lyr.GetLayerDefn())
    _ring = ogr.Geometry(ogr.wkbLinearRing)
    _ring.AddPoint(_lon_0, _lat_0)
    _ring.AddPoint(_lon_1, _lat_1)
    _ring.AddPoint(_lon_3, _lat_3)
    _ring.AddPoint(_lon_2, _lat_2)
    _ring.AddPoint(_lon_0, _lat_0)
    _yard = ogr.Geometry(ogr.wkbPolygon)
    _yard.AddGeometry(_ring)
    _feat.SetGeometry(_yard)#写入几何
    _feat.SetField(0, data.split('.')[0])#写入属性
    _lyr.CreateFeature(_feat) 
    return

def main():
    pathin = r'/mnt/e/r1'
    pathout = r'/mnt/e/r1/out/shp'
    datas = listdatas(pathin)
    for data in datas:
        raster_extent(data, pathout)
    return
                              
if __name__ == "__main__":
    main()
    
    
