def read(data_txt):
    '''读出无值栅格'''
    import re

    a = []
    f = open(data_txt, 'r')
    #f.readline()
    for line in f.readlines():
        a.append(re.split(',', line.strip())[0].split('/')[-1])
    f.close()
    return a

def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i.endswith('.tif'):
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def delte(data):
    '''影像删除'''
    import os

    os.system('rm -rf {}'.format(data))
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input', required=True)# 输入路径
    parser.add_argument('-t', '--txt', type=str, help='txt', required=True)# 输入txt
    args = parser.parse_args()

    a = read(args.txt)
    b = listdatas(args.input)

    for i in b:
        if i.split('/')[-1] in a:
            print(i)
            delte(i)
    return

if __name__ == '__main__':
    main()

#python del_outside.py -i /public/home/mfeng/jwang/forest/northeast/out/bzc/1 -t /public/home/mfeng/jwang/forest/northeast/code_tcc/inter_new/tcc/mean.txt