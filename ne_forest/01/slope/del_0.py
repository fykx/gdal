def listdatas(pathin):
    import os

    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i.endswith('.tif'):
            fn_i = pathin + '/' + i
            if os.path.getsize(fn_i) == 0:
                a.append(fn_i)
    return a

def delte(data):
    '''影像删除'''
    import os

    os.system('rm -rf {}'.format(data))
    return

def main():
    '删除大小为0的栅格'
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input', required=True)# 输入路径
    args = parser.parse_args()

    datas = listdatas(args.input)
    for data in datas:
        print(data)
        delte(data)
    return

if __name__ == '__main__':
    main()

# python del_0.py -i /public/home/mfeng/jwang/forest/northeast/out/slope/2
