# TODO
# add fallback if no desirable students left

school = ['CCDS', 'EEE', 'CoB (NBS)', 'SoH', 'WKW SCI', 'CoE', 'MAE', 'SPMS', 'SBS', 'SSS', 'ASE', 'NIE', 'ADM', 'CCEB', 'MSE', 'LKCMedicine', 'CEE', 'HASS']

team_size = 5
stat_gender = 3
stat_school = 3
stat_cgpa_tolerance = 0.5

# open and copy records
fp = open('records_small.csv','r')
pool = [i.replace('\n','').split(',') for i in fp.readlines()][1:]
#tuts = [pool[i:i+50] for i in range(0,len(pool),50)]
tuts = [sorted(pool[i:i+50], key = lambda x: x[5]) for i in range(0,len(pool),50)]
fp.close()

# fetch desirable student from the tutorial group
def fetch_std(tut,gender='MaleFemale',schools=[]):
    for std in tut:
        if std[4] in gender and std[2] not in schools:
            return std
    else:
        # TODO IMPLEMENT CASE WHEN NO DESIRABLE STUDENTS ARE LEFT
        pass

# for each tutorial group
for tut in tuts:
    #while tut:
    team = tut[:2]
    tut = tut[2:]
    m = f = 0
    cgpa = 0
    schools = {i:0 for i in school}


    # example fetch and append
    while len(team)<5:
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

    for i in team: print(i)
    print('\n')