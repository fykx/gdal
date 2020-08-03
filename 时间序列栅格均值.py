'''
Descripttion: 
version: 0.1
Author: Jianbang Wang
Date: 2020-08-03 20:28:12
'''

def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def main(pathin, pathout):
    import numpy as np
    from osgeo import gdal
    from matplotlib import pyplot as plt
    from matplotlib.pyplot import MultipleLocator

    datas = listdatas(pathin)
    datas.sort()

    time_list = []
    data_list = []

    for i in datas:
        print(int(i.split('/')[-1].split('_')[3]))
        time_list.append(int(i.split('/')[-1].split('_')[3]))
        in_ds = gdal.Open(i)
        in_band = in_ds.GetRasterBand(1)
        in_data = in_band.ReadAsArray()
        in_data = np.ma.masked_where(in_data>100, in_data)
        data_list.append(np.mean(in_data))
    time_array = np.array(time_list)
    data_array = np.array(data_list)

    fig = plt.figure(figsize=(15, 3), dpi=300, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)

    ax.grid()
    ax.plot(time_array, data_array, 'go--', markersize=8)
    
    x_major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim(1985,2020)

    plt.ylabel('TCC(mean)') 
    plt.xlabel('Year')
    fig.autofmt_xdate()

    fig.savefig(pathout + '/' + 'time_list' + '.png', dpi=300, bbox_inches='tight')
    plt.close()
    return

if __name__ == "__main__":
    pathin = r'E:\forest_data\tianshui\tcc\maps\tcc'
    pathout = r'E:\forest_data\tianshui\time_main'
    main(pathin, pathout)