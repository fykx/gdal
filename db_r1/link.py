def readf(data_in):
    import re
    a=[]
    f = open(data_in,'r')
    f.readline()
    for line in f.readlines():
        a.append(re.split(',',line.strip()))
    f.close()
    return a

def link(a,b,pathout):
    data_a = readf(a)
    data_b = readf(b)

    nn = pathout + '/' + 'result_2.csv'
    f = open(nn, 'w')

    for i in data_a:
        for j in data_b:
            if i[0] == j[3] and i[1] == j[4]:
                for q in range(len(i)):
                    f.write('{},'.format(i[q]))
                f.write('{},{},{}\n'.format(j[7],j[8],j[1]))
    f.close()
    return

def main():
    a = r'/mnt/e/r1/out/csv/result_1.csv'
    b = r'/mnt/e/r1/test.csv'
    pathout = r'/mnt/e/r1/out/csv'
    link(a,b,pathout)
    return



if __name__ == '__main__':
    main()