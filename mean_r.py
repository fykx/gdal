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
    xsize = in_band.XSize
    ysize = in_band.YSize

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + 'mean.tif', xsize, ysize, 1, gdal.GDT_Float32)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    para_0 = np.zeros(shape=(ysize, xsize))

    for data in datas:
        print(data.split('/')[-1])
        ds = gdal.Open(data)
        band = ds.GetRasterBand(1)
        data_array = band.ReadAsArray().astype(float)
        data_mask_array = np.where(data_array>100.0, np.nan, data_array)
        para_0 = para_0 + data_mask_array
    out_array = para_0/len(datas)
    out_array = np.where(np.isnan(out_array), -99.0, out_array)

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(out_array)
    out_band.SetNoDataValue(-99.0)#设置nodata时注意创建栅格的类型（int?folat?）
    out_band.ComputeStatistics(False) 
    return

def main():
    pathin = r'/home/forest/tianshui/tcc_c'
    pathout = r'/home/forest/tianshui/2_result/mean_raster'
    mean_raster(pathin, pathout)
    return

if __name__ == '__main__':
    main()