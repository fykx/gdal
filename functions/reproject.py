def reprojection(t_srs, srcnodata, dstnodata, resample, input, output):
    '''重投影栅格'''
    import os
    #os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj' # 当在服务器上运行时取消注释

    from osgeo import gdal,ogr,osr
    os.system("gdalwarp -t_srs '{}' -srcnodata {} -dstnodata {} -r {} {} {}".format(t_srs, srcnodata, dstnodata, resample, input, output))
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-ts', '--t_srs', type=str, help='t_srs', required=True)# 输出投影
    parser.add_argument('-sn', '--srcnodata', type=str, help='srcnodata', required=True)# 输入文件nodata值
    parser.add_argument('-dn', '--dstnodata', type=str, help='dstnodata', required=True)# 输出文件nodata值
    parser.add_argument('-r', '--resample', type=str, help='resample', required=True)# 重采样方法 near bilinear cubic ...
    parser.add_argument('-i', '--input', type=str, help='input', required=True)# 输入文件
    parser.add_argument('-o', '--output', type=str, help='output', required=True)# 输出路径
    args = parser.parse_args()

    reprojection(args.t_srs, args.srcnodata, args.dstnodata, args.resample, args.input, args.output)
    return

if __name__ == "__main__":
    main()

# python reproject.py -ts '+proj=aea +lat_0=0 +lon_0=105 +lat_1=25 +lat_2=47 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs' -sn -99.0 -dn -99.0 -r near -i /mnt/e/r_tcc/code/h1500v200_y2019_dat.tif -o /mnt/e/r_tcc/234.tif

