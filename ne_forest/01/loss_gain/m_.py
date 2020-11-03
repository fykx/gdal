import os
#os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj'

def listdatas(pathin):
    '''列出同年份数据'''
    import os

    _datas = []
    _years = []
    for _root, _dirs, _files in os.walk(pathin):
        if len(_files) != 0:
            for _file in _files:
                _years.append(_file.split("_")[1])
                _vv = None
                if _file.endswith('.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas.append(_vv)

    _mosaic_datas = []
    fykx = ['_gain_year_n0_m1.tif', '_loss_year_n0_m1.tif']
    for ends in fykx:
        _mosaic_data = []
        for _data in _datas:
            if _data.endswith(ends):
                _mosaic_data.append(_data)
        _mosaic_datas.append(_mosaic_data)
    return _mosaic_datas

def mosaic(datas, pathout, pathout_sh):
    from osgeo import gdal

    nn = pathout_sh + '/' + datas[0].split('/')[-1].split('_')[1] + '.sh'
    f = open(nn,'w')

    f.write('gdal_merge.py -o {} -n 255 -a_nodata 255 '.format(pathout + '/' + datas[0].split('/')[-1].split('_')[1] + '.tif'))
    for i in datas:
        f.write('{} '.format(i))
    f.close()
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input', required=True)# 输入路径
    parser.add_argument('-o', '--output', type=str, help='output', required=True)# 输出路径
    parser.add_argument('-os', '--output_sh', type=str, help='output_sh', required=True)# .sh输出路径
    args = parser.parse_args()
    datas = listdatas(args.input)
    for datalist in datas:
        mosaic(datalist, args.output, args.output_sh)
    return

if __name__ == "__main__":
    main()

# python m_.py -i /public/home/mfeng/work/test/forest/pangyong/phase2/ne/forest/file12/scene04/comp01/change0a/r1/data -o /public/home/mfeng/jwang/forest/northeast/out/loss_gain -os /public/home/mfeng/jwang/forest/northeast/out/loss_gain