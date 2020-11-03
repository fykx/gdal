def read(data_txt):
    '''读出无值栅格'''
    import re

    a = []
    f = open(data_txt, 'r')
    #f.readline()
    for line in f.readlines():
        a.append(re.split(',', line.strip())[0].split(' ')[-1])
    f.close()
    return a

def delte(data):
    '''影像删除'''
    import os

    os.system('rm -rf {}'.format(data))
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--txt', type=str, help='txt', required=True)# 输入路径
    args = parser.parse_args()

    a = read(args.txt)

    for i in a:
        delte(i)
    return

if __name__ == '__main__':
    main()