def zonalstatistics(input_shp, field_name, input_raster):
    from osgeo import gdal, osr, ogr
    import numpy as np

    in_ds = gdal.Open(input_raster)
    print(in_ds)
    in_band = in_ds.GetRasterBand(1)# 波段索引从1开始
    in_data = in_band.ReadAsArray()

    xsize = in_band.XSize# 列
    ysize = in_band.YSize# 行

    mem_driver = gdal.GetDriverByName('MEM')
    mem_ds = mem_driver.Create('', xsize, ysize, 1, gdal.GDT_Byte)
    mem_ds.SetProjection(in_ds.GetProjection())
    mem_ds.SetGeoTransform(in_ds.GetGeoTransform())
    # srs.SetWellKnownGeogCS('WGS84')
    # mid_ds.SetProjection(srs.ExportToWkt())

    # sr = osr.SpatialReference()
    # sr.ImportFromEPSG(4326)
    mem_ds.GetRasterBand(1).WriteArray(np.ones((xsize, ysize), dtype=np.bool))

    driver = ogr.GetDriverByName('ESRI Shapefile')
    shp_ds = driver.Open(input_shp, 0)
    lyr = shp_ds.GetLayer(0)

    for feat in lyr:
        field_value = feat.GetField(field_name)
        expression = "{} = '{}'".format(field_name, field_value)
        mask_ds = gdal.Warp('', mem_ds, format='MEM', cutlineDSName=input_shp, cutlineWhere=expression, dstNodata = 0)

        in_mask_band = mask_ds.GetRasterBand(1)
        in_mask_data = in_mask_band.ReadAsArray()
        print(in_mask_data.shape)

        out_mask_1 = np.ma.masked_where(in_mask_data == 0, in_data)

        out_mask_2 = np.ma.masked_where(out_mask_1 == -99.0, out_mask_1)
        mean_value = np.mean(out_mask_2)
        print(field_value, mean_value)
        del mask_ds
    del in_ds, mem_ds, shp_ds
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-is', '--input_shp', type=str, help='inputshp', required=True)# 输入矢量
    parser.add_argument('-fn', '--field_name', type=str, help='field_name', required=True)# 输入矢量
    parser.add_argument('-ir', '--input_raster', type=str, help='inputraster', required=True)# 输入栅格
    args = parser.parse_args()

    zonalstatistics(args.input_shp, args.field_name, args.input_raster)
    return

if __name__ == '__main__':
    main()

# python mask.py -is /mnt/e/r_tcc/out/test.shp -fn step -ir /mnt/e/r_tcc/out/h1508v234.tif
# python mask.py -is /mnt/e/r_tcc/out/test.shp -fn step -ir /mnt/e/r_tcc/out/h1508v234.tif


