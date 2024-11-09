toggle_cgpa = 0
school = ['CCDS', 'EEE', 'CoB (NBS)', 'SoH', 'WKW SCI',
          'CoE', 'MAE', 'SPMS', 'SBS', 'SSS', 'ASE','NIE',
          'ADM', 'CCEB', 'MSE', 'LKCMedicine', 'CEE', 'HASS']


# config
team_size_input = int(input("Enter team size : "))

# open and copy records
with open('records.csv','r') as records:
    header = records.readline() # store first line of records.csv
    cohort = [i[:-1].split(',') for i in records.readlines()] # convert records to list
    tuts = [sorted(cohort[i:i+50], key = lambda x:x[5]) for i in range(0,len(cohort),50)] # 2D list of all students sorted by cgpa

output = open('output.csv','w')
output.write(header[:-1]+',Team Assigned\n') # write output.csv file table headers


# fetch desirable student from the tutorial group
def fetch_std(tut,gender='',schools=[]):
    global toggle_cgpa
    toggle_cgpa ^= 1 # switch between 0 and 1
    if toggle_cgpa: tut = tut[::-1] # reverse tut group every other run

    gender_match, school_match = [], []
    for std in tut:
        if std[4] in gender and std[2] not in schools: return std # return perfect match if found
        if std[4] in gender: gender_match.append(std)
        if std[2] not in schools: school_match.append(std)
    if gender_match: return gender_match[0] # else return gender match
    elif school_match: return school_match[0] # else return non-blacklisted school
    else: return tut[0] # else return first student from tut


# for each tutorial group
for tut_grp in tuts:
    team_no = 0
    extra_members = 50 % team_size_input

    while tut_grp:
        team_size = team_size_input
        if extra_members:
            team_size += 1
            extra_members -= 1

        # tutorial group statistics
        m_tut = f_tut = 0
        for student in tut_grp:
            if student[4]=='Male': m_tut += 1
            else: f_tut += 1

        # team variables
        males = females = 0
        schools = {i:0 for i in school}
        team = []
        team_no += 1

        # append minority gender to team
        for _ in range(team_size//2):
            if m_tut>f_tut: member = fetch_std(tut_grp,gender='Female')
            else: member = fetch_std(tut_grp,gender='Male')
            team.append(member)
            tut_grp.remove(member)

        # fetch and append to team
        while len(team)<team_size:
            for std in team:
                schools[std[2]] += 1 # school
                if std[4]=='Male': males += 1 # gender
                else: females += 1
            school_bl = [i for i in schools if schools[i]>team_size//2-1] # blacklist schools with 2+ members

            if males>3: team.append(fetch_std(tut_grp,gender='Female',schools=school_bl))
            elif females>3: team.append(fetch_std(tut_grp,gender='Male',schools=school_bl))
            else: team.append(fetch_std(tut_grp,schools=school_bl))
            
            # remove selected team members from the pool
            for member in team:
                if member in tut_grp: tut_grp.remove(member)

        # write to file output.csv
        for member in team:
            member.append(str(team_no)) # attach team number to each student
            output.write(','.join(member)+'\n')
        
output.close()