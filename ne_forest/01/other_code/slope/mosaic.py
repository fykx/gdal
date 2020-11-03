def listdatas(pathin):
    import os
    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i.endswith('.tif'):
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def mosaic(datas, pathout, pathout_sh):
    from osgeo import gdal

    nn = pathout_sh + '/' + 'mosaic.sh'
    f = open(nn,'w')

    f.write('gdal_merge.py -o {} -a_nodata -99.0 '.format(pathout + '/' + 'slope_mosaic' + '.tif'))
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
    mosaic(datas, args.output, args.output_sh)
    return

if __name__ == "__main__":
    main()