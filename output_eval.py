school = ['CCDS', 'EEE', 'CoB (NBS)', 'SoH', 'WKW SCI', 'CoE', 'MAE', 'SPMS', 'SBS', 'SSS', 'ASE', 'NIE', 'ADM', 'CCEB', 'MSE', 'LKCMedicine', 'CEE', 'HASS']

fp = open("output.csv","r")
pool = [i.replace('\n','').split(',') for i in fp.readlines() if i!='\n']

# bad teams counters
flag_mf = 0
flag_gpa = 0
flag_sch = 0
teams = 0

for i in range(0,len(pool),5):
    team = pool[i:i+5]
    teams += 1
    m = f =0
    cgpa = 0
    schools = {i:0 for i in school}
    
    for std in team:
        # school
        schools[std[2]] += 1
        # gender
        if std[4]=='Male': m+=1
        else: f+=1
        # cgpa
        cgpa += float(std[5])
    
    school_bl = [i for i in schools if schools[i]>2]

    if m>3 or f>3:
        flag_mf += 1
        for k in team: print(k)
        print('\n')

    if school_bl:
        flag_sch += 1
        for k in team: print(k)
        print('\n')

print("Teams with undesirable gender ratios : ",flag_mf)
print("Teams with undesirable school ratios : ",flag_sch)
print("Total teams : ",teams)