def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def mean_raster(pathin, pathout, para_width, para_height):
    from osgeo import gdal
    import numpy as np
    import math

    datas = listdatas(pathin)
    datas.sort()

    in_ds = gdal.Open(datas[0])
    in_band = in_ds.GetRasterBand(1)
    #nodata = in_band.GetNoDataValue()
    xsize = in_band.XSize#列
    ysize = in_band.YSize#行
    
    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + 'mean_3.tif', xsize, ysize, 1, gdal.GDT_Float32)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    out_data = np.zeros(shape=(ysize, xsize))
    progress = 0
    for i in range(math.ceil(xsize/para_width)):#列
        for j in range(math.ceil(ysize/para_height)):#行
            print(round(progress/(math.ceil(xsize/para_width)*math.ceil(ysize/para_height))*100,2),'%')
            progress = progress + 1
            datas_array = []
            for data in datas:
                ds = gdal.Open(data)
                band = ds.GetRasterBand(1)
                if (i+1)*para_width <= xsize and (j+1)*para_height <= ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, para_width, para_height).astype(float)
                    f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(f_array)

                elif (i+1)*para_width > xsize and (j+1)*para_height <= ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, xsize - i*para_width, para_height).astype(float)
                    f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(f_array)

                elif (i+1)*para_width <= xsize and (j+1)*para_height > ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, para_width, ysize - j*para_height).astype(float)
                    f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(f_array)

                elif (i+1)*para_width > xsize and (j+1)*para_height > ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, xsize - i*para_width, ysize - j*para_height).astype(float)
                    f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(f_array)
                del ds

            height, width = f_array.shape

            for x in range(width):#遍历列
                for y in range(height):#遍历行
                    value_list = []
                    for array in datas_array:
                        if array[y, x] == -99.0:
                            pass
                        else:
                            value_list.append(array[y,x])
                    if len(value_list) == 0:
                        out_data[j*para_height+y, i*para_width+x] = -99.0
                    else:
                        out_data[j*para_height+y, i*para_width+x] = np.mean(value_list)

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(out_data)
    out_band.SetNoDataValue(-99.0)
    out_band.ComputeStatistics(False) 
    return

def main():
    pathin = r'/mnt/d/test/data'
    pathout = r'/mnt/d/test/out'
    para_width = 200#列（宽）
    para_height = 200#行（高）
    mean_raster(pathin, pathout, para_width, para_height)
    return

if __name__ == '__main__':
    main()