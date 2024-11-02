# config
school = ['CCDS', 'EEE', 'CoB (NBS)', 'SoH', 'WKW SCI', 'CoE', 'MAE', 'SPMS', 'SBS', 'SSS', 'ASE', 'NIE', 'ADM', 'CCEB', 'MSE', 'LKCMedicine', 'CEE', 'HASS']
team_size = 5
#stat_gender = 3
#stat_school = 2
#stat_cgpa_tolerance = 0.5
toggle_cgpa = 0

# open and copy records
fp = open('records.csv','r')
pool = [i.replace('\n','').split(',') for i in fp.readlines()][1:]
tuts = [sorted(pool[i:i+50], key = lambda x: x[5]) for i in range(0,len(pool),50)]
fp.close()
fo = open('output.csv','w')

# fetch desirable student from the tutorial group
def fetch_std(tut,gender='MaleFemale',schools=[]):
    global toggle_cgpa
    toggle_cgpa = (toggle_cgpa+1)%2 # switch between 0 and 1
    if toggle_cgpa: tut = tut[::-1] # reverse tut group every other run

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
        if len(tut)<team_size: break

        m = f = 0
        cgpa = 0
        schools = {i:0 for i in school}

        team = []
        for i in range(2):
            if m_tut>f_tut: k = fetch_std(tut,gender='Female')
            else: k = fetch_std(tut,gender='Male')
            team.append(k)
            tut.remove(k)

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

            school_bl = [i for i in schools if schools[i]>1]

            if m>3: team.append(fetch_std(tut,gender='Female',schools=school_bl))
            elif f>3: team.append(fetch_std(tut,gender='Male',schools=school_bl))
            else: team.append(fetch_std(tut,schools=school_bl))
            
            # remove selected team members from the pool
            for k in team:
                if k in tut: tut.remove(k)

        for i in team: fo.write(','.join(i)+'\n')
        fo.write('\n')
        
fo.close()