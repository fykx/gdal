def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i.endswith('.tif'):
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def get_hist(pathin):
    from osgeo import gdal
    import numpy as np

    datas = listdatas(pathin)

    hists = {}
    for i in datas:
        print(i.split('/')[-1])
        ds = gdal.Open(i)
        band = ds.GetRasterBand(1)
        hist = band.GetHistogram(-10, 2490, 25, include_out_of_range=False, approx_ok=False)
        hist_array = np.array(hist)
        hists[i.split('/')[-1].split('.')[0]] = hist_array
    return hists

def draw(pathin, pathout):
    from matplotlib import pyplot as plt
    from matplotlib.pyplot import MultipleLocator
    import numpy as np

    lists = get_hist(pathin)
    x = [x*100-10 for x in range(26)]
    x_array = np.array(x)

    for i in lists.keys():
        data_array = lists[i]# /np.sum(lists[i])*100
        fig, ax = plt.subplots(1,1,figsize=(6,4))
        plt.bar(x_array, data_array, align =  'center')


        '''
        ax = plt.gca()
        y_major_locator = MultipleLocator(j)
        ax.yaxis.set_major_locator(y_major_locator)
        plt.ylim(0,int(np.max(data_array)) + 1 + q)
        '''

        plt.title(i + ' ' + 'Histogram') 
        plt.ylabel('Frequency') 
        plt.xlabel('Pixel Value')
        fig.savefig(pathout + '/' + i + '.png', dpi=300, bbox_inches='tight')
        plt.close()
    return

if __name__ == "__main__":
    pathin = r'/public/home/mfeng/jwang/forest/northeast/out/dem'
    pathout = r'/public/home/mfeng/jwang/forest/northeast/out/dem'
    draw(pathin, pathout)