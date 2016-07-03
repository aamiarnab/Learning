import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

#enrollments = read_csv('/datasets/ud170/udacity-students/enrollments.csv')
#daily_engagement = read_csv('/datasets/ud170/udacity-students/daily_engagement.csv')
#project_submissions = read_csv('/datasets/ud170/udacity-students/project_submissions.csv')

enrollments = read_csv('../../data/enrollments.csv')
daily_engagement = read_csv('../../data/daily_engagement.csv')
project_submissions = read_csv('../../data/project_submissions.csv')

unique_engagement = set()
for rec in daily_engagement:
    unique_engagement.add(rec['account_key'])

for enr_rec in enrollments:
    if enr_rec['account_key'] not in unique_engagement:
        if enr_rec['days_to_cancel'] != '0':
            print enr_rec
