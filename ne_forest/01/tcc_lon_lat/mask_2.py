def zonalstatistics(input_shp, field_name, input_raster):
    from osgeo import gdal, osr, ogr
    import numpy as np

    in_ds = gdal.Open(input_raster)

    in_band = in_ds.GetRasterBand(1)# 波段索引从1开始
    in_data = in_band.ReadAsArray()

    driver = ogr.GetDriverByName('ESRI Shapefile')
    shp_ds = driver.Open(input_shp, 0)
    lyr = shp_ds.GetLayer(0)

    value_dict = {}

    for feat in lyr:
        field_value = feat.GetField(field_name)
        expression = "{} = '{}'".format(field_name, field_value)
        mask_ds = gdal.Warp('', input_raster, format='MEM', cutlineDSName=input_shp, cutlineWhere=expression, dstNodata = -99.0)# 注意此处nodata设置，关乎下方掩膜语句书写

        in_mask_band = mask_ds.GetRasterBand(1)
        in_mask_data = in_mask_band.ReadAsArray()

        out_mask = np.ma.masked_where(in_mask_data == -99.0, in_data)# 注意此处nodata设置

        mean_value = np.mean(out_mask)
        value_dict[field_value] = mean_value
        print(field_value, mean_value)
        del mask_ds
    del in_ds, shp_ds
    return value_dict

def draw(input_shp, field_name, input_raster, pathout):
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.pyplot import MultipleLocator

    value_dict = zonalstatistics(input_shp, field_name, input_raster)

    x_array = np.array([x for x in range(len(value_dict))], dtype=float)
    
    y_array = np.array([x for x in range(len(value_dict))], dtype=float)
    
    i = 0
    for key in value_dict.keys():
        x_array[i] = key
        y_array[i] = value_dict[key]
        i = i + 1

    fig = plt.figure(figsize=(15, 3), dpi=300, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)

    ax.grid()
    ax.plot(x_array, y_array, 'go--', markersize=8)

    x_major_locator = MultipleLocator(0.6)
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim(38.7, 53.5)

    plt.ylabel('TCC(mean)') 
    plt.xlabel('latitude')
    fig.autofmt_xdate()

    fig.savefig(pathout + '/' + 'latitude' + '.png', dpi=300, bbox_inches='tight')
    plt.close()

    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-is', '--input_shp', type=str, help='inputshp', required=True)# 输入矢量
    parser.add_argument('-fn', '--field_name', type=str, help='field_name', required=True)# 输入矢量
    parser.add_argument('-ir', '--input_raster', type=str, help='inputraster', required=True)# 输入栅格
    parser.add_argument('-o', '--output', type=str, help='output', required=True)# 输出路径
    args = parser.parse_args()

    draw(args.input_shp, args.field_name, args.input_raster, args.output)
    return

if __name__ == '__main__':
    main()

# python mask_2.py -is /public/home/mfeng/jwang/forest/northeast/out/tcc_lon_lat/1/lat_step.shp -fn step -ir /public/home/mfeng/jwang/forest/northeast/out/mean/2/mean_mosaic.tif -o /public/home/mfeng/jwang/forest/northeast/out/tcc_lon_lat/2


