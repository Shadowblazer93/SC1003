fp = open('records_small.csv','r')
pool = [i.replace('\n','').split(',') for i in fp.readlines()][1:]
tuts = [sorted(pool[i:i+50], key = lambda x: x[5]) for i in range(0,len(pool),50)]
fp.close()

for tut in tuts:
    print(tut)