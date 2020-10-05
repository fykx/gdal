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

def divide(datas, n):
    mpi_datas = {}
    step = len(datas)//n
    for i in range(n):
        if i < n-1:
            mpi_data = datas[i*step:(i+1)*step]
            mpi_datas[i] = mpi_data
        else:
            mpi_data = datas[i*step:]
            mpi_datas[i] = mpi_data

    j = 0
    while len(mpi_datas[n-1]) > step and j < n-1:
        mpi_datas[j].append(mpi_datas[n-1][-1])
        mpi_datas[n-1].remove(mpi_datas[n-1][-1])
        j = j + 1
    
    mpi_datas_out = []
    for mpi_data_out in mpi_datas.values():
        mpi_datas_out.append(mpi_data_out)
    return mpi_datas_out




def raster_extent(data, pathout):
    from osgeo import gdal,ogr,osr

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

import click
@click.command()
@click.option('-i', '--input', type=str, help='input', required=True)# 输入路径
@click.option('-o', '--output', type=str, help='output', required=True)# 输出路径
@click.option('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
def main(input, output, number):
    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD
    from tqdm import tqdm
    
    datas = listdatas(input)
    mpi_datas = divide(datas, number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for mpi_data in tqdm(mpi_data_divide):
        raster_extent(mpi_data, output)
    return
                              
if __name__ == "__main__":
    main()
    # mpiexec -n 4 python toshp.py -i /mnt/e/r1/data -o /mnt/e/r1/out/shp -n 4
    

