def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i.endswith('.hdf'):
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def test(data, pathout):
    from osgeo import gdal
    import numpy as np

    in_ds = gdal.Open(data)
    in_band = in_ds.GetRasterBand(1)
    nodata = in_band.GetNoDataValue()

    in_data = in_band.ReadAsArray()
    driver  = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(pathout + '/' + data.split('/')[-1].replace('.hdf','.tif'), in_band.XSize, in_band.YSize, 1, in_band.DataType)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(in_data)
    out_band.SetNoDataValue(nodata)
    out_band.ComputeStatistics(False) 
    return

def main():
    pathin = r'/mnt/d/test/hdf'
    pathout = r'/mnt/d/test/result'
    datas = listdatas(pathin)
    for data in datas:
        print(data.split('/')[-1])
        test(data, pathout)
    return
            
if __name__ == "__main__":
    main()
    
