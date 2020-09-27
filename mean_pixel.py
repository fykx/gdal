def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def mean_raster(pathin, pathout):
    from osgeo import gdal
    import numpy as np

    datas = listdatas(pathin)
    datas.sort()

    in_ds = gdal.Open(datas[0])
    in_band = in_ds.GetRasterBand(1)
    #nodata = in_band.GetNoDataValue()
    xsize = in_band.XSize
    ysize = in_band.YSize

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + 'mean.tif', xsize, ysize, 1, gdal.GDT_Float32)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    out_data = np.zeros(shape=(ysize, xsize))

    datas_array = []
    for data in datas:
        ds = gdal.Open(data)
        band = ds.GetRasterBand(1)
        data_array = band.ReadAsArray().astype(float)
        f_array = np.where(np.isnan(data_array), -99.0, data_array)
        datas_array.append(f_array)

    for x in range(xsize):#遍历列
        for y in range(ysize):#遍历行
            value_list = []
            for array in datas_array:
                if array[y,x] == -99.0:
                    pass
                else:
                    value_list.append(array[y,x])
            if len(value_list) == 0:
                out_data[y,x] = -99.0
            else:
                out_data[y,x] = np.mean(value_list)

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(out_data)
    out_band.SetNoDataValue(-99.0)
    out_band.ComputeStatistics(False) 
    return

def main():
    pathin = r'/mnt/d/test/data'
    pathout = r'/mnt/d/test/out'
    mean_raster(pathin, pathout)
    return

if __name__ == '__main__':
    main()