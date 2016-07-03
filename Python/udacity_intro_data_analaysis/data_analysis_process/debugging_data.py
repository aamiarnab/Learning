import unicodecsv
import datetime
from collections import defaultdict


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
paid_enrollment = create_paid_list(enrollments)

engagement_record_first_week = []
for eng_rec in paid_engagement:
    acct = eng_rec['account_key']
    engagement_date = datetime.datetime.strptime(eng_rec['utc_date'] , '%d/%m/%Y')
    enrollment_date = datetime.datetime.strptime(paid_students[acct] , '%Y-%m-%d')
    if (engagement_date - enrollment_date).days< 7 and (engagement_date - enrollment_date).days >= 0:
    #if (engagement_date - enrollment_date).days< 7:
        engagement_record_first_week.append(eng_rec)

engagement_by_account = defaultdict(list)
for rec in engagement_record_first_week:
    account_key = rec['account_key']
    engagement_by_account[account_key].append(rec)

total_minutes_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0.0
    for eng_rec in engagement_for_student:
        total_minutes += float(eng_rec['total_minutes_visited'])
    total_minutes_by_account[account_key] = total_minutes

total_minutes = total_minutes_by_account.values()
import numpy as np
print "Mean:", np.mean(total_minutes)
print "Standard Deviation:", np.std(total_minutes)
print "Minimum:", np.min(total_minutes)
print "Maximum:", np.max(total_minutes)

#print total_minutes_by_account.keys()

for account_key, total_minutes in total_minutes_by_account.items():
    if total_minutes > 7000:
        print account_key, total_minutes
        for rec in paid_enrollment:
            if rec['account_key'] == account_key:
                print rec
