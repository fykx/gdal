def zonalstatistics(dem, data):
    from osgeo import gdal, osr, ogr
    import numpy as np

    in_ds_dem = gdal.Open(dem)
    in_band_dem = in_ds_dem.GetRasterBand(1)# 波段索引从1开始
    in_dem_array = in_band_dem.ReadAsArray()

    in_ds_data = gdal.Open(data)
    in_band_data = in_ds_data.GetRasterBand(1)# 波段索引从1开始
    in_data_array = in_band_data.ReadAsArray()


    i = 15

    value_dict = {}

    while i <= 49:
        out_mask_1 = np.ma.masked_where(in_data_array != i, in_dem_array)
        mean_value = np.mean(out_mask_1)
        value_dict[i] = mean_value
        out_mask_1 = None
        print(i, mean_value)
        i = i + 1
        
    return value_dict

def draw(dem, data, pathout):
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.pyplot import MultipleLocator

    value_dict = zonalstatistics(dem, data)

    x_array = np.array([x+1970 for x in range(len(value_dict))], dtype=float)
    
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

    x_major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim(1985, 2019)

    plt.ylabel('altitude (mean)') 
    plt.xlabel('year')
    fig.autofmt_xdate()

    fig.savefig(pathout + '/' + 'gain_dem' + '.png', dpi=300, bbox_inches='tight')
    plt.close()

    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dem', type=str, help='dem', required=True)
    parser.add_argument('-t', '--tcc', type=str, help='tcc', required=True)
    parser.add_argument('-o', '--output', type=str, help='output', required=True)
    args = parser.parse_args()

    draw(args.dem, args.tcc, args.output)
    return

if __name__ == '__main__':
    main()

# python stat_gain.py -d /public/home/mfeng/jwang/forest/northeast/dem/Reproject/clip_dem.tif -t /public/home/mfeng/jwang/forest/northeast/out/loss_gain/clip/clip_gain.tif -o /public/home/mfeng/jwang/forest/northeast/out/dem

