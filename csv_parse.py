fp = open('records_small.csv','r')
pool = [i.replace('\n','').split(',') for i in fp.readlines()]

for i in pool:
    print(i)