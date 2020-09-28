def read(data):
    import re
    a = []
    f = open(data, 'r')
    f.readline()
    for line in f.readlines():
        a.append(str(re.split(',', line.strip())[0]) + '_' +str(re.split(',', line.strip())[1]))
    f.close()
    return a,list(set(a))


def main():
    data = r'/mnt/e/r1/out/csv/result_1.csv'
    a, list_a = read(data)
    for i in list_a:
        a.remove(i)
    for j in a:
        print(j)
            
    return

if __name__ == '__main__':
    main()