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
        engagement_record_first_week.append(eng_rec)
'''
engagement_by_account = defaultdict(list)
for rec in engagement_record_first_week:
    account_key = rec['account_key']
    engagement_by_account[account_key].append(rec)
'''
def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data

engagement_by_account = group_data(engagement_record_first_week, 'account_key')

'''
total_lessons_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    total_lessons = 0.0
    for eng_rec in engagement_for_student:
        total_lessons += float(eng_rec['lessons_completed'])
    total_lessons_by_account[account_key] = total_lessons
'''
def get_total_by_key(data, measure_name):
    total_by_key = {}
    for key_name, data_list in data.items():
        total_value = 0.0
        for data_point in data_list:
            total_value += float(data_point[measure_name])
        total_by_key[key_name] = total_value
    return total_by_key

total_lessons_by_account = get_total_by_key(engagement_by_account, 'lessons_completed')

total_lessons = total_lessons_by_account.values()

import numpy as np
def describe_data(data):
    print "Mean:", np.mean(total_lessons)
    print "Standard Deviation:", np.std(total_lessons)
    print "Minimum:", np.min(total_lessons)
    print "Maximum:", np.max(total_lessons)

describe_data(total_lessons)
