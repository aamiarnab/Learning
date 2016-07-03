import unicodecsv
import datetime

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

def count_unique_student(filename):
    counter_set = set()
    for rec in filename:
        counter_set.add(rec['account_key'])
    return len(counter_set)

def create_paid_list(filename):
    paid_list = []
    for rec in filename:
        if rec['account_key'] in paid_students:
            paid_list.append(rec)
    return paid_list

enrollments = read_csv('../../data/enrollments.csv')
daily_engagement = read_csv('../../data/daily_engagement.csv')
project_submissions = read_csv('../../data/project_submissions.csv')

paid_students = {}
for enr_rec in enrollments:
    if enr_rec['is_udacity'] == 'False' and (enr_rec['days_to_cancel'] == '' or int(enr_rec['days_to_cancel']) > 7) :
        if enr_rec['account_key'] not in paid_students or paid_students[enr_rec['account_key']] < enr_rec['join_date']:
            paid_students[enr_rec['account_key']] = enr_rec['join_date']

paid_engagement = create_paid_list(daily_engagement)
engagement_record_first_week = []
for eng_rec in paid_engagement:
    acct = eng_rec['account_key']
    engagement_date = datetime.datetime.strptime(eng_rec['utc_date'] , '%d/%m/%Y')
    enrollment_date = datetime.datetime.strptime(paid_students[acct] , '%Y-%m-%d')
    if (engagement_date - enrollment_date).days< 7:
        engagement_record_first_week.append(eng_rec)

print len(engagement_record_first_week)
