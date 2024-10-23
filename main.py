# TODO
# add fallback if no desirable students left
# optimize fetch function to only run student loop once by storing values in lists
# choose majority gender as first teammates

# config
school = ['CCDS', 'EEE', 'CoB (NBS)', 'SoH', 'WKW SCI', 'CoE', 'MAE', 'SPMS', 'SBS', 'SSS', 'ASE', 'NIE', 'ADM', 'CCEB', 'MSE', 'LKCMedicine', 'CEE', 'HASS']
team_size = 5
stat_gender = 3
stat_school = 2
stat_cgpa_tolerance = 0.5

# open and copy records
fp = open('records.csv','r')
pool = [i.replace('\n','').split(',') for i in fp.readlines()][1:]
tuts = [sorted(pool[i:i+50], key = lambda x: x[5]) for i in range(0,len(pool),50)]
fp.close()
fo = open('output.csv','w')

# fetch desirable student from the tutorial group
def fetch_std(tut,gender='MaleFemale',schools=[]):
    gnd, sch = [], []
    for std in tut:
        if std[4] in gender and std[2] not in schools: return std
        if std[4] in gender: gnd.append(std)
        if std[2] not in schools: sch.append(std)
    if gnd: return gnd[0]
    elif sch: return sch[0]
    else: return tut[0]

# for each tutorial group
for tut in tuts:
    # prioritize three of majority gender
    m_tut = f_tut = 0
    for std in tut:
        if std[4]=='Male': m_tut += 1
        else: f_tut += 1

    while tut:
        # TODO : Implement 3 of majority gender first, with two of them from the right end of tut
        team = [tut[0],tut[-1]]
        tut = tut[1:-1]
        m = f = 0
        cgpa = 0
        schools = {i:0 for i in school}

        # fetch and append
        while len(team)<team_size:
            for std in team:
                # school
                schools[std[2]] += 1
                # gender
                if std[4]=='Male': m+=1
                else: f+=1
                # cgpa
                cgpa += float(std[5])

            school_bl = [i for i in schools if schools[i]>2]

            if m>3: team.append(fetch_std(tut,gender='Female',schools=school_bl))
            elif f>3: team.append(fetch_std(tut,gender='Male',schools=school_bl))
            else: team.append(fetch_std(tut,schools=school_bl))
            
            # remove selected team members from the pool
            for k in team:
                if k in tut: tut.remove(k)

        for i in team: fo.write(','.join(i)+'\n')
        fo.write('\n')
        
fo.close()