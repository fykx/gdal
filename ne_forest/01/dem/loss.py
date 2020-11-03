def listdatas(pathin):
    import os
    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def zonalstatistics(dem, data, pathout):
    from osgeo import gdal, osr, ogr
    import numpy as np

    in_ds_dem = gdal.Open(dem)
    in_band_dem = in_ds_dem.GetRasterBand(1)# 波段索引从1开始
    in_dem_array = in_band_dem.ReadAsArray()
    xsize = in_band_dem.XSize#列
    ysize = in_band_dem.YSize#行

    in_ds_data = gdal.Open(data)
    in_band_data = in_ds_data.GetRasterBand(1)# 波段索引从1开始
    in_data_array = in_band_data.ReadAsArray()

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + 'dem_'+data.split('/')[-1], xsize, ysize, 1, in_band_dem.DataType)
    out_ds.SetProjection(in_ds_dem.GetProjection())
    out_ds.SetGeoTransform(in_ds_dem.GetGeoTransform())

    out_mask_1 = np.ma.masked_where(in_data_array < 15, in_dem_array)
    out_mask_2 = np.ma.masked_where(in_data_array > 49, out_mask_1)
    out_mask_3 = np.ma.filled(out_mask_2, fill_value=-99.0)

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(out_mask_3)
    out_band.SetNoDataValue(-99.0)
    out_band.ComputeStatistics(False) 
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-de', '--dem', type=str, help='dem', required=True)
    parser.add_argument('-i', '--input', type=str, help='input', required=True)
    parser.add_argument('-o', '--output', type=str, help='output', required=True)
    args = parser.parse_args()

    datas = listdatas(args.input)
    for data in datas:
        print(data)
        zonalstatistics(args.dem, data, args.output)
    return

if __name__ == '__main__':
    main()

# python loss.py -d /public/home/mfeng/jwang/forest/northeast/dem/Reproject/clip_dem.tif -i /public/home/mfeng/jwang/forest/northeast/out/loss_gain/clip -o /public/home/mfeng/jwang/forest/northeast/out/dem
