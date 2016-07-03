import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

def count_unique_student(file_name):
    counter_set = set()
    for rec in file_name:
        counter_set.add(rec['account_key'])
    return len(counter_set)

enrollments = read_csv('../../data/enrollments.csv')
daily_engagement = read_csv('../../data/daily_engagement.csv')
project_submissions = read_csv('../../data/project_submissions.csv')

paid_students = {}
for enr_rec in enrollments:
    if enr_rec['is_udacity'] == 'False' and (enr_rec['days_to_cancel'] == '' or int(enr_rec['days_to_cancel']) > 7) :
        if enr_rec['account_key'] not in paid_students or paid_students[enr_rec['account_key']] < enr_rec['join_date']:
            paid_students[enr_rec['account_key']] = enr_rec['join_date']
print len(paid_students)
print count_unique_student(enrollments)
